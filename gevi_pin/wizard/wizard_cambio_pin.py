# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions


class WizardCambioPin(models.TransientModel):
    _name = 'gevi_pin.wizard.cambiopin'
    _description = "Cambio PIN"

    vecchio_pin = fields.Char(string="Vecchio PIN", help="PIN (4 cifre)", size=4)
    nuovo_pin = fields.Char(string="Nuovo PIN", help="PIN (4 cifre)", size=4)
    conferma_pin = fields.Char(string="Conferma PIN", help="PIN (4 cifre)", size=4)

    def controlla_pin(self):
        if self.vecchio_pin == self.env.user.pin and self.nuovo_pin == self.conferma_pin:
            return True
        else:
            raise exceptions.ValidationError(
                'Assicurati che il pin attuale sia corretto e che il nuovo pin coincida con la conferma!')

    def cambia_pin(self):
        for line in self:
            if line.controlla_pin():
                self.env.user.pin = line.nuovo_pin
