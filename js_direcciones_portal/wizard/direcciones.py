# import logging
# from odoo.tools.translate import _
# from odoo.tools import email_split
# from odoo.exceptions import UserError
from odoo import api, models, fields
# _logger = logging.getLogger(__name__)

# from odoo import models, api
# from odoo.addons.portal.wizard.portal_wizard import PortalWizard

# Override /addons/portal/wizard/portal_wizard.py > onchange_portal_id
class Direcciones(models.TransientModel):

    _inherit = 'portal.wizard'

    # Hacer que sólo aparezca el contacto padre en el listado de Acceso al Portal
    @api.onchange('portal_id')
    def onchange_portal_id(self):
        # for each partner, determine corresponding portal.wizard.user records
        partner_ids = self.env.context.get('active_ids', [])
        contact_ids = set()
        user_changes = []
        for partner in self.env['res.partner'].sudo().browse(partner_ids):            
            # Aquí se decide cuales son los partners que aparecen en el listado.
            contact_partners = [partner] # así estaba antes: contact_partners = partner.child_ids or [partner]
            for contact in contact_partners:
                # make sure that each contact appears at most once in the list
                if contact.id not in contact_ids:
                    contact_ids.add(contact.id)
                    in_portal = False
                    if contact.user_ids:
                        in_portal = self.portal_id in contact.user_ids[0].groups_id
                    user_changes.append((0, 0, {
                        'partner_id': contact.id,
                        'email': contact.email,
                        'in_portal': in_portal,
                    }))
        self.user_ids = user_changes
