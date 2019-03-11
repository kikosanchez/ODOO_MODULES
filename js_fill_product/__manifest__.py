# -*- coding: utf-8 -*-
# © 2018 Miguel Ángel García <info@miguel-angel-garcia.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#
{
    'name': "js_fill_product",

    'summary': """Descarga de imágenes de productos""",

    'description': """
        Descarga automática de las imágenes de productos
        desde el servidor de Jim Sports.

        08/03/2019 Modificado para que también funcione con
        las referencias de variantes, cogiendo la parte anterior
        al primer punto de la referencia.
    """,

    'author': "Miguel Ángel García",
    'website': "http://miguel-angel-garcia.com",
    'category': 'Administration',
    'version': '0.2',
    'depends': ['base', 'product', 'website_sale'],
    'external_dependencies': {'python' : ['urllib', 'base64']},
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
