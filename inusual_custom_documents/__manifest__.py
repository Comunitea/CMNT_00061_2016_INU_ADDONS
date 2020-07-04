# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Inusual Custom Documents',
    'version': '12.0.1.0.0',
    'author': 'Comunitea ',
    "category": "Custom",
    'license': 'AGPL-3',
    'depends': [
        'stock_picking_report_valued',
        'intrastat_product',
        'mrp',
        'account',
        'purchase_stock',
        'repair',
        'account_invoice_report_due_list'
    ],
    'contributors': [
        "Comunitea: ",
        "Javier Colmenero <javier@comunitea.com>, "
        "Omar Castiñeira Saavedra <omar@comunitea.com>"
    ],
    "data": [
        "views/report_invoice.xml",
        "views/report_stockpicking.xml",
        "views/layouts.xml",
        "views/manufacturing_order.xml",
        "views/stock_picking.xml",
        "views/report_saleorder.xml",
        'views/account_invoice.xml',
        'views/report_repair.xml',
        'views/repair_view.xml'
    ],
    "installable": True
}
