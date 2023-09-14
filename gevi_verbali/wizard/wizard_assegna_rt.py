# -*- coding: utf-8 -*-
from odoo import fields, models


class WizardAssegnaRT(models.TransientModel):
    _name = 'gevi_verbali.wizard_assegna_rt'

    responsabile_tecnico_id = fields.Many2one(
        'hr.employee',
        string="Responsabile Tecnico",
        domain=[('job_id.name', 'ilike', 'Responsabile Tecnico')])
    verbale_id = fields.Many2one(
        "gevi_verbali.verbale"
    )

    def assegna_rt(self):
        verbali = [self.verbale_id]
        for verbale in verbali:
            verbale.responsabile_tecnico_id = self.responsabile_tecnico_id
            verbale.action_assegnato()
        return {'type': 'ir.actions.act_window_close'}
