# -*- encoding: utf-8 -*-

{
    'name':'JS Vimenpaq Delivery',
    'summary': 'Personalización de envío para Vimenpaq',
    'website': 'https://www.jimsports.com',
    'description': 'Gestiona las sucursales de Vimenpaq y permite al cliente seleccionar una para el envío',
    'version':'1.0',
    'author':'Jim Sports',
    'data': [
        'security/ir.model.access.csv',
        'views/layout.xml'
    ],
    'category': 'Website',
    'depends': ['website', 'website_sale', 'website_sale_delivery'],
    'installable': True,
}
