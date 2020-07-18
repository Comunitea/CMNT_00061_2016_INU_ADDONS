# (c) 2016 Santi Argüeso - Comunitea Servicios Tecnológicos S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Inusual Custom ',
    'version': '12.0.1.0.0',
    'author': 'Comunitea ',
    "category": "Custom",
    'license': 'AGPL-3',
    'depends': [
        'account',
        'sale',
        'hr_expense'
    ],
    'contributors': [
        "Comunitea: ",
        "Santi Argüeso <santi@comunitea.com>, "
        "Omar Castiñeira Saavedra <omar@comunitea.com>"
    ],
    "data": [
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
        'views/hr_expense_view.xml',
    ],
    "installable": True
}
