# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    weight = fields.Float('Weight')
