# (c) 2014 Daniel Campos <danielcampos@avanzosc.es>
# (c) 2020 Omar Castiñeira Saavedra - Comunitea Servicios Tecnológicos S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    def _project_shortcut_count_repair(self):
        for repair in self:
            repair.repair_count = len(
                self.env['repair.order'].
                search([('project_id', '=', repair.id)]))

    repair_count = fields.Integer(
        string='Repair Count', compute="_project_shortcut_count_repair")
