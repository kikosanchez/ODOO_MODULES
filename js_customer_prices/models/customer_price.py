# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError
import time

class CustomerPrice(models.Model):
    _name = 'customer.price'

    product_tmpl_id = fields.Many2one('product.template', 'Template', index=1)
    product_id = fields.Many2one('product.product', 'Product', index=1)
    partner_id = fields.Many2one('res.partner', 'Customer', required=True, index=1)
    min_qty = fields.Float('Min Quantity', default=1.0, required=True)
    price = fields.Float('Price', default=0.0, digits=dp.get_precision('Product Price'), required=True, help="The price to purchase a product")
    date_start = fields.Date('Start Date', index=1, help="Start date for this customer price")
    date_end = fields.Date('End Date', index=1, help="End date for this customer price")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1)

    @api.depends('date_end')
    @api.onchange('partner_id', 'product_tmpl_id', 'product_id', 'min_qty', 'price')
    def _onchange_any_field(self):
        # Para no permitir elegir las 2 cosas
        # cuando tenemos una plantilla seleccionada 
        # la variante se bloquea y viceversa
        if self.product_tmpl_id:
            self.product_id = False
        if self.product_id:
            self.product_tmpl_id = False
        # Comprobar que el precio no sea mayor que el de la lista de precios del cliente
        pricelist = self.partner_id.property_product_pricelist
        product = self.product_tmpl_id or self.product_id
        currency = pricelist.currency_id.symbol
        if self.partner_id and pricelist and product and self.min_qty and self.price:
            # No podemos obtener el precio del producto con cantidad 0, sin embargo si que funciona para la cantidad 0.1
            product_list_price = pricelist.get_product_price(product, self.min_qty or 1, self.partner_id, self.date_end or False)
            if self.price >= product_list_price:
                # Convertir precio a string con la moneda
                product_list_price = str(product_list_price) + currency if pricelist.currency_id.position == 'after' else currency + str(product_list_price)
                # Devolver una alerta con la información
                return {
                    'warning': {
                        'title': _('Warning, check this!'),
                        'message': _('Customer price is higher or equal than the one assigned on its pricelist\nActual price on %s is: %s') % (pricelist.name, product_list_price)
                    }
                }

    @api.model
    def _get_partner_parents_ids(self, partner, parents=[]):
        # Buscar recursivamente los padres
        # de un contacto
        while partner.parent_id:
            partner = partner.parent_id
            parents.append(partner.id)
        return parents

    @api.model
    def _check_price_obj(self, values):
        # Si ya existe esta combianción de plantilla/variante/cliente no lo creamos
        if self.env['customer.price'].search([
            ('product_tmpl_id', '=', values.get('product_tmpl_id', False)), 
            ('product_id', '=', values.get('product_id', False)), 
            ('partner_id', '=', values.get('partner_id', False))
        ]):
            raise ValidationError(_('Product/variant must be unique in customer pricelist!'))

    @api.model
    def get_price_obj(self, partner_id, product_id, min_qty, date=False, product_key='product_id'):
        # Si no se pasa una fecha límite es la actual
        date_end = date or time.strftime("%Y-%m-%d")
        # Buscamos y devolvemos la instancia
        return self.env['customer.price'].search([
            # Polish notation query
            '&','&','&','&',
            ('partner_id', '=', partner_id),
            (product_key, '=', product_id),
            ('min_qty', '<=', min_qty),
            '|',
            ('date_start', '=', False),
            ('date_start', '<=', date_end),
            '|',
            ('date_end', '=', False),
            ('date_end', '>=', date_end)
        ], limit=1, order='min_qty DESC')

    @api.model
    def get_customer_price(self, partner, product, qty, date=False):
        # Si no se recibe una instancia de un models.Model (un objeto)
        # mejor pasar la instancia si podemos para evitar una segunda llamada a la BBDD
        if not isinstance(partner, models.Model):
            # Obtenemos la instancia del cliente
            partner = self.env['res.partner'].sudo().browse(partner)

        # Establecemos un listado con los ID de clientes donde buscaremos los precios
        clients_to_search = self._get_partner_parents_ids(partner, [partner.id])

        # Buscar precio para los contactos, si lo encontramos en el hijo ya no buscamos en el/los padre/s
        for client in clients_to_search:
            # Buscamos el precio específico en el producto
            customer_price = self.get_price_obj(client, product.id, qty, date, 'product_id')

            # Buscamos el precio específico en la plantilla
            if not customer_price:
                customer_price = self.get_price_obj(client, product.product_tmpl_id.id, qty, date, 'product_tmpl_id')

            # Si hay un precio lo devolvemos
            if customer_price:
                return customer_price.price

        # Si no hay precio se devuelve 0.0 para no
        # cambiar el tipo de datos, a efectos prácticos
        # se puede interpretar como un False
        return 0.0

    @api.model
    def create(self, values):
        self._check_price_obj(values)
        return super(CustomerPrice, self).create(values)

    @api.multi
    def write(self, values):
        self._check_price_obj(values)
        return super(CustomerPrice, self).write(values)