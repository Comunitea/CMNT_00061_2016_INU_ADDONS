# © 2022 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    shipment_date = fields.Date("Shipment date")
    delivered = fields.Boolean("Delivered")
    delivery_date = fields.Date("Delivery date")
