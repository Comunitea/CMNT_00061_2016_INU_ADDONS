# (c) 2014 Daniel Campos <danielcampos@avanzosc.es>
# (c) 2020 Omar Castiñeira Saavedra - Comunitea Servicios Tecnológicos S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, fields


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    mrp_production_id = fields.Many2one(
        comodel_name='mrp.production', string='Manufacturing Order')
    workorder_id = fields.Many2one(
        comodel_name='mrp.workorder', string='Work Order',
        oldname='workorder')

    @api.model
    def create(self, vals):
        context = dict(self.env.context)
        production = context.get('production', False)
        workorder = context.get('workorder', False)
        vals['mrp_production_id'] = vals.get(
            'mrp_production_id', False
        ) or production and production.id
        vals['workorder_id'] = vals.get(
            'workorder_id', False
        ) or workorder and workorder.id
        return super().create(vals)
