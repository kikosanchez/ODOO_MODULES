# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Aquí se almacena el importe descontado en el pedido para este cliente sobre su tarifa (por tener un precio especial)
    customer_discounts = fields.Monetary(string='Customer discounts', readonly=True, default=0.0)

    ##api.depends('order_line.price_total')
    ## def _amount_all(self):
    ##  
    ##  for order in self:
    ##      order.customer_discounts = sum(x.price_olf- x.price.ctm for x in order.order_line
    ## return super().....
    
    
    @api.model
    def _get_product_templates(self):
        tmpls_in_order = {}
        # Recorremos todas las líneas para obtener una relacción
        # de plantillas y cantidad total de variantes
        for line in self.order_line:
            tmpls_in_order.update({
                line.product_id.product_tmpl_id.id: tmpls_in_order.get(line.product_id.product_tmpl_id.id, 0) + line.product_uom_qty
            })
        return tmpls_in_order

    @api.model
    def _get_customer_price(self, partner, product, qty, date, tmpls_variants_rel):
        # Precio específico del cliente
        price = self.env['customer.price'].get_customer_price(partner, product, qty, date)
        # Si no obtuvimos un precio para el producto lo buscamos para la plantilla
        if not price:
            tmpl_variants_qty = tmpls_variants_rel.get(product.product_tmpl_id.id, 0)
            price = self.env['customer.price'].get_price_obj(partner.id, product.product_tmpl_id.id, tmpl_variants_qty, date, 'product_tmpl_id').price or 0.0
        return price * qty

    @api.model
    def _recalculate_prices_for_customer(self, partner_id, partner_shipping_id, pricelist_id, date_order):
        # Suma de descuentos
        customer_discounts = 0.0
        # Relación de ID de plantillas y número de variantes en el pedido
        tmpls_in_order = self._get_product_templates()
        # Recorremos de nuevo las líneas para recalcular los precios
        for line in self.order_line:
            newdata = line._recalculate_prices_for_customer(partner_id, partner_shipping_id, pricelist_id, date_order, tmpls_in_order)
            if newdata:
                customer_discount = newdata['price_old'] - newdata['price_ctm']
                # Si el descuento es menor a 0 no lo trataremos como tal pero aplicaremos 
                # igualmente su precio, en caso contrario lo sumamos al total
                if customer_discount > 0:
                        customer_discounts += customer_discount
                line.write(newdata)
        # Devolver descuento total
        return customer_discounts

    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, attributes=None, **kwargs):
        self.ensure_one()
        result = super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty, attributes, **kwargs)
        self.customer_discounts = self.sudo()._recalculate_prices_for_customer(self.partner_id, self.partner_shipping_id, self.pricelist_id, self.date_order)
        return result

    @api.model
    def create(self, values):
        date_order = values.get('date_order', False)
        partner_id = self.env['res.partner'].browse(values['partner_id'])
        partner_shipping_id = self.env['res.partner'].browse(values['partner_shipping_id'])
        pricelist_id = self.env['product.pricelist'].browse(values['pricelist_id'])

        values.update({
            'customer_discounts': self._recalculate_prices_for_customer(partner_id, partner_shipping_id, pricelist_id, date_order)
        })

        return super(SaleOrder, self).create(values)

    @api.multi
    def write(self, values):
        isWrited = super(SaleOrder, self).write(values)
        if isWrited:
            for order in self:
                if not order.state in ('done', 'cancel'):
                    if values.get('order_line', False) or values.get('partner_id', False) or values.get('partner_shipping_id', False) or values.get('date_order', False) or values.get('pricelist_id', False):
                        order.customer_discounts = self._recalculate_prices_for_customer(order.partner_id, order.partner_shipping_id, order.pricelist_id, order.date_order)
        return isWrited

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # Aquí se almacena el importe que se debería cobrar si no tuviese un precio específico
    price_old = fields.Float('Pricelist Price', digits=dp.get_precision('Product Price'), default=0.0)
    # Aquí se almacena el precio específico del cliente
    price_ctm = fields.Float('Customer Price', digits=dp.get_precision('Product Price'), default=0.0)
    
    ##
    ##@api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    ##def _compute_amount(self):
    ## si la plantilla de la línea tiene variantes y si hay variantes en las líneas de pedido,   
    ## lines_to_check = self.order_id.order_lines.filtered(lambda x: x.product_id.product_tmpl_id==line.product_id.product_tmpl_id
    ## if lines_to_check:
    ##  lines_toc_check ._recalculate_prices_for_customer(.....)
    ##
    ## con esto calculas por línea lo que necesites
    
    @api.model
    def _recalculate_prices_for_customer(self, partner_id, partner_shipping_id, pricelist_id, date_order, tmpls_in_order):
        qty = self.product_uom_qty
        # Precio del listado para el cliente (total, precio * cantidad)
        product_list_price = pricelist_id.get_product_price(self.product_id, qty, partner_id, date_order) * qty
        # Precio específico del cliente (total, precio * cantidad)
        customer_price = self.order_id._get_customer_price(partner_id, self.product_id, qty, date_order, tmpls_in_order) or product_list_price
        # Calcular descuento
        customer_discount = product_list_price - customer_price
        # Si el descuento es 0 quiere decir que no hay cambios en el precio 
        # (o no tiene un precio específico) por lo que la omitimos, a no ser que
        # el precio haya cambiado
        if customer_discount != 0 or self.price_old or self.price_ctm:
            # Volvemos a dividir el precio para obtenerlo por unidad
            # es necesario redondearlo al número de decimales configurado para
            # asegurarnos que coincida
            decimal_places = partner_id.property_product_pricelist.currency_id.decimal_places
            product_list_price = round(product_list_price/qty, decimal_places)
            customer_price = round(customer_price/qty, decimal_places)
            # Si es un precio manual no lo actualizamos (sabemos que es manual
            # porque no está en la tarifa ni en los precios de cliente)
            if self.price_unit in (product_list_price, customer_price, self.price_old, self.price_ctm):
                # Calcular impuestos del nuevo precio
                customer_price_taxes = self.tax_id.compute_all(customer_price, self.currency_id, self.product_uom_qty, product=self.product_id, partner=partner_shipping_id)

                return {
                    'price_unit': customer_price,
                    'price_ctm': customer_price if customer_discount != 0 else 0.0, 
                    'price_old': product_list_price if customer_discount != 0 else 0.0,
                    'price_subtotal': customer_price_taxes['total_excluded'], 
                    'price_total': customer_price_taxes['total_included']
                }

        return False
