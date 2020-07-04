from odoo import models, fields


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    customer_ref = fields.Char("Customer ref.")
