{
    "name": "JS Product Code",
    "summary": "Modifica el comportamiento de la referencia interna",
    "version": "11.0.1.0",
    "license": "AGPL-3",
    "author": "Jim Sports",
    "category": "Product",
    "website": "https://jimsports.com",
    "depends": ["product"],
    "data": [
        "views/product_view.xml"
    ],
    "post_init_hook": 'init_template_code',
    "uninstall_hook": 'restore_default_code',
    "installable": True,
}
