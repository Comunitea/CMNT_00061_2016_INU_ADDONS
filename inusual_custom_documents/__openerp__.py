# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Inusual Custom Documents',
    'version': '8.0.0.0.0',
    'author': 'Comunitea ',
    "category": "Custom",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'cmnt_custom_reports',
    ],
    'contributors': [
        "Comunitea ",
        "Javier Colmenero <javier@comunitea.com>"
    ],
    "data": [
        "views/report_invoice.xml",
        "views/layouts.xml",
        "views/manufacturing_order.xml",
        "views/stock_picking.xml",
        "views/sale_order_tree.xml",
    ],
    "demo": [
    ],
    'test': [
    ],
    "installable": True
}
