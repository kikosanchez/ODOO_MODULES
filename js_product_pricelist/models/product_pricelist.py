from odoo import api, fields, models

class CustomProductTemplate(models.Model):
    _inherit = "product.template"

    item_ids = fields.One2many('product.pricelist.item', 'product_tmpl_id', 'Pricelist Items')

    # Si es una plantilla no se aplica el precio a la variante, pero debemos pasarlo igualmente a ala vista a 0
    def _default_variant_applied(self):
        for record in self:
            record.default_variant_applied = 0

    default_variant_applied = fields.Integer(compute='_default_variant_applied')

class CustomProduct(models.Model):
    _inherit = "product.product"

    item_ids = fields.One2many('product.pricelist.item', 'product_id', 'Pricelist Items')

    # Si es una variante pasamos el id de la misma a la vista para guardar el precio como variante
    def _default_variant_applied(self):
        for record in self:
            record.default_variant_applied = record.id

    default_variant_applied = fields.Integer(compute='_default_variant_applied')

class CustomPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    @api.model
    def create(self, vals):
        # Si se establece un id de variante eliminamos el del producto que se pone por defecto en la plantilla
        if ('product_id' in vals and 'product_tmpl_id' in vals and vals['product_id']):
            del vals['product_tmpl_id']
        return super(CustomPricelistItem, self).create(vals)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.applied_on = '0_product_variant'
        else:
            self.applied_on = '1_product'
