# (c) 2014 Daniel Campos <danielcampos@avanzosc.es>
# (c) 2015 Pedro M. Baeza - Serv. Tecnol. Avanzados
# (c) 2020 Omar Castiñeira Saavedra - Comunitea Servicios Tecnológicos S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "MRP Repair Project Link",
    "summary": "Link repair with projects",
    "version": "12.0.1.0.0",
    "depends": [
        "mrp_analytic",
        "mrp_project",
        'repair'
    ],
    'license': 'AGPL-3',
    "images": [],
    "author": "OdooMRP team,"
              "AvanzOSC,"
              "Serv. Tecnol. Avanzados - Pedro M. Baeza,"
              "Antiun Ingeniería S.L.,"
              "Odoo Community Association (OCA)",
    "category": "Manufacturing",
    'data': [
        "views/mrp_repair_view.xml",
        "views/project_task_view.xml",
    ],
    'installable': True,
    'auto_install': False,
}
