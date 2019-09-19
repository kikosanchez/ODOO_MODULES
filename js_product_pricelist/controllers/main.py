# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class jsProductPricelist(http.Controller):
    @http.route([
        '/js_product_pricelist'
    ], type='http', auth='user')
    def index(self, **kw):
        return request.render('js_product_pricelist.pricelist_edit_index')

    @http.route([
        '/js_product_pricelist/run'
    ], type='http', auth='user')
    def run(self, plimit=0, tmode=0, **kw):

        # Solo pueden acceder usuarios con permisos de configuración (Administración/Ajustes)
        if request.env.user.has_group('base.group_system'):

            product_limit = int(plimit) # Limite de productos como entero
            test_mode = int(tmode) # Test mode como entero (0-1)
            debug_processed = [] # Creamos una lista para guardar los valores

            # Hacemos uso de request para acceder al modelo de los productos
            product_list = request.env['product.template'].sudo().search([
                ('sale_ok', '=', True),
                ('default_code', '!=', False),
                ('type', '=', 'product')
            ], order='name')

            # Realizamos un bucle para recorrer los productos
            for product in product_list:

                # Si no tiene variantes
                if (len(product.product_variant_ids) < 2):

                    # Buscamos los precios
                    prices_list = request.env['product.pricelist.item'].sudo().search([
                        ('product_id', '=', product.product_variant_ids[0].id)
                    ])

                    # Si no estamos en modo test
                    if not test_mode:
                        # Actualizamos los precios
                        for price_item in prices_list:
                            price_item.write({
                                'applied_on': '1_product',
                                'product_id': None,
                                'product_tmpl_id': product.id
                            })

                    # Sacamos la información de los productos
                    debug_processed.append({
                        'id': product.id,
                        'reference': product.default_code.strip(),
                        'name': product.name,
                        'prices_modified': len(prices_list)
                    })

                    # Si llegamos al límite de productos establecido salimos del bucle
                    if (product_limit > 0 and len(debug_processed) >= product_limit):
                        break

            # Pasamos los resultados a la vista
            return request.render('js_product_pricelist.pricelist_edit_batch', {
                'total': len(debug_processed),
                'products': debug_processed
            })

        else:
            return 'No está autorizado para acceder a esta página'
