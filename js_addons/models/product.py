from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    discontinued_product = fields.Boolean('Discontinued', default=False, help="If checked, the product will not be sold in main company")

    def _set_variant_discontinued(self, values):
        if 'discontinued_product' in values:
            for variant in self.product_variant_ids:
                variant.discontinued_product = values['discontinued_product']

    @api.model
    def create(self, vals):
        self._set_variant_discontinued(vals);
        return super(ProductTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        self._set_variant_discontinued(vals);
        return super(ProductTemplate, self).write(vals)

class ProductProduct(models.Model):
    _inherit = "product.product"

    discontinued_product = fields.Boolean('Discontinued', default=False, help="If checked, the variant will not be sold in main company")
