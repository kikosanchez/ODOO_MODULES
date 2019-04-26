from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    featured_product = fields.Boolean('Featured', default=False, help="If checked, this product appears first")
