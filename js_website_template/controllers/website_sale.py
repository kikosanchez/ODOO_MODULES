# -*- coding: utf-8 -*-
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class JsWebTemplateWebsiteSale(WebsiteSale):
    # Campos obligatorios en la dirección de facturación
    def _get_mandatory_billing_fields(self):
        result = super(JsWebTemplateWebsiteSale, self)._get_mandatory_billing_fields()
        # result.append('zip');
        return result

    # Campos obligatorios en la dirección de envío
    def _get_mandatory_shipping_fields(self):
        result = super(JsWebTemplateWebsiteSale, self)._get_mandatory_shipping_fields()
        # result.append('zip');
        return result

    # Modificar validaciones
    def checkout_form_validate(self, mode, all_form_values, data):
        result = list(super(JsWebTemplateWebsiteSale, self).checkout_form_validate(mode, all_form_values, data))
        # zip validation
        if data.get('zip'):
            if not data.get('zip').isdigit() or len(data.get('zip')) != 5:
                result[0]['zip'] = 'error'
                result[1].append(_('ZIP Code is not valid.'))
        return tuple(result)

    # Para corregir problema al mostrar el precio del producto
    # https://trello.com/c/EtrtWRyi/72-odoo-modifica-el-precio-del-producto-al-a%C3%B1adir-o-quitar-unidades-en-el-sitio-web
    @http.route(['/shop/get_unit_price'], type='json', auth="public", methods=['POST'], website=True)
    def get_unit_price(self, product_ids, add_qty, **kw):
        products = request.env['product.product'].with_context({'quantity': add_qty}).browse(product_ids)
        # return {product.id: product.website_price / add_qty for product in products}
        return {product.id: product.website_price for product in products}

    # Para que no se puedan añadir al carro productos sin precio
    # https://trello.com/c/haFQLVA4/14-hacer-que-no-se-puedan-comprar-art%C3%ADculos-sin-precio
    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        product = request.env['product.product'].search([('id','=',product_id)])

        if (product.website_price <= 0):
            return False

        return super(JsWebTemplateWebsiteSale, self).cart_update(product_id, add_qty=1, set_qty=0, **kw)
