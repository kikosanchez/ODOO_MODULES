# -*- coding: utf-8 -*-
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class JsWebTemplateWebsiteSale(WebsiteSale):
    # Para corregir problema al mostrar el precio del producto
    # https://trello.com/c/EtrtWRyi/72-odoo-modifica-el-precio-del-producto-al-a%C3%B1adir-o-quitar-unidades-en-el-sitio-web
    @http.route(['/shop/get_unit_price'], type='json', auth="public", methods=['POST'], website=True)
    def get_unit_price(self, product_ids, add_qty, **kw):
        products = request.env['product.product'].with_context({'quantity': add_qty}).browse(product_ids)
        # return {product.id: product.website_price / add_qty for product in products}
        return {product.id: product.website_price for product in products}

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
