# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Product serial numbers',
    'summary': '',
    'version': '8.0.1.0.0',
    'category': 'Stock',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base',
        'product',
        'stock',
    ],
    'data': [
        'views/product.xml',
        'views/assets.xml'
    ],
    'qweb': ['static/src/xml/picking.xml']
}
