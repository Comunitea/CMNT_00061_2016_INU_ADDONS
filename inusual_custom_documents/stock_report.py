# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, _


class ReportMedAudio(models.AbstractModel):
    _name = 'report.inusual_custom_documents.action_report_med_audio'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'inusual_custom_documents.action_report_med_audio')

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'report_tittle': 'MEDICIÓN AUDIO'
        }
        with self.env.do_in_draft():
            docargs['docs'].valued_picking = False
            res = report_obj.render('stock.report_picking',
                                     docargs)
        return res


class ReportMedPant(models.AbstractModel):
    _name = 'report.inusual_custom_documents.action_report_med_pantalla'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'inusual_custom_documents.action_report_med_pantalla')

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'report_tittle': 'MEDICIÓN PANTALLAS'
        }
        with self.env.do_in_draft():
            docargs['docs'].valued_picking = False
            res = report_obj.render('stock.report_picking',
                                     docargs)
        return res
