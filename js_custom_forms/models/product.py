from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    website_price_min = fields.Float('Website Min Price', compute='_website_price', store=False)
    website_price_max = fields.Float('Website Max Price', compute='_website_price', store=False)

    def _website_price(self):
        # Llamar al método sobreescrito
        super(ProductTemplate, self)._website_price()

        for template in self:
            # Lista para guardar los precios
            product_prices = []

            # Precio de la plantilla
            if (template.sale_ok and template.website_price > 0):
                # Aquí se usa sudo para evitar discrepancias en el precio
                # entre un usuario logueado y anónimo (no debería hacer falta)
                product_prices.append(template.sudo().website_price)

            # Precio de las variantes
            # - se necesita usar sudo() para el visitante anónimo -
            for p in template.sudo().product_variant_ids:
                # Se puede vender, tiene precio y ...
                if (p.sale_ok and p.website_price > 0 and (
                        # Es un producto almacenable y ...
                        p.type == 'product' and (
                            # Se vende si hay stock
                            (p.inventory_availability == "always" and p.qty_available > 0)
                            # Se vende si el stock está por encima de un umbral
                            or (p.inventory_availability == "threshold" and p.qty_available > p.available_threshold)
                            # Se vende independientemente del stock
                            or (p.inventory_availability == "never" or p.inventory_availability == "custom")
                        )
                    ) or (
                        # No es un producto almacenable
                        (p.type == 'consu' or p.type == 'service')
                    )):
                    # Guardar en la lista el precio de la variante
                    product_prices.append(p.website_price)

            # Obtenemos el precio menor y el mayor de la lista
            template.website_price_min = min(product_prices) if len(product_prices) else 0.00
            template.website_price_max = max(product_prices) if len(product_prices) else 0.00