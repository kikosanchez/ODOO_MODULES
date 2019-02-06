# -*- coding: utf-8 -*-
#import web_pdb; web_pdb.set_trace()
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale

class MyWebsiteSale(WebsiteSale):

    # Devuelve True si una variante se puede vender
    def _variant_can_be_sold(self, variant):
        # Cogemos las variantes con stock o que se venden independientemente del inventario
        # El inventario no se puede cambiar para una sola variante, afecta a todo el producto, aunque aquí se coge de la variante
        # Si inventory_availability es False (no tiene un valor) no se vende
        if  (variant.inventory_availability == 'always' and variant.virtual_available > 0) \
            or (variant.inventory_availability == 'threshold' and variant.virtual_available >= variant.available_threshold) \
            or (variant.inventory_availability == 'never' or variant.inventory_availability == 'custom'):
                return True

        return False

    # Devuelve una Lista con los ID de variantes que se pueden vender
    def _get_attribute_ids_with_stock(self, product):
        attribute_value_ids = []

        for variant in product.product_variant_ids:
            for variant_value in variant.attribute_value_ids:
                if  self._variant_can_be_sold(variant.sudo()): attribute_value_ids.append(variant_value.id)

        # Crear una lista con valores únicos
        return list(dict.fromkeys(attribute_value_ids))

    # Sobreescribe a un método de la clase WebsiteSale para desactivar variantes que no se pueden vender
    def get_attribute_value_ids(self, product):
        quantity = product._context.get('quantity') or 1
        product = product.with_context(quantity=quantity)

        visible_attrs_ids = product.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped('attribute_id').ids
        to_currency = request.website.get_current_pricelist().currency_id
        attribute_value_ids = []

        for variant in product.product_variant_ids:
            if to_currency != product.currency_id:
                price = variant.currency_id.compute(variant.website_public_price, to_currency) / quantity
            else:
                price = variant.website_public_price / quantity

            visible_attribute_ids = [v.id for v in variant.attribute_value_ids if v.attribute_id.id in visible_attrs_ids]
            if  self._variant_can_be_sold(variant.sudo()): attribute_value_ids.append([variant.id, visible_attribute_ids, variant.website_price / quantity, price])

        return attribute_value_ids

    # Sobreescribe a un método de la clase WebsiteSale para desactivar variantes que no se pueden vender
    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        product_context = dict(request.env.context,
                               active_id=product.id,
                               partner=request.env.user.partner_id)
        ProductCategory = request.env['product.public.category']

        if category:
            category = ProductCategory.browse(int(category)).exists()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/shop', category=category and category.id, search=search, attrib=attrib_list)

        categs = ProductCategory.search([('parent_id', '=', False)])

        pricelist = request.website.get_current_pricelist()

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)

        if not product_context.get('pricelist'):
            product_context['pricelist'] = pricelist.id
            product = product.with_context(product_context)

        values = {
            'search': search,
            'category': category,
            'pricelist': pricelist,
            'attrib_values': attrib_values,
            'compute_currency': compute_currency,
            'attrib_set': attrib_set,
            'keep': keep,
            'categories': categs,
            'main_object': product,
            'product': product,
            # Pasar valores en vez de función
            'product_attributes': self.get_attribute_value_ids(product),
            # Pasar ids de atributos con stock
            'attr_ids_with_stock': self._get_attribute_ids_with_stock(product)
        }

        return request.render("website_sale.product", values)
