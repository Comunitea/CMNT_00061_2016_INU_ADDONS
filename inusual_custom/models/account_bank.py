# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields
from datetime import date

class AccountBankStatementLine(models.Model):

    _inherit = 'account.bank.statement.line'

    date = fields.Date(default=lambda r: date.today())
