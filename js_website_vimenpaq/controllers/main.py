# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import base64
import os

# Heredamos el método WebsiteSale para sobreescribir el checkout
class VimenpaqOfficesController(WebsiteSale):

    # SOBREESCRIBIMOS MÉTODO checkout()
    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        vimenpaq_offices = request.env['js_website_vimenpaq.office']
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)

        if redirection:
            return redirection

        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            return request.redirect('/shop/address')

        for f in self._get_mandatory_billing_fields():
            if not order.partner_id[f]:
                return request.redirect('/shop/address?partner_id=%d' % order.partner_id.id)

        if redirection:
            return redirection

        # Si hay una dirección de envío asignada comprobamos si coincide
        # con una de Vimenpaq para auto-seleccionarla
        if order.partner_shipping_id:
            Partner = request.env['res.partner']
            partner_name = Partner.browse(order.partner_shipping_id.id).sudo().name
            found_vimenpaq_partner = vimenpaq_offices.search([('name', '=', partner_name)])

        values = self.checkout_values(**post)

        #values.update({'website_sale_order': order})

        # INCLUIMOS NUEVOS DATOS CON EL UPDATE
        values.update({
            'website_sale_order': order,
            # Incluimos en el diccionario todas las oficinas de Vimenpaq activas
            'offices': vimenpaq_offices.search([('active', '=', True)]),
            # Si ya está asignada una dirección de Vimenpaq guardamos el id para que aparezca auto-seleccionada en el <select>
            'selected_office_id': found_vimenpaq_partner.id if found_vimenpaq_partner else None,
            # Ocultar la dirección de envío si no es una compañía y mostrar Vimenpaq
            'only_services': order.partner_id.company_type != "company" or False
        })

        # Avoid useless rendering if called in ajax
        if post.get('xhr'):
            return 'ok'

        return request.render("website_sale.checkout", values)

    # NUEVO MÉTODO
    @http.route(['/shop/vimenpaq'], type='http', auth="public", website=True)
    def vimenpaq(self, **post):
        order = request.website.sale_get_order()

        if post and post.get('office'):
            Partner = request.env['res.partner'].sudo()
            selected_office_id = post.get('office');
            vimenpaq_offices = request.env['js_website_vimenpaq.office']
            selected_office = vimenpaq_offices.browse(int(selected_office_id))

            # Buscamos si existe el partner Vimenpaq (activo o archivado)
            vimenpaq_partner_id = Partner.sudo().with_context(active_test=False).search([
                ('type', '=', 'other'),
                ('parent_id', '=', None),
                ('name', '=', 'VIMENPAQ')
            ]).id

            if not vimenpaq_partner_id:
                # Si no existe el cliente VIMENPAQ se crea
                vimenpaq_module_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
                with open(os.path.join(vimenpaq_module_path, 'static', 'img', 'icon.png'), 'rb') as image_logo:
                    vimenpaq_partner_id = Partner.create({
                        'customer': True,
                        'parent_id': None,
                        'team_id': request.website.salesteam_id and request.website.salesteam_id.id,
                        'image': base64.encodestring(image_logo.read()),
                        'type': 'other',
                        'name': 'VIMENPAQ',
                        'phone': '(809) 532-7388',
                        'street': 'Av. Enrique Jimenez Moya No. 9 esq. Bolivar. La Julia',
                        'city': 'Santo Domingo',
                        'country_id': 61, #Rep. Dominicana
                        'active': True
                    }).id

            # Buscamos si la dirección ya está creada
            address_id = Partner.search([
                ('type', '=', 'delivery'),
                ('parent_id', '=', vimenpaq_partner_id),
                ('name', '=', selected_office.name)
            ]).id

            if address_id: # Si la dirección existe guardamos su id
                order.partner_shipping_id = address_id
            else: # Si no lo hay la creamos y asignamos
                order.partner_shipping_id = Partner.create({
                    'customer': True,
                    'parent_id': vimenpaq_partner_id,
                    'team_id': request.website.salesteam_id and request.website.salesteam_id.id,
                    'type': 'delivery',
                    'name': selected_office.name,
                    'phone': selected_office.phone,
                    'street': selected_office.address,
                    'city': selected_office.city,
                    'country_id': 61, #Rep. Dominicana
                    'active': True
                }).id

            return request.redirect('/shop/payment')

        else:
            return request.redirect('/shop/checkout')

    # SOBREESCRIBIMOS MÉTODO payment_validate()
    @http.route('/shop/payment/validate', type='http', auth="public", website=True)
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        if transaction_id is None:
            tx = request.website.sale_get_transaction()
        else:
            tx = request.env['payment.transaction'].browse(transaction_id)

        if sale_order_id is None:
            order = request.website.sale_get_order()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')

        if not order or (order.amount_total and not tx):
            return request.redirect('/shop')

        if (not order.amount_total and not tx) or tx.state in ['pending', 'done', 'authorized']:
            if (not order.amount_total and not tx):
                # Orders are confirmed by payment transactions, but there is none for free orders,
                # (e.g. free events), so confirm immediately
                order.with_context(send_email=True).action_confirm()
        elif tx and tx.state == 'cancel':
            # cancel the quotation
            order.action_cancel()

        # LOS DATOS DE LA SESIÓN SE ELIMINAN EN LA PÁGINA DE CONFIRMACIÓN
        # PARA PODER RECUPERAR EL PEDIDO Y MOSTRAR SU DATOS (DE OTRA FORMA PASA A LA PÁGINA /shop)

        # clean context and session, then redirect to the confirmation page
        #request.website.sale_reset()
        #if tx and tx.state == 'draft':
        #    return request.redirect('/shop')

        return request.redirect('/shop/confirmation')

    # SOBREESCRIBIMOS MÉTODO payment_confirmation()
    @http.route(['/shop/confirmation'], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):

        # RECUPERAMOS LOS DATOS DEL PEDIDO Y BORRAMOS LA SESIÓN
        order = request.website.sale_get_order()
        request.website.sale_reset()

        # MOSTRAMOS LOS DATOS DEL PEDIDO
        return request.render("website_sale.confirmation", {'order': order})

        #sale_order_id = request.session.get('sale_last_order_id')
        #if sale_order_id:
        #    order = request.env['sale.order'].sudo().browse(sale_order_id)
        #    return request.render("website_sale.confirmation", {'order': order})
        #else:
        #    return request.redirect('/shop')
