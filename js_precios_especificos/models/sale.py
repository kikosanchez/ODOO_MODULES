# © 2019 Jim Sports
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _get_display_price(self, product):
        res = super(SaleOrderLine, self)._get_display_price(product)
        # Buscar precios específicos en variantes
        qty = product._context.get('quantity', 1.0)
        vals = {}
        partner_id = self.order_id.partner_id.id
        date = self.order_id.date_order
        customer_price = self.env['customer.price'].get_customer_price(partner_id, product, qty, date=date)
        if customer_price:
            return customer_price
        return res
