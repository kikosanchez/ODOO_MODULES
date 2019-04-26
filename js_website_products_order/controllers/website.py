# -*- coding: utf-8 -*-
from odoo import http, tools, _
from odoo.addons.website_sale.controllers.main import WebsiteSale

class JsProductsOrderWebsiteSale(WebsiteSale):

    def _get_search_order(self, post):
        if not post.get('order'):
            return 'website_published desc, featured_product desc, sequence asc, id desc'
        return 'website_published desc,%s , id desc' % post.get('order', 'website_sequence desc')
