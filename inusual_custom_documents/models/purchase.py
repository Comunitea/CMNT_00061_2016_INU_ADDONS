# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order.line'

    @api.multi
    def _prepare_stock_moves(self, picking):
        res = super()._prepare_stock_moves(picking)
        if res and self.order_id.dest_address_id:
            res[0]['name'] = self.product_id.\
                with_context(lang=self.order_id.dest_address_id.lang).\
                display_name
        return res
