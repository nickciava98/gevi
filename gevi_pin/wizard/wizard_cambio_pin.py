# -*- coding: utf-8 -*-
from openerp import fields, models, api, exceptions


class WizardCambioPin(models.TransientModel):
    _name = 'gevi_pin.wizard.cambiopin'

    vecchio_pin = fields.Char(string="Vecchio PIN", help="PIN (4 cifre)", size=4)
    nuovo_pin = fields.Char(string="Nuovo PIN", help="PIN (4 cifre)", size=4)
    conferma_pin = fields.Char(string="Conferma PIN", help="PIN (4 cifre)", size=4)

    def controlla_pin(self):
        if self.vecchio_pin == self.env.user.pin and self.nuovo_pin == self.conferma_pin:
            return True
        else:
            raise exceptions.ValidationError('Assicurati che il pin attuale sia corretto e che il nuovo pin coincida con la conferma!')

    def cambia_pin(self):
        if self.controlla_pin():
            self.env.user.pin = self.nuovo_pin
