# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

# PLP - Movido método batch_update a controlador para poder llamarlo por URL
class jsFillProductController(http.Controller):
    @http.route([
        '/js_fill_product/',
        '/js_fill_product/<int:plimit>']
    , type='http', auth='user')
    def index(self, plimit=0, **kw):
        # Solo pueden acceder usuarios con permisos de configuración (Administración/Ajustes)
        if request.env.user.has_group('base.group_system'):

            # Creamos una lista para guardar los valores
            debug_processed = []

            # Hacemos uso de request para acceder al modelo de los productos
            product_list = request.env['product.template'].sudo().search([
                ('sale_ok', '=', True),
                ('default_code', '!=', False),
                ('type', '=', 'product')
            ], order='name', limit=plimit )

            # Realizamos un bucle para descargar las imágenes y guardar los resultados
            for product in product_list:
                product_ref = product.default_code.strip()

                debug_processed.append({
                    'reference': product_ref,
                    'name': product.name,
                    'images': product.js_download_images()
                })

            # Pasamos los resultados a la vista
            return request.render('js_fill_product.js_fill_product_batch', {
                'total': len(product_list),
                'products': debug_processed
            })

        else:
            return 'No está autorizado para acceder a esta página'
