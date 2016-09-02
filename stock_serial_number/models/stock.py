# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class StockPackOperation(models.Model):

    _inherit = 'stock.pack.operation'

    @api.multi
    def set_serial_numbers(self, serial_numbers):
        """
            Se crea una operacion con una unidad por cada numero de serie.
            TODO: Tal vez fallaria si la cantidad de numeros de serie es igual a la cantidad de la operacion
        """
        lots = self.env['stock.production.lot']
        for serial_number in serial_numbers:
            lot = self.env['stock.production.lot'].search(
                [('name', '=', serial_number),
                 ('product_id', '=', self.product_id.id)])
            if not lot:
                lot = self.env['stock.production.lot'].create(
                    {'name': serial_number,
                     'product_id': self.product_id.id})
            lots += lot
        for lot in lots:
            self.copy({'product_qty': 1, 'qty_done': 1, 'lot_id': lot.id})
        self.write({'product_qty': self.product_qty - len(lots), 'qty_done': 0})
        return True
