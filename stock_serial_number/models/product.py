# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductProduct(models.Model):

    _inherit = 'product.product'

    use_serial_number = fields.Boolean('Use serial number')
