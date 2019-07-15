from odoo import models, api
from odoo.addons.portal.wizard.portal_wizard import PortalWizard

class JSPortalWizard(PortalWizard):

    @api.onchange('portal_id')
    def onchange_portal_id(self):
        # for each partner, determine corresponding portal.wizard.user records
        partner_ids = self.env.context.get('active_ids', [])
        contact_ids = set()
        user_changes = []
        for partner in self.env['res.partner'].sudo().browse(partner_ids):
            # contact_partners = partner.child_ids + partner if partner.child_ids else partner
            contact_partners = partner.child_ids or [partner]
            for contact in contact_partners:
                if contact.type != 'delivery':
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