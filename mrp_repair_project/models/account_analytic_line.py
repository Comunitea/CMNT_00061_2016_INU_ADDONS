# (c) 2014 Daniel Campos <danielcampos@avanzosc.es>
# (c) 2020 Omar Castiñeira Saavedra - Comunitea Servicios Tecnológicos S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, fields


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    mrp_repair_id = fields.Many2one(
        comodel_name='repair.order', string='Repair Order')

    @api.model
    def create(self, vals):
        context = dict(self.env.context)
        repair = context.get('repair', False)
        vals['mrp_repair_id'] = vals.get(
            'mrp_repair_id', False
        ) or repair and repair.id
        return super().create(vals)
