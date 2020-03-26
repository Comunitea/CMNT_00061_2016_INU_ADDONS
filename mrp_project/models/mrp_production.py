# (c) 2014 Daniel Campos <danielcampos@avanzosc.es>
# (c) 2015 Pedro M. Baeza - Serv. Tecnol. Avanzados
# (c) 2020 Omar Castiñeira Saavedra - Comunitea Servicios Tecnológicos S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    @api.depends('analytic_account_id')
    def _compute_project_id(self):
        project = self.env['project.project']
        for record in self:
            project_domain = [(
                'analytic_account_id', '=', record.analytic_account_id.id
            )]
            record.project_id = project.search(project_domain, limit=1)[:1]

    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Project",
        compute='_compute_project_id',
        store=True, readonly=True
    )

    @api.model
    def _prepare_project_vals(self, production):
        return {
            'name': production.name,
            'user_id': production.user_id.id,
            'allow_timesheets': True,
            'automatic_creation': True
        }

    @api.multi
    def _prepare_production_task(self):
        product = self.product_id
        task_name = "{0}::{1}- {2}".format(
            self.name,
            "[{0}] ".format(
                product.default_code if product.default_code else ""
            ),
            product.name
        )
        task_descr = _("""
            <p><b>Manufacturing Order:</b> {0}</p>
            <p><b>Product to Produce:</b> [{1}]{2}</p>
            <p><b>Quantity to Produce:</b> {3}</p>
            <p><b>Bill of Material:</b> {4} - {5}</p>
            <p><b>Planned Date:</b> {6} - {7}</p>
            """.format(
            self.name,
            self.product_id.default_code,
            self.product_id.name,
            self.product_qty,
            self.bom_id.product_tmpl_id.name,
            self.bom_id.sequence,
            self.date_planned_start,
            self.date_planned_finished
        ))
        return {
            'mrp_production_id': self.id,
            'user_id': self.user_id.id,
            'name': task_name,
            'project_id': self.project_id.id,
            'description': task_descr
        }

    @api.multi
    def _prepare_workorder_task(self, workorder):
        product = workorder.production_id.product_id
        task_name = "{0}: {1} - {2}".format(
            workorder.production_id.name,
            workorder.name,
            product.name
        )
        task_descr = _("""
            <p><b>Manufacturing Order:</b> {0}</p>
            <p><b>Product to Produce:</b> [{1}]{2}</p>
            <p><b>Quantity to Produce:</b> {3}</p>
            <p><b>Bill of Material:</b> {4} - {5}</p>
            <p><b>Planned Date:</b> {6} - {7}</p>
            <p><b>Workorder:</b> {8}</p>
            """.format(
            self.name,
            self.product_id.default_code,
            self.product_id.name,
            self.product_qty,
            self.bom_id.product_tmpl_id.name,
            self.bom_id.sequence,
            self.date_planned_start,
            self.date_planned_finished,
            workorder.name
        ))
        return {
            'mrp_production_id': self.id,
            'user_id': self.user_id.id,
            'name': task_name,
            'project_id': self.project_id.id,
            'description': task_descr,
            'workorder_id': workorder.id
        }

    @api.multi
    def _generate_moves(self):
        res = super()._generate_moves()
        project_obj = self.env['project.project']
        task_obj = self.env['project.task']
        for production in self:
            if not production.project_id:
                project_vals = self._prepare_project_vals(production)
                project = project_obj.create(project_vals)
                production.analytic_account_id = project.analytic_account_id.id
            if not production.routing_id:
                task_domain = [('mrp_production_id', '=', production.id),
                               ('workorder_id', '=', False)]
                tasks = task_obj.search(task_domain)
                if not tasks:
                    task_obj.create(production._prepare_production_task())
        return res

    @api.multi
    def _generate_workorders(self, exploded_boms):
        task_obj = self.env['project.task']
        workorders = super()._generate_workorders(exploded_boms)
        for workorder in workorders:
            task_domain = [('mrp_production_id', '=', self.id),
                           ('workorder_id', '=', workorder.id)]
            tasks = task_obj.search(task_domain)
            if not tasks:
                task_obj.create(self._prepare_workorder_task(workorder))
        return workorders

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


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    task_ids = fields.One2many(
        comodel_name="project.task", inverse_name="workorder_id",
        string="Tasks")
    work_ids = fields.One2many(
        comodel_name="account.analytic.line", inverse_name="workorder_id",
        string="Task works")
