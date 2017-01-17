# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class AccountBankStatementLine(models.Model):

    _inherit = 'account.bank.statement.line'

    @api.onchange('statement_id')
    def onchange_statement_id(self):
        seflf.date = self.statement_id.date
