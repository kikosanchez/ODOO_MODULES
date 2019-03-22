{
    "name": "Valued Picking Report",
    "summary": "Adding Valued Picking on Delivery Slip report",
    "version": "11.0.1.0.0",
    "author": "Jim Sports Technology",
    "category": "Warehouse Management",
    "license": "AGPL-3",
    "depends": [
        "base",
        "sale",
        "sale_management",
        "stock",
        "delivery",
        "account",
    ],
    "data": [
        'views/res_partner_view.xml',
        'views/stock_picking_valued_view.xml',
        'views/stock_picking_valued_reports.xml',
    ],
    "installable": True,
}
