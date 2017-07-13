# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields

class ProductTemplate(models.Model):

    _inherit = 'product.template'

    use_serial_number = fields.Boolean('Use serial number')
