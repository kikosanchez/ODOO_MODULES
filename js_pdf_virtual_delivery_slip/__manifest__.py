# -*- encoding: utf-8 -*-

{
  'name':'JS PDF Virtual Delivery Slip',
  'summary': 'Permite imprimir un PDF simulando un albarán usando los datos del pedido',
  'description': 'La opción de imprimir el PDF está en el pedido. No se crea ningún albarán, sólo se imprime un PDF con los datos de productos entregados en las líneas de pedido',
  'version':'1.0',
  'author':'Jim Sports',
  'data': [
    'views/pdf_virtual_delivery_slip_view.xml',
    'views/pdf_virtual_delivery_slip_report.xml',
  ],
  'category': 'Advanced Reporting',
  'depends': ['base', 'delivery', 'stock', 'sale', 'purchase', 'account'],
}
