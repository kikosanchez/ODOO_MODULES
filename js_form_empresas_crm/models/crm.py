from odoo import api, fields, models

class CrmTemplate(models.Model):
    _inherit = 'crm.lead'
    
    siret = fields.Char(string='SIRET')

    TIPOS_EMPRESA = [('magasin', 'Magasin'), ('club', 'Club, association ou collectif'), ('autre', 'Autre')]
    tipo_empresa = fields.Selection(TIPOS_EMPRESA, string='Company class', default='autre')    
    
    vat_number = fields.Char(string='Numéro de TVA')