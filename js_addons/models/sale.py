# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import time

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # discontinued_product = fields.Boolean('Discontinued', default=False, related='product_id.discontinued_product')
    discontinued_product = fields.Boolean(compute='_compute_product_discontinued')

    # Si una de las variantes está descatalogada decimos que la plantilla también lo está
    def _template_discontinued(self):
        if hasattr(self, 'order_lines'):
            for line in self.order_lines:
                if (line.product_id.discontinued_product):
                    return True

        if hasattr(self, 'product_id') and hasattr(self.product_id, 'discontinued_product'):
            return self.product_id.discontinued_product

        return False

    @api.depends('product_id')
    def _compute_product_discontinued(self):
        for record in self:
            record.discontinued_product = record._template_discontinued()

    @api.model
    def ts_product_id_change(self, product_id, partner_id, pricelist_id, get_stock=False):
        # product = self.env['product.product'].browse(product_id)
        # result = super(SaleOrderLine, self).ts_product_id_change(product_id, partner_id, pricelist_id)

        if not pricelist_id:
            pricelist_id = self.env['res.partner'].browse(partner_id).property_product_pricelist.id

        order = self.env['sale.order'].new({
            'partner_id': partner_id,
            'date_order': time.strftime("%Y-%m-%d"),
            'pricelist_id': pricelist_id
        })

        line = self.new({
            'order_id': order.id,
            'product_id': product_id
        })

        line.product_id_change()
        line._onchange_discount()

        return {
            'price_unit': line.price_unit,
            'product_uom': line.product_uom.id,
            'product_uom_qty': line.product_uom_qty,
            'discount': line.discount,
            'tax_id': [x.id for x in line.tax_id],
            'standard_price': line.product_id.standard_price,
            'discontinued': line._template_discontinued()
        }
