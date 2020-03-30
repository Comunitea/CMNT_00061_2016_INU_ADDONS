# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class StockPicking(models.Model):

    _inherit = "stock.picking"

    @api.multi
    def _get_picking_valued(self):
        for picking in self:
            if picking.state == 'done':
                picking.valued = picking.partner_id.valued_picking

    @api.multi
    def _amount_all(self):
        for picking in self:
            if not picking.sale_id:
                picking.amount_discounted = picking.amount_gross = 0.0
                continue
            amount_gross = 0.0
            for line in picking.move_lines:
                sale_line = line.sale_line_id
                if sale_line and line.state != 'cancel':
                    amount_gross += (line.sale_line_id.price_unit *
                                     line.product_qty)
                else:
                    continue
            round_curr = picking.sale_id.currency_id.round
            picking.amount_gross = round_curr(amount_gross)
            picking.amount_discounted = round_curr(amount_gross) - \
                picking.amount_untaxed

    amount_gross = fields.Monetary('Amount gross', compute='_amount_all',
                                   compute_sudo=True)
    amount_discounted = fields.Monetary('Disounted amount',
                                        compute='_amount_all',
                                        compute_sudo=True)
    valued = fields.Boolean(compute='_get_picking_valued', related=None)
    comments = fields.Text()
