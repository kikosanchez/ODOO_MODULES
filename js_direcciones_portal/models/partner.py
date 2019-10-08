# import base64
# import datetime
# import hashlib
# import pytz
import threading

# from email.utils import formataddr

# import requests
# from lxml import etree
# from werkzeug import urls

from odoo import api, fields, models, tools, _
from odoo.modules import get_module_resource
# from odoo.osv.expression import get_unaccent_wrapper
# from odoo.exceptions import UserError, ValidationError

class DireccionesPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _handle_first_contact_creation(self):
        """ On creation of first contact for a company (or root) that has no address, assume contact address
        was meant to be company address """
        parent = self.parent_id
        address_fields = self._address_fields()

        if (parent.is_company or not parent.parent_id) and len(parent.child_ids) == 1 and any(self[f] for f in address_fields) and not any(parent[f] for f in address_fields):
            addr_vals = self._update_fields_values(address_fields)
            parent.update_address(addr_vals)

        ##############################################################################################
        # Generar automáticamante una dirección de facturación al momento de guardar el contacto empresa
        if(self.is_company and len(self.child_ids) == 0):
            invoice_address = parent.create({
                'is_company'    : False,
                'type'          : 'invoice',
                'name'          : self.name,
                'display_name'  : self.display_name,
                'street'        : self.street,
                'street2'       : self.street2,
                'city'          : self.city,
                'state_id'      : self.state_id.id,
                'zip'           : self.zip,
                'country_id'    : self.country_id.id,
                'phone'         : self.phone,
                'mobile'        : self.mobile,
                'email'         : self.email,
                'parent_id'     : self.id,
            })

    @api.model
    def create(self, vals):
        ##############################################################
        # no ejecutar si es invoice y ya hay otras direcciones invoice
        hijos = self.env['res.partner'].browse([vals.get('parent_id')]).child_ids
        for hijo in hijos:
            if vals.get('type') == 'invoice' and hijo.type == 'invoice':
                return

        if vals.get('website'):
            vals['website'] = self._clean_website(vals['website'])
        if vals.get('parent_id'):
            vals['company_name'] = False
        # compute default image in create, because computing gravatar in the onchange
        # cannot be easily performed if default images are in the way
        if not vals.get('image'):
            vals['image'] = self._get_default_image(vals.get('type'), vals.get('is_company'), vals.get('parent_id'))
        tools.image_resize_images(vals)
        
        partner = super(DireccionesPartner, self).create(vals)
        partner._fields_sync(vals)
        partner._handle_first_contact_creation()
        return partner
