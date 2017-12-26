# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, _
from openerp.exceptions import except_orm


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def _check_invoice_validate(self):
        for inv in self:
            if not inv.commercial_partner_id.street:
                raise except_orm(_('Error validating data!'),
                                 _('Partner address must be setted'))

            if not inv.commercial_partner_id.vat:
                raise except_orm(_('Error validating data!'),
                                 _('Partner NIF must be setted'))
        return

    @api.multi
    def action_date_assign(self):
        self._check_invoice_validate()
        res = super(AccountInvoice, self).action_date_assign()
        return res
