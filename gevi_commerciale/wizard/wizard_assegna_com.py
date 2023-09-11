# -*- coding: utf-8 -*-
from odoo import api, fields, models


class WizardAssegnaCom(models.TransientModel):
    _name = 'gevi_commerciale.wizard_assegna_com'

    commerciale_id = fields.Many2one(
        'hr.employee',
        string="Commerciale",
        domain=[('job_id.name', 'ilike', 'Commerciale')])

    def assegna_com(self):
        referenti = self.env['gevi_contatti.referente'].browse(
            self._context.get('active_ids', []))
        for referente in referenti:
            referente.utente_assegnato_id = self.commerciale_id.user_id
        return {'type': 'ir.actions.act_window_close'}
