# (c) 2014 Daniel Campos <danielcampos@avanzosc.es>
# (c) 2020 Omar Castiñeira Saavedra - Comunitea Servicios Tecnológicos S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    mrp_repair_id = fields.Many2one(
        'repair.order', string='Repair Order')

    repair_product = fields.Many2one(
        comodel_name='product.product', string='Product to Repair',
        store=False, related='mrp_repair_id.product_id', readonly=True)

    mrp_repair_lines = fields.One2many(
                comodel_name="repair.line", inverse_name='task_id',
                related='mrp_repair_id.operations', readonly=True,
                string='Scheduled Operations')

    @api.multi
    def write(self, vals):
        for rec in self:
            super(ProjectTask, rec.with_context(
                repair=rec.mrp_repair_id)).write(vals)
        return True

