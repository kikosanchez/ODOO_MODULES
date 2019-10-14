from odoo import api, fields, models, tools
from odoo.http import request

class DireccionesWebsite(models.Model):
    _inherit = 'website'

    ##############################################################################################################    
    # Esta función sólo se ejecuta cuando NO hay un pedido activo (aunque sea un presupuesto vacío, sin artículos)
    # En las pruebas tenía que ir a borrarlo en el backend cada vez
    @api.multi
    def _prepare_sale_order_values(self, partner, pricelist):
        self.ensure_one()
        affiliate_id = request.session.get('affiliate_id')
        salesperson_id = affiliate_id if self.env['res.users'].sudo().browse(affiliate_id).exists() else request.website.salesperson_id.id
        addr = partner.address_get(['delivery', 'invoice'])
        default_user_id = partner.parent_id.user_id.id or partner.user_id.id
        values = {
            'partner_id': partner.id,
            'pricelist_id': pricelist.id,
            'payment_term_id': self.sale_get_payment_term(partner),
            'team_id': self.salesteam_id.id or partner.parent_id.team_id.id or partner.team_id.id,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
            'user_id': salesperson_id or self.salesperson_id.id or default_user_id,
        }

        ############################################################################################################
        # comprobar si el padre tiene algún hijo que sea dirección de facturación y asignarlo a 'partner_invoice_id'
        if partner.child_ids:
            for hijo in partner.child_ids:
                if hijo.type == 'invoice':
                    values['partner_invoice_id'] = hijo.id
        
        company = self.company_id or pricelist.company_id
        if company:
            values['company_id'] = company.id

        return values