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
    @api.depends('partner_id', 'date_order', 'pricelist_id', 'order_line.product_id', 'order_line.product_uom_qty')
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
                    qty = line.product_uom_qty
                    # Precio del listado para el cliente (total, precio * cantidad)
                    product_list_price = order.pricelist_id.get_product_price(line.product_id, qty, order.partner_id, order.date_order) * qty
                    # Precio específico del cliente (total, precio * cantidad)
                    customer_price = (self._get_customer_price(order.partner_id, line.product_id, qty, order.date_order, tmpls_in_order) * qty) or product_list_price
                    # Calcular descuento
                    customer_discount = product_list_price - customer_price
                    # Si el descuento es 0 quiere decir que no hay cambios en el precio 
                    # (o no tiene un precio específico) por lo que la omitimos, a no ser que
                    # el precio haya cambiado
                    if customer_discount != 0 or line.price_old:
                        # Volvemos a dividir el precio para obtenerlo por unidad
                        # es necesario redondearlo al número de decimales configurado para
                        # asegurarnos que coincida
                        decimal_places = order.partner_id.property_product_pricelist.currency_id.decimal_places
                        product_list_price = round(product_list_price/qty, decimal_places)
                        customer_price = round(customer_price/qty, decimal_places)

                        # Guardar nuevos datos (necesario para recalcular todas las líneas y no sólo la actual)
                        line.write({
                            # Precio de línea
                            'price_unit': customer_price,
                            # Precio del cliente, se guarda para poder compararlo a posterior
                            'price_ctm': customer_price if product_list_price != customer_price else 0.0, 
                            # Precio anterior a esta sobreescritura
                            'price_old': product_list_price if product_list_price != customer_price else 0.0
                        })

                        # Si es un precio manual no lo actualizamos (sabemos que es manual
                        # porque no está en la tarifa ni en los precios de cliente)
                        if line.price_unit in (product_list_price, customer_price, line.price_ctm):
                            # Hay que recalcular el total
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
                            line.update({
                                # Precio de línea
                                'price_unit': customer_price,
                                # Subtotal de la línea
                                'price_subtotal': customer_price_taxes['total_excluded'], 
                                # Total de la línea
                                'price_total': customer_price_taxes['total_included']
                            })

                            # Actualizar precio (price_reduce_taxinc/price_reduce_taxexcl)
                            line._get_price_reduce()
                # Actualizar descuento total en pedido
                order.update({ 'customer_discounts': customer_discounts })
        # Hacer cálculos restantes (actualiza los totales)
        if recalculate_totals:
            super(SaleOrder, self)._amount_all()

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # Aquí se almacena el importe que se debería cobrar si no tuviese un precio específico
    price_old = fields.Float('Pricelist price', digits=dp.get_precision('Product Price'), default=0.0)
    # Aquí se almacena el precio específico del cliente
    price_ctm = fields.Float('Customer price', digits=dp.get_precision('Product Price'), default=0.0)