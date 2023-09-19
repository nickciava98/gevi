# -*- coding: utf-8 -*-
from odoo import fields, models


class WizardAssegnaISP(models.TransientModel):
    _name = 'gevi_zbilance.wizard_assegna_isp'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Assegna Ispettore"

    ispettore_id = fields.Many2one(
        'hr.employee',
        string="Ispettore",
        domain=[('job_id.name', 'ilike', 'Ispettore')])

    verbale_id = fields.Many2one(
        "gevi_zbilance.verbale"
    )

    def assegna_isp(self):
        verbali = [self.verbale_id]
        for verbale in verbali:
            if verbale.state in "in_revisione":
                verbale.ispettore_id = self.ispettore_id
            if verbale.state in "assegnato":
                verbale.ispettore_id = self.ispettore_id
            if verbale.state in "eseguito":
                verbale.ispettore_id = self.ispettore_id
            if verbale.state in "bozza":
                verbale.ispettore_id = self.ispettore_id
                verbale.action_assegnato()
        return {'type': 'ir.actions.act_window_close'}
