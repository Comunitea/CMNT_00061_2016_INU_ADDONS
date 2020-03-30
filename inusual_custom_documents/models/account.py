# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    weight = fields.Float('Weight', digits=dp.get_precision('Stock Weight'))

    @api.onchange('product_id')
    def intrastat_product_id_change(self):
        super().intrastat_product_id_change()
        if self.hs_code_id:
            self.weight = self.product_id.weight


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, qty):
        res = super()._prepare_invoice_line(qty)
        if self.product_id:
            hs_code = self.product_id.get_hs_code_recursively()
            if hs_code:
                res['hs_code_id'] = hs_code.id
                res['weight'] = self.product_id.weight
        return res
