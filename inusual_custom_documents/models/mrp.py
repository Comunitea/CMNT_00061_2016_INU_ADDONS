from odoo import models, fields


class ManufacturingOrder(models.Model):
    _inherit = 'mrp.production'

    notes = fields.Text()
