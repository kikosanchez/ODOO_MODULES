# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class jsProductPricelist(http.Controller):
    @http.route([
        '/js_product_pricelist/',
        '/js_product_pricelist/<int:plimit>']
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

                # Si no tiene variantes
                if (len(product.product_variant_ids) < 2):

                    # Buscamos los precios
                    prices_list = request.env['product.pricelist.item'].sudo().search([
                        ('product_id', '=', product.product_variant_ids[0].id)
                    ])

                    # Actualizamos los precios
                    for price_item in prices_list:
                        price_item.write({'applied_on':'1_product', 'product_id':None, 'product_tmpl_id':product.id})

                    # Sacamos la información de los productos actualizados
                    debug_processed.append({
                        'reference': product_ref,
                        'name': product.name
                    })

            # Pasamos los resultados a la vista
            return request.render('js_product_pricelist.pricelist_edit_batch', {
                'total': len(product_list),
                'products': debug_processed
            })

        else:
            return 'No está autorizado para acceder a esta página'
