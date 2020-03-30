# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, _, exceptions


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def _check_invoice_validate(self):
        for inv in self:
            if not inv.commercial_partner_id.street:
                raise exceptions.\
                    ValidationError(_('Partner address must be setted'))

            if not inv.commercial_partner_id.vat:
                raise exceptions.\
                    ValidationError(_('Partner NIF must be setted'))
        return

    @api.multi
    def action_invoice_open(self):
        self._check_invoice_validate()
        res = super().action_invoice_open()
        return res
