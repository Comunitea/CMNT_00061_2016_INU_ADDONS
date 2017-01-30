# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Pexego All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@pexego.es>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class product_customer(models.Model):

    _name = 'product.customer'

    name = fields.Char('Name', size=64)
    code = fields.Char('Code', size=64)
    customer_id = fields.Many2one('res.partner', 'Customer', required=True)
    product_id = fields.Many2one('product.template', 'Reference')


class product_template(models.Model):

    _inherit = 'product.template'

    product_customer_ids = fields.One2many('product.customer', 'product_id',
                                           'Customer name')


class product_product(models.Model):

    _inherit = 'product.product'

    def get_product_ref(self, partner):
        if not partner:
            return self.default_code or ''
        if isinstance(partner, (int, long)):
            partner = self.env['res.partner'].browse(partner)
        custom_prod = self.env['product.customer'].search(
            [('product_id', '=', self.id), ('customer_id', '=', partner.id)])
        if not custom_prod:
            top_partner_id = partner.get_top_partner_id()
            custom_prod = self.env['product.customer'].search(
                [('product_id', '=', self.id), ('customer_id', '=',
                                                top_partner_id)])
        return custom_prod and custom_prod[0].code or '', custom_prod and \
                                                     custom_prod[0].name or ''

    def get_product_complete_name(self, partner):
        code = False
        name = False
        if not partner:
            return self.default_code or ''
        if isinstance(partner, (int, long)):
            partner = self.env['res.partner'].browse(partner)
        custom_prod = self.env['product.customer'].search(
            [('product_id', '=', self.id), ('customer_id', '=', partner.id)])
        if not custom_prod:
            top_partner_id = partner.get_top_partner_id()
            custom_prod = self.env['product.customer'].search(
                [('product_id', '=', self.id), ('customer_id', '=',
                                                top_partner_id)])

            code = custom_prod and custom_prod[0].code or self.code
            name = custom_prod and custom_prod[0].name or self.name

        ref = '[' + code + '] ' if code else ''
        return ref + name
