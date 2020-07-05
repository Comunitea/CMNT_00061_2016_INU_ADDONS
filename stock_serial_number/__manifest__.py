# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Product serial numbers',
    'summary': '',
    'version': '12.0.1.0.0',
    'category': 'Stock',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'stock_picking_filter_lot',
        'repair',
        'mrp'
    ],
    'data': ['views/stock_view.xml'],
}
