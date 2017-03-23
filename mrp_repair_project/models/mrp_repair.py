# -*- coding: utf-8 -*-
# (c) 2014 Daniel Campos <danielcampos@avanzosc.es>
# (c) 2015 Pedro M. Baeza - Serv. Tecnol. Avanzados
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, _


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    project_id = fields.Many2one(
        comodel_name="project.project", string="Project", copy=False,
        readonly=True, states={'draft': [('readonly', False)]})
    analytic_account_id = fields.Many2one(
        related="project_id.analytic_account_id", store=True)
        	
	
    @api.model
    def _prepare_project_vals(self, repair):
        return {
            'name': repair.name,
            'use_tasks': True,
            'automatic_creation': True,
        }
        
        
    @api.model
    def _prepare_repair_task(self, repair):
        product = repair.product_id
        task_name = "%s::%s%s" % (
            repair.name,
            "[%s] " % product.default_code if product.default_code else "",
            product.name)
        task_descr = _("""
        Repair Order: %s
        Product to Repair: [%s]%s
        Quantity to Repair: %s
        """) % (repair.name, repair.product_id.default_code,
                repair.product_id.name, repair.product_qty)
        return {
            'mrp_repair_id': repair.id,
            'name': task_name,
            'project_id': repair.project_id.id,
            'description': task_descr
        }


    @api.multi
    def button_add_repair_task(self): 
        task_obj = self.env['project.task']        
        for record in self:
            task_domain = [('mrp_repair_id', '=', record.id),
                           ('workorder', '=', False)]
            tasks = task_obj.search(task_domain)
            if not tasks:
                task_obj.create(self._prepare_repair_task(record))
        # return super(MrpRepair, self).button_add_repair_task()
	


    @api.multi  
    def action_confirm(self):
        project_obj = self.env['project.project']
        result = super(MrpRepair, self).action_confirm()
        for repair in self:
            if not repair.project_id:
                project_vals = self._prepare_project_vals(repair)
                project = project_obj.create(project_vals)
                repair.project_id = project.id
        return result

    @api.multi
    def action_repair_start(self):
        res = super(MrpRepair, self).action_repair_start()
        for repair in self:
            repair. button_add_repair_task()
        return res



'''
    @api.multi   # VER ESTE 
    def unlink(self):
        projects = self.mapped('project_id').filtered('automatic_creation')
        tasks = self.env['project.task'].search(
            [('project_id', 'in', projects.ids)])
        if not tasks.mapped('work_ids'):
            child_tasks = tasks.filtered(lambda x: x.parent_ids)
            child_tasks.unlink()
            (tasks - child_tasks).unlink()
            projects.unlink()
        return super(MrpRepair, self).unlink()


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.production.workcenter.line'

    task_ids = fields.One2many(
        comodel_name="project.task", inverse_name="workorder", string="Tasks")
    work_ids = fields.One2many(
        comodel_name="project.task.work", inverse_name="workorder",
        string="Task works")

    @api.multi
    def write(self, vals, update=True):
        for rec in self:
            super(MrpProductionWorkcenterLine, rec.with_context(
                production=rec.production_id)).write(vals, update=update)
        return True
'''
