# -*- coding: utf-8 -*-
#from odoo import http, tools, _
#from odoo.addons.website_sale.controllers.main import WebsiteSale

#class MyWebsiteSale(WebsiteSale):
#    @http.route([
#        '/shop',
#        '/shop/page/<int:page>',
#        '/shop/category/<model("product.public.category"):category>',
#        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
#    ], type='http', auth="public", website=True)
#    def shop(self, page=0, category=None, search='', ppg=False, **post):
#        post['paginate_scope'] = 5 #Necesario incorporar esta variable en website_sale\controllers\main.py linea 258 para el parametro 'scope'
#        return super(MyWebsiteSale, self).shop(page, category, search, ppg, **post)
