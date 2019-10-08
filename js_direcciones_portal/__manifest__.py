{
    "name": "JS Direcciones en Portal",
    "summary": "Cambia el comportamiento del portal de Odoo: la asignación y las direcciones",
        'description': """
1. Sólo la empresa padre aparece en el listado de dar acceso al portal. Sin este módulo el contacto padre nunca aparece en caso de tener contactos hijos.
2. Cada empresa solo debe tener 1 dirección de facturación. Este módulo impide que se guarde más de una dirección de facturación al crearla.
3. Al guardar un contacto por vez primera, se genera una dirección de facturación con los datos del padre. Es posible crear una dirección de facturación con datos distintos si la creamos y guardamos el contacto padre al mismo tiempo. No se crea automáticamente si ya hay previamente creado un contacto hijo porque el condicional child_ids == 0 no comprueba de que tipo son los hijos. De todas formas siempre se puede editar esta única dirección de facturación.
4. En las ventas web, Odoo siempre asigna como dirección de facturación al parent_id, contacto padre. Da igual que tenga un contacto hijo que sea Dirección de facturación; lo ignora. Para que se asigne un hijo de tipo Dirección de Facturación (si lo tiene) se hace un override de la función _prepare_sale_order_values(). Esta función sólo se ejecuta al principio, cuando el cliente web no tiene ningún pedido activo; un pedido vacío sin artículos (como un carrito abandonado) también es un pedido activo.
""",
    "version": "1.0",
    "license": "AGPL-3",
    "author": "Jim Sports",
    "category": "Uncategorized",
    "website": "https://jimsports.com",
    'data': [
        'views/direcciones_checkout.xml',
    ],
    'depends': ['website', 'website_sale', 'portal'],
}