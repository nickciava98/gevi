# -*- coding: utf-8 -*-
from odoo import api, fields, models


class WizardAssegnaRT(models.TransientModel):
    _name = 'gevi_zbilance.wizard_assegna_rt'

    responsabile_tecnico_id = fields.Many2one(
        'hr.employee',
        string="Responsabile Tecnico",
        domain=[('job_id.name', 'ilike', 'Responsabile Tecnico')])

    def assegna_rt(self):
        verbali = self.env['gevi_zbilance.verbale'].browse(
            self._context.get('active_ids', []))
        for verbale in verbali:
            verbale.responsabile_tecnico_id = self.responsabile_tecnico_id
        return {'type': 'ir.actions.act_window_close'}
