# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    valued_picking = fields.Boolean(
        default=True,
        help='You can select which partners have valued pickings',
    )
