# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class jsUpdatePrices(http.Controller):
    @http.route([
        '/js_update_prices'
    ], type='http', auth='user')
    def index(self, **kw):
        return request.render('js_update_prices.prices_edit_index')

    @http.route([
        '/js_update_prices/run'
    ], type='http', auth='user')
    def run(self, otype='sale.order', order='', tmode=0, **kw):

        # Solo pueden acceder usuarios con permisos de configuración (Administración/Ajustes)
        if request.env.user.has_group('base.group_system'):

            numLines = 0 # Contador para numero de líneas
            test_mode = int(tmode) # Test mode como entero (0-1)
            debug_processed = [] # Creamos una lista para guardar los valores

            # Hacemos uso de request para acceder al modelo de los pedidos
            if (order != ''):
                orders = request.env[otype].sudo().search([
                    ('name', '=', order)
                ], order='id')
            else:
                orders = request.env[otype].sudo().search([
                    ('state', '=', 'draft')
                ], order='id')

            #import web_pdb; web_pdb.set_trace()

            # Realizamos un bucle para recorrer los pedidos
            for order in orders:

                # Realizamos un bucle para recorrer las lineas del pedido
                for line in order.order_line:

                    numLines += 1

                    # Órdenes de venta
                    if otype == 'sale.order':

                        # TODO
                        debug_processed.append({
                            'id': line.id,
                            'name': line.name,
                            'quantity': line.product_qty,
                            'old_price': line.price_unit,
                            'new_price': line.price_unit
                        })

                    # Órdenes de compra
                    if otype == 'purchase.order':

                        # Buscamos los precios de compra
                        supplier_prices = request.env['product.supplierinfo'].sudo().search([
                            ('company_id', '=', line.company_id.id),
                            ('product_id', '=', line.product_id.id)
                        ], order='sequence')

                        # Si existe un precio en la tarifa lo actualizamos si la linea está como borrador
                        if (line.state == 'draft' and len(supplier_prices) > 0):

                            old_price = line.price_unit
                            price_unit = supplier_prices[0].price
                            price_subtotal = price_unit * line.product_qty
                            price_total = price_subtotal

                            if (line.price_unit != price_unit):

                                # Si no estamos en modo test
                                if not test_mode:

                                    # Actualizamos el precio
                                    line.write({
                                        'price_unit': price_unit,
                                        'price_subtotal': price_subtotal,
                                        'price_total': price_total
                                    })

                                # Guardamos la linea en el listado
                                debug_processed.append({
                                    'id': line.id,
                                    'name': line.name,
                                    'quantity': line.product_qty,
                                    'old_price': old_price,
                                    'new_price': price_unit
                                })

            # Pasamos los resultados a la vista
            return request.render('js_update_prices.prices_edit_batch', {
                'total': numLines,
                'total_changes': len(debug_processed),
                'products': debug_processed,
                'test_mode': test_mode
            })

        else:
            return 'No está autorizado para acceder a esta página'
