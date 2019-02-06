# -*- encoding: utf-8 -*-

{
    'name':'JS Products Carousel',
    'summary': 'Snippet para mostrar carousel de productos',
    'description': 'Crea un carousel de productos filtrándolos por etiquetas',
    'version':'1.0',
    'author':'Jim Sports',
    'data': [
        'security/ir.model.access.csv',
        'views/website_filter_ept_view.xml',
        'templates/assets.xml',
        'templates/ecommerce_product_carousel_snippet.xml',
        'templates/snippet_options.xml',
        'data/product_carousel.xml'
    ],
    'category': 'Website',
    'depends': ['website', 'website_sale'],
    'installable': True
}
