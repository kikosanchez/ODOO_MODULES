# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Aquí se almacena el importe descontado en el pedido para este cliente sobre su tarifa (por tener un precio especial)
    customer_discounts = fields.Monetary(string='Customer discounts', store=True, readonly=True, default=0.0, compute='_recalculate_prices_for_customer')

    @api.model
    def _get_product_templates(self):
        self.ensure_one()
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
        return price

    @api.multi
    @api.depends('partner_id', 'date_order', 'pricelist_id', 'order_line.product_id', 'order_line.price_total')
    def _recalculate_prices_for_customer(self):
        # Flag para saber si hay que recalcular el total
        recalculate_totals = False
        # Recorremos los pedidos
        for order in self:
            # Relación de ID de plantillas y número de variantes en el pedido
            tmpls_in_order = order._get_product_templates()
            # No se puede hacer nada en pedidos bloqueados o cancelados
            if not order.state in ('done', 'cancel'):
                # Contador para almacenar el total
                customer_discounts = 0.0
                # Recorremos de nuevo las líneas para recalcular los precios
                for line in order.order_line:
                    # Precio del listado para el cliente (total, precio * cantidad)
                    product_list_price = order.pricelist_id.get_product_price(line.product_id, line.product_uom_qty, order.partner_id, order.date_order) * line.product_uom_qty
                    # Precio específico del cliente (total, precio * cantidad)
                    customer_price = (self._get_customer_price(order.partner_id, line.product_id, line.product_uom_qty, order.date_order, tmpls_in_order) * line.product_uom_qty) or product_list_price
                    # Calcular descuento
                    customer_discount = product_list_price - customer_price
                    # Si el descuento es 0 quiere decir que no hay cambios en el precio 
                    # (o no tiene un precio específico) por lo que la omitimos, a no ser que
                    # el precio haya cambiado
                    if customer_discount != 0 or line.price_old:
                        # Volvemos a dividir el precio para obtenerlo por unidad
                        product_list_price = product_list_price / line.product_uom_qty
                        customer_price = customer_price / line.product_uom_qty
                        # Si una línea es diferente hay que recalcular el total
                        recalculate_totals = True
                        # Si el descuento es menor a 0 hay algún error en las tarifas o este 
                        # cliente tiene un precio más alto que en su tarifa por algún motivo
                        # entonces no lo trataremos como un descuento pero aplicaremos 
                        # igualmente su precio, en caso contrario lo sumamos al total
                        if customer_discount > 0:
                            customer_discounts += customer_discount

                        # Calcular impuestos del nuevo precio
                        customer_price_taxes = line.tax_id.compute_all(customer_price, order.currency_id, line.product_uom_qty, product=line.product_id, partner=order.partner_shipping_id)
                        
                        # Actualizar línea
                        line.write({
                            'price_unit': customer_price,
                            'price_subtotal': customer_price_taxes['total_excluded'],
                            'price_total': customer_price_taxes['total_included'],
                            'price_old': product_list_price if customer_discount > 0 else 0.0
                        })

                        # Actualizar precio en la interfaz
                        line._get_price_reduce()
                # Actualizar descuento total en pedido
                order.update({ 'customer_discounts': customer_discounts })
        # Hacer cálculos restantes (actualiza los totales)
        if recalculate_totals:
            super(SaleOrder, self)._amount_all()

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # Aquí se almacena el importe que se debería cobrar si no tuviese un precio específico (si no lo tiene será 0)
    price_old = fields.Float('Customer price after discount', drequired=False, digits=dp.get_precision('Product Price'), default=0.0)