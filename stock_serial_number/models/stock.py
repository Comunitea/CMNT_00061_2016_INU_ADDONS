# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, exceptions, _, api


class StockMove(models.Model):

    _inherit = 'stock.move'

    serial_numbers = fields.Text("Serial numbers",
                                 help="Write serial numbers separated by "
                                      "commas")

    def apply_serial_numbers(self):
        self.ensure_one()
        if not self.serial_numbers:
            raise exceptions.UserError(_("Any serial number to apply"))
        serials = list(set(self.serial_numbers.split(',')))
        if not serials:
            raise exceptions.UserError(_("Any serial number to apply"))
        elif len(serials) != len(self.move_line_ids):
            raise exceptions.UserError(_("The number of serial numbers is "
                                         "not equal to operations"))
        else:
            for line in self.move_line_ids:
                if not serials:
                    break
                serial = serials.pop()
                serial_id = self.env['stock.production.lot'].\
                    search([('name', '=', serial),
                            ('product_id', '=', self.product_id.id)],
                           limit=1)
                if serial_id:
                    line.write({'lot_id': serial_id.id})
                else:
                    line.write({'lot_name': serial,
                                'lot_id': False})
                line.onchange_serial_number()
            self.serial_numbers = False
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.move',
            'res_id': self.id,
            'view_id': self.env.ref('stock.view_stock_move_operations').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def action_show_details(self):
        res = super().action_show_details()
        res['context']['show_source_location'] = False
        res['context']['show_destination_location'] = False
        return res


class StockProductionLot(models.Model):

    _inherit = "stock.production.lot"

    available = fields.Boolean("Available", compute="_get_available",
                               store=True)

    @api.depends('quant_ids.quantity')
    def _get_available(self):
        for lot in self:
            lot.available = any(lot.quant_ids.
                                filtered(lambda x: x.quantity > 0.0 and
                                         x.location_id.usage == 'internal'))


class MrpProductProduceLot (models.TransientModel):
    _name = 'mrp.product.produce.lot'

    lot_id = fields.Many2one('stock.production.lot', 'Lot')
    lot_name = fields.Char("Lot name")
    qty_done = fields.Float('Done', default=1.0)
    wizard_id = fields.Many2one('mrp.product.produce', 'Wizard')


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    location_id = fields.Many2one("stock.location", string="Location",
                                  related="production_id.location_src_id")
    lot_ids = fields.One2many('mrp.product.produce.lot', 'wizard_id',
                              'Serials')
    serial_numbers = fields.Text("Serial numbers",
                                 help="Write serial numbers separated by "
                                      "commas")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if self._context and self._context.get('active_id'):
            production = self.env['mrp.production'].\
                browse(self._context['active_id'])
            serial_finished = (production.product_id.tracking == 'serial')
            if serial_finished:
                main_product_moves = production.move_finished_ids.\
                    filtered(lambda x: x.product_id.id ==
                             production.product_id.id)
                todo_quantity = production.product_qty - \
                    sum(main_product_moves.mapped('quantity_done'))
                todo_quantity = todo_quantity if (todo_quantity > 0) else 0
                if 'product_qty' in fields:
                    res['product_qty'] = todo_quantity
        return res

    def apply_serial_numbers(self):
        self.ensure_one()
        if not self.serial_numbers:
            raise exceptions.UserError(_("Any serial number to apply"))
        serials = list(set(self.serial_numbers.split(',')))
        if not serials:
            raise exceptions.UserError(_("Any serial number to apply"))
        else:
            self.lot_ids.unlink()
            for serial in serials:
                serial_id = self.env['stock.production.lot'].\
                    search([('name', '=', serial),
                            ('product_id', '=', self.product_id.id)],
                           limit=1)
                if serial_id:
                    self.env['mrp.product.produce.lot'].\
                        create({'lot_id': serial_id.id,
                                'wizard_id': self.id})
                else:
                    self.env['mrp.product.produce.lot'].\
                        create({'lot_name': serial,
                                'wizard_id': self.id})
            self.serial_numbers = False
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mrp.product.produce',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def check_finished_move_lots(self):
        if not self.lot_ids:
            return super().check_finished_move_lots()
        else:
            produce_move = self.production_id.move_finished_ids.\
                filtered(lambda x: x.product_id == self.product_id and
                         x.state not in ('done', 'cancel'))
            for lot in self.lot_ids:
                if lot.lot_name and not lot.lot_id:
                    lot_obj = self.env['stock.production.lot'].\
                        create({'name': lot.lot_name,
                                'product_id': self.product_id.id})
                    lot.lot_id = lot_obj.id

                existing_move_line = produce_move.move_line_ids.\
                    filtered(lambda x: x.lot_id == lot.lot_id)
                if existing_move_line:
                    if self.product_id.tracking == 'serial':
                        raise exceptions.\
                            UserError(_('You cannot produce the same serial '
                                        'number twice.'))
                    produced_qty = self.product_uom_id.\
                        _compute_quantity(lot.qty_done,
                                          existing_move_line.product_uom_id)
                    existing_move_line.product_uom_qty += produced_qty
                    existing_move_line.qty_done += produced_qty
                else:
                    location_dest_id = produce_move.location_dest_id.\
                        get_putaway_strategy(self.product_id).id or \
                        produce_move.location_dest_id.id
                    vals = {
                      'move_id': produce_move.id,
                      'product_id': produce_move.product_id.id,
                      'production_id': self.production_id.id,
                      'product_uom_qty': lot.qty_done,
                      'product_uom_id': self.product_uom_id.id,
                      'qty_done': lot.qty_done,
                      'lot_id': lot.lot_id.id,
                      'location_id': produce_move.location_id.id,
                      'location_dest_id': location_dest_id,
                    }
                    self.env['stock.move.line'].create(vals)

            for pl in self.produce_line_ids:
                if pl.qty_done:
                    if pl.product_id.tracking != 'none' and not pl.lot_id:
                        raise exceptions.UserError(_('Please enter a lot or '
                                                     'serial number for %s !'
                                                     % pl.product_id.
                                                     display_name))
                    if not pl.move_id:
                        # Find move_id that would match
                        move_id = self.production_id.move_raw_ids.\
                            filtered(lambda m: m.product_id == pl.product_id
                                     and m.state not in ('done', 'cancel'))
                        if move_id:
                            pl.move_id = move_id
                        else:
                            # create a move and put it in there
                            order = self.production_id
                            pl.move_id = self.env['stock.move'].create({
                                        'name': order.name,
                                        'product_id': pl.product_id.id,
                                        'product_uom': pl.product_uom_id.id,
                                        'location_id':
                                        order.location_src_id.id,
                                        'location_dest_id':
                                        self.product_id.
                                        property_stock_production.id,
                                        'raw_material_production_id': order.id,
                                        'group_id':
                                        order.procurement_group_id.id,
                                        'origin': order.name,
                                        'state': 'confirmed'})
                    pl.move_id.\
                        _generate_consumed_move_line(pl.qty_done,
                                                     self.lot_ids[0].lot_id,
                                                     lot=pl.lot_id)
            return True
