from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

class ProductTemplateProduct(models.Model):
    _inherit = 'product.template'

    # CAMPO AUXILIAR PARA GUARDAR EL DEFAULT_CODE
    template_code = fields.Char('Template Reference')
    # MODIFICAMOS LAS FUNCIONES INVERSE Y COMPUTED DEL DEFAULT CODE
    default_code = fields.Char('Internal Reference', compute='_compute_tmpl_dc', inverse='_set_tmpl_dc', store=True)
    # PARA PASAR A LA VISTA EL PARAMETRO DE CONFIGURACION
    default_code_required = fields.Boolean(default=False, store=False)

    @api.depends('product_variant_ids', 'product_variant_ids.default_code')
    def _compute_tmpl_dc(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.default_code = template.product_variant_ids.default_code
        for template in (self - unique_variants):
            template.default_code = template.template_code

    @api.one
    def _set_tmpl_dc(self):
        # CUANDO SE MODIFICA EL DEFAUL_CODE TAMBIÉN MODIFICAMOS EL TEMPLATE_CODE
        self.template_code = self.default_code
        # SI SOLO EXISTE UNA VARIANTE LE ASIGNAMOS EL CÓDIGO DE LA PLANTILLA
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.default_code = self.default_code

    @api.onchange('default_code')
    def _check_default_code(self):
        self.default_code_required = bool(self.env['ir.config_parameter'].get_param('js_product_code.required_code'))

        if self.default_code:
            self.default_code = self.default_code.strip()

        if self.default_code_required:
            default_code_exists = (self.default_code != self._origin.default_code and len(self.env['product.template'].search([
                ('default_code', '=', self.default_code)
            ])))

            if default_code_exists:
                self.default_code = None
                return {
                    'warning': {
                        'title': _("Warning"),
                        'message': _("Internal Reference must be unique for all products!")
                    }
                }

    @api.model
    def create(self, vals):
        defaultCodeIsRequired = bool(self.env['ir.config_parameter'].get_param('js_product_code.required_code'))
        #  SI EL CÓDIGO ES REQUERIDO PERO NO ESTÁ DEFINIDO O ES FALSE
        if defaultCodeIsRequired and (not hasattr(self, 'default_code') or (not self.default_code)):
            # AL CREAR UN PRODUCTO AL VUELO
            if self.env.context.get('create_product_product') and not self.env.context.get('default_name'):
                raise ValidationError(_('You can not create products from variants!'))
        return super(ProductTemplateProduct, self).create(vals)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.onchange('default_code')
    def _check_default_code(self):
        self.default_code_required = bool(self.env['ir.config_parameter'].get_param('js_product_code.required_code'))

        if self.default_code:
            self.default_code = self.default_code.strip()

        if self.default_code_required:
            default_code_exists = (self.default_code != self._origin.default_code and len(self.env['product.product'].search([
                ('default_code', '=', self.default_code)
            ])))

            if default_code_exists:
                self.default_code = None
                return {
                    'warning': {
                        'title': _("Warning"),
                        'message': _("Internal Reference must be unique for all variants!")
                    }
                }

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_required_code = fields.Selection(
        [
            (0, 'Not required'),
            (1, 'Required (unique)')
        ],
        string='Set product internal reference as unique',
        help='Set behaviour of codes (if you set as unique an internal reference value is required)'
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        res.update({
            'product_required_code': int(self.env['ir.config_parameter'].get_param('js_product_code.required_code'))
        })

        return res

    @api.one
    def set_values(self):
        self.env['ir.config_parameter'].set_param('js_product_code.required_code', int(self.product_required_code))
        super(ResConfigSettings, self).set_values()
