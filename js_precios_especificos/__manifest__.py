# © 2019 Jim Sports
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'JS Precio Específicos',
    'version': '11.0.1.0.0',
    'author': 'Jim Sports',
    "category": "Custom",
    'license': 'AGPL-3',
    'depends': [
        'product',
        'sale',
    ],
    'contributors': [
        "Jim Sports <info@jimsports.com>",
    ],
    "data": [        
        'security/ir.model.access.csv',
        'views/customer_price.xml',
        'views/product_view.xml',
        'views/res_partner_view.xml',
        'security/js_sale_security.xml',
    ],
}