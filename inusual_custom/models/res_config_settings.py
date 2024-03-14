from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    disable_partner_autofollow = fields.Boolean(
        config_parameter="inusual_custom.disable_partner_autofollow",
        string="Customer disable autofollow",
    )
