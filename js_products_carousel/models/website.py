from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.http import request

class website(models.Model):

    _inherit = "website"

    clarico_header_style_one = fields.Char('Clarico Heading')
    clarico_header_style_two = fields.Char("Clarico Heading Style 2")
    clarico_header_style_three = fields.Char("Clarico Heading Style 3")

    def category_check(self,filter=[]):
        if filter:
            filter.extend([('website_published','=',True)])
        else:
            filter=([('website_published','=',True)])

        return self.env['product.public.category'].sudo().search(filter)

    def get_res_lang(self):
        current_lang= request.env.lang
        res_lang = self.env['res.lang'].search([('code','=',current_lang)])
        return res_lang
