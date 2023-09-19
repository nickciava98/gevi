# -*- coding: utf-8 -*-
from odoo import fields, models


class WizardAssegnaAgente(models.TransientModel):
    _name = 'gevi_zupdate20170530.wizard_assegna_agente'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Assegna Agente"

    agente_id = fields.Many2one(
        'hr.employee',
        string="Agente",
        domain=[('job_id.name', 'ilike', 'Agente')])

    def assegna_agente(self):
        referenti = self.env['gevi_contatti.referente'].browse(
            self._context.get('active_ids', []))
        for r in referenti:
            r.agente_id = self.agente_id
        return {'type': 'ir.actions.act_window_close'}
