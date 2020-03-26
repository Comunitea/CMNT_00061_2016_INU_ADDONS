# (c) 2014 Daniel Campos <danielcampos@avanzosc.es>
# (c) 2020 Omar Castiñeira Saavedra - Comunitea Servicios Tecnológicos S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    def _compute_mrp_production_count(self):
        production = self.env['mrp.production']
        for project in self:
            domain = [('project_id', '=', self.id)]
            project.production_count = production.search_count(domain)

    production_count = fields.Integer(
        string='Manufacturing Count', compute="_compute_mrp_production_count")
    automatic_creation = fields.Boolean()
