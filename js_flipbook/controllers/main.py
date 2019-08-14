from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm

class FlipbookCatalogue(http.Controller):
    @http.route('/catalogue', auth="public", website=True)
    def flipbook_catalogue(self, **kwargs):
        return request.render('js_flipbook.jim_flipbook_catalogo')