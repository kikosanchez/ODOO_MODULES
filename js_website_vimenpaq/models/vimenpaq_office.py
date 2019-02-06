# -*- coding: utf-8 -*-
from odoo import models, fields

class VimenpaqOffice(models.Model):
    _name = 'js_website_vimenpaq.office'
    _description = "Vimenpaq destination"
    _order = 'sequence, id'

    sequence = fields.Integer(help="Determine the display order", default=10)
    name = fields.Char(required=True, translate=False)
    active = fields.Boolean(default=True)
    schedule = fields.Text(string='Schedule')
    phone = fields.Char('Phone')
    address = fields.Text(string='Address')
    city = fields.Char('City')
