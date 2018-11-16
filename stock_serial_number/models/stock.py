# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class StockPackOperation(models.Model):

    _inherit = 'stock.pack.operation'

    serial_numbers_str = fields.Char(size=512, readonly=True, copy=False)
    # Para que el cliente web pueda leer este atributo en la operación
    use_serial_number = fields.Boolean('Use serial number',
                                       related="product_id.use_serial_number",
                                       readonly=True)

    @api.multi
    def action_drop_down(self):
        return super(
            StockPackOperation,
            self.with_context(move_serial_number=True)).action_drop_down()

    @api.one
    def copy(self, default=None):
        res = super(StockPackOperation, self).copy(default)
        if self._context.get('move_serial_number', False):
            res.serial_numbers_str = self.serial_numbers_str
            self.serial_numbers_str = False
        return res

    @api.multi
    def set_serial_numbers(self, serial_numbers):
        """
            Se crea una operacion con una unidad por cada numero de serie.
            TODO: Tal vez fallaria si la cantidad de numeros de serie es igual
            a la cantidad de la operacion
        """
        serial_numbers_str = ''
        lots = []
        for serial_number in serial_numbers:
            lot = self.env['stock.production.lot'].search(
                [('name', '=', serial_number),
                 ('product_id', '=', self.product_id.id)])
            if not lot:
                lot = self.env['stock.production.lot'].create(
                    {'name': serial_number,
                     'product_id': self.product_id.id})
            else:
                lot = lot[0]
            lots.append(str(lot.id))
            if not self.lot_id:
                self.lot_id = lot.id

        serial_numbers_str = ','.join(lots)
        self.write({'serial_numbers_str': serial_numbers_str})
        return True


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.multi
    def do_transfer(self):
        for pick in self:
            for operation in pick.pack_operation_ids:
                if operation.serial_numbers_str:
                    serial_numbers_str = \
                        operation.serial_numbers_str.split(',')
                    serial_numbers_ids = map(int, serial_numbers_str)
                    while serial_numbers_ids:
                        lot_id = serial_numbers_ids.pop()
                        vals = {'qty_done': 1, 'lot_id': lot_id,
                                'serial_numbers_str': '',
                                'product_qty': 1}
                        operation.with_context(no_recumpute=True).copy(vals)
                    operation.unlink()
        return super(StockPicking, self).do_transfer()
