# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions


class WizardConferma(models.TransientModel):
    _name = 'gevi_verbali.wizardconferma'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Conferma"

    pin = fields.Char(string="Inserire il PIN", help="PIN (4 cifre)", size=4)
    verbale_id = fields.Many2one(
        "gevi_verbali.verbale"
    )

    def conferma_con_pin(self):
        for line in self:
            verbale = line.verbale_id
            if line.pin == self.env.user.pin:
                if verbale.state in "confermato":
                    verbale.action_validato()
                else:
                    if verbale.state in "in_revisione":
                        verbale.action_riconfermato()
                    else:
                        if verbale.state in "eseguito":
                            verbale.action_confermato()
                        else:
                            raise exceptions.ValidationError('Non c\'è nulla da validare!')
            else:
                raise exceptions.ValidationError('Il PIN non è corretto, riprovare!')
            return {'type': 'ir.actions.act_window_close'}
