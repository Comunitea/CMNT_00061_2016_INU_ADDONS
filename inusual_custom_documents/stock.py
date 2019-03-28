# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields


class StockMove(models.Model):

    _inherit = 'stock.move'

    def _get_invoice_line_vals(self, cr, uid, move, partner, inv_type,
                               context=None):
        res = super(StockMove, self)._get_invoice_line_vals(cr, uid, move,
                                                            partner, inv_type,
                                                            context)
        res['weight'] = move.product_id.weight
        hs_code = move.product_id.get_hs_code_recursively()
        if hs_code:
            res['hs_code_id'] = hs_code.id
        else:
            res['hs_code_id'] = False
        return res
