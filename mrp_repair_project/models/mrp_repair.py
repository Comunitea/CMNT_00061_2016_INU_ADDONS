# (c) 2014 Daniel Campos <danielcampos@avanzosc.es>
# (c) 2015 Pedro M. Baeza - Serv. Tecnol. Avanzados
# (c) 2020 Omar Castiñeira Saavedra - Comunitea Servicios Tecnológicos S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api, _


class MrpRepair(models.Model):
    _inherit = 'repair.order'

    project_id = fields.Many2one(
        comodel_name="project.project", string="Project", copy=False,
        readonly=True, states={'draft': [('readonly', False)]})
    analytic_account_id = fields.Many2one(
        related="project_id.analytic_account_id", store=True,
        readonly=True)
    parent_analytic_acc_id = fields.Many2one("account.analytic.account",
                                             "Parent Account")

    @api.multi
    def _prepare_project_vals(self):
        return {
            'name': self.name,
            'automatic_creation': True,
            'allow_timesheets': True,
        }

    @api.multi
    def _prepare_repair_task(self):
        product = self.product_id
        task_name = "{0}: {1}{2}".format(
            self.name,
            "[{0}] ".format(product.default_code
                            if product.default_code else ""),
            product.name)
        task_descr = _("""Repair Order: {0}
Product to Repair: [{1}]{2}
Quantity to Repair: {3}""".format(
            self.name,
            self.product_id.default_code,
            self.product_id.name,
            self.product_qty,
        ))
        return {
            'mrp_repair_id': self.id,
            'name': task_name,
            'project_id': self.project_id.id,
            'description': task_descr
        }

    @api.multi
    def button_add_repair_task(self):
        task_obj = self.env['project.task']
        for record in self:
            task_domain = [('mrp_repair_id', '=', record.id)]
            tasks = task_obj.search(task_domain)
            if not tasks:
                task_obj.create(record._prepare_repair_task())

    @api.multi
    def action_repair_confirm(self):
        project_obj = self.env['project.project']
        result = super().action_repair_confirm()
        for repair in self:
            if not repair.project_id:
                project_vals = repair._prepare_project_vals()
                project = project_obj.create(project_vals)
                repair.project_id = project.id
                if repair.parent_analytic_acc_id:
                    repair.analytic_account_id.parent_id = \
                        repair.parent_analytic_acc_id.id
        return result

    @api.multi
    def action_repair_start(self):
        res = super().action_repair_start()
        for repair in self:
            repair.button_add_repair_task()
        return res

    @api.multi
    def unlink(self):
        projects = self.mapped('project_id').filtered('automatic_creation')
        tasks = self.env['project.task'].search(
            [('project_id', 'in', projects.ids)])
        if not tasks.mapped('timesheet_ids'):
            child_tasks = tasks.filtered(lambda x: x.parent_id)
            child_tasks.unlink()
            (tasks - child_tasks).unlink()
            projects.unlink()
        return super().unlink()
