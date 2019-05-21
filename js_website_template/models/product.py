from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    website_price_min = fields.Float('Website Min Price', compute='_website_price', store=False)
    website_price_max = fields.Float('Website Max Price', compute='_website_price', store=False)

    def _website_price(self):
        # Llamar al método sobreescrito
        super(ProductTemplate, self)._website_price()

        for template in self:
            # Para guardar los precios
            product_prices = []

            # Precio de la plantilla
            if (template.sale_ok and template.website_price > 0):
                product_prices.append(template.website_price);

            # Precio de las variantes
            # Se necesita usar sudo() para el visitante anónimo
            for p in template.sudo().product_variant_ids:
                # Obtener el precio de cada variante si es mayor que 0, tiene stock y se puede comprar
                if (p.sale_ok and (p.inventory_availability == "always" or p.inventory_availability == "threshold") and p.qty_available > 0 and p.website_price > 0):
                    product_prices.append(p.website_price)

            # Obtenemos el precio más bajo y el más alto
            template.website_price_min = min(product_prices) if len(product_prices) else 0.00
            template.website_price_max = max(product_prices) if len(product_prices) else 0.00
