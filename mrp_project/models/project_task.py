# (c) 2014 Daniel Campos <danielcampos@avanzosc.es>
# (c) 2020 Omar Castiñeira Saavedra - Comunitea Servicios Tecnológicos S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    workorder_id = fields.Many2one(
        comodel_name='mrp.workorder', string='Work Order',
        oldname='workorder')
    mrp_production_id = fields.Many2one(
        'mrp.production', string='Manufacturing Order')
    production_scheduled_products = fields.One2many(
        comodel_name="stock.move", readonly=True,
        related='mrp_production_id.move_raw_ids', string='Scheduled Products')
    final_product = fields.Many2one(
        comodel_name='product.product', string='Product to Produce',
        related='mrp_production_id.product_id', readonly=True)

    @api.multi
    def write(self, vals):
        for rec in self:
            super(ProjectTask, rec.with_context(
                production=rec.mrp_production_id,
                workorder=rec.workorder_id)).write(vals)
        return True
