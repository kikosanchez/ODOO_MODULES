# -*- encoding: utf-8 -*-

{
  'name':'JS Custom Template',
  'summary': 'Módulo para mantener los cambios CSS y plantillas HTML',
  'description': 'Introduce modificaciones en el tema activo (recomedado Default) y añade funcionalidades extra en la tienda de Odoo.',
  'version':'1.0',
  'author':'Jim Sports',
  'data': [
    'views/pdfs.xml',
    'views/main.xml',
    'views/cart.xml',
    'views/shop.xml',
    'views/footer.xml'

  ],
  'category': 'Website',
  'depends': ['website', 'website_sale'],
}
