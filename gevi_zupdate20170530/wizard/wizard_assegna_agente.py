# -*- coding: utf-8 -*-
from openerp import api, fields, models


class WizardAssegnaAgente(models.TransientModel):
    _name = 'gevi_zupdate20170530.wizard_assegna_agente'

    agente_id = fields.Many2one(
        'hr.employee',
        string="Agente",
        domain=[('job_id.name', 'ilike', 'Agente')])

    @api.multi
    def assegna_agente(self):
        referenti = self.env['gevi_contatti.referente'].browse(
            self._context.get('active_ids', []))
        for r in referenti:
            r.agente_id = self.agente_id
        return {'type': 'ir.actions.act_window_close'}
