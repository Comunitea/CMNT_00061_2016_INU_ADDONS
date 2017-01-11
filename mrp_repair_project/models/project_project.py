# -*- coding: utf-8 -*-
# (c) 2014 Daniel Campos <danielcampos@avanzosc.es>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.one
    def _project_shortcut_count_repair(self):
        self.repair_count = len(
            self.env['mrp.repair'].search([('project_id', '=', self.id)]))

    repair_count = fields.Integer(
        string='Repair Count', compute=_project_shortcut_count_repair)
    # automatic_creation = fields.Boolean('Automatic Creation')

