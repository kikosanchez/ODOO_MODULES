{
    'name': 'JS Custom Template',
    'summary': 'Cambios genéricos en plantilla Clarico y otras personalizaciones de Odoo',
    'description': 'Modifica el tema Clarico y añade funcionalidades extra en la tienda de Odoo para la República Dominicana.',
    'version': '11.0.2.0',
    'license': 'AGPL-3',
    'author': 'Jim Sports',
    'website': 'https://jimsports.com',
    'data': [
        'views/assets.xml',
        'views/reports.xml',
        'data/ir_model_data.xml',
        'views/default_contact_form.xml',
        'views/shop_address.xml',
        'views/web_product.xml',
        'views/clarico_wishlist.xml',
        'views/filter_sort_by.xml',
        'views/clarico_cart.xml',
        'views/web_shop.xml'
        # 'views/web_signup.xml'
    ],
    'category': 'Website',
    'depends': ['account', 'website', 'website_sale', 'website_sale_options', 'clarico_contact', 'clarico_product',  'clarico_shop', 'clarico_wishlist', 'website_form_recaptcha'],
}
