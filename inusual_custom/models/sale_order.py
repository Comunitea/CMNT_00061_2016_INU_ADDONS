from odoo import api, models, fields, _


class SaleOrder(models.Model):

    _inherit = "sale.order"

    confirmation_date = fields.Datetime(readonly=False)


    @api.model
    def _sale_order_confirm_message_content(
            self):
        title = _('Sale confirmation %s') % (
            self.name)
        message = '<h3>%s</h3>' % title
        message += _('The following sale '
                     'has been confirmed %s:') % (
            self.name)
        message += '<ul>'

        return message



    def message_subscribe(self, partner_ids=None, channel_ids=None, subtype_ids=None):
        partner_ids = partner_ids or []
        if (
            self._context.get("sale_partner_disable_autofollow")
            and self.partner_id.id in partner_ids
        ):
            partner_ids.remove(self.partner_id.id)
        return super(SaleOrder, self).message_subscribe(
            partner_ids, channel_ids, subtype_ids
        )

    @api.model_create_multi
    def create(self, values):
         return super(
            SaleOrder,
            self.with_context(
                sale_partner_disable_autofollow=self._partner_disable_autofollow()
            ),
        ).create(values)


    def action_confirm(self):
        res = super(
            SaleOrder,
            self.with_context(
                sale_partner_disable_autofollow=self._partner_disable_autofollow()
            ),
        ).action_confirm()

        for sale in self:
            message = \
                self._sale_order_confirm_message_content()
            sale.sudo().message_post(
                body=message,
                subtype='inusual_custom.mt_sale_confirmation',
                author_id=self.env.user.partner_id.id)
        return res

    def _partner_disable_autofollow(self):
        """Returns the state of the "Customer disable autofollow" option

        Returns:
            bool: Option status
        """
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "inusual_custom.disable_partner_autofollow", False
            )
        )




