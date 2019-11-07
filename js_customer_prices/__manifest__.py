# -*- coding: utf-8 -*-
{
    'name': 'JS Customer Prices',
    'version': '11.0.2.0.0',
    'category': 'Sale',
    'license': 'AGPL-3',

    # Dependencies
    'depends': [
        'product',
        'sale',
        'website_sale'
    ],

    # Security & Views
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/customer_price.xml',
        'views/res_partner.xml',
        'views/product.xml',
        'views/website.xml',
        'views/sale.xml'
    ],

    # Odoo Store
    # 'live_test_url': 'https://jimsports.com',
    # 'images': [
    #     'static/description/main_poster.jpg',
    #     'static/description/main_screenshot.jpg'
    # ],

    # Author
    'author': 'Jim Sports Technology S.L.',
    'website': 'https://jimsports.com',
    'maintainer': 'Jim Sports',

    # Technical
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 49.99,
    'currency': 'EUR'
}
