# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, models


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.model
    def _prepare_order_line_move(self, order, order_line,
                                 picking_id, group_id):
        res = super(PurchaseOrder, self)._prepare_order_line_move(
            order, order_line, picking_id, group_id)
        res[0]['name'] = order_line.product_id.with_context(
            lang=order.dest_address_id.lang).display_name
        return res
