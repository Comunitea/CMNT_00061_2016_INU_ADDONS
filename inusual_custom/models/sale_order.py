from odoo import models, fields


class SaleOrder(models.Model):

    _inherit = "sale.order"

    confirmation_date = fields.Datetime(readonly=False)
