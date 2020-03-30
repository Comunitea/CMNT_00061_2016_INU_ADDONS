# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields


class StockMove(models.Model):

    _inherit = 'stock.move'

    def action_show_details(self):
        res = super().action_show_details()
        res['context']['show_source_location'] = False
        res['context']['show_destination_location'] = False
        return res
