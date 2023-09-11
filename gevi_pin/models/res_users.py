# -*- coding: utf-8 -*-
from odoo import fields, models, api
# from openerp.tools.translate import _


class ResUsers(models.Model):
    _inherit = 'res.users'

    pin = fields.Char(string="PIN", help="PIN (4 cifre)", size=4, default="0000")
    timbro_isp = fields.Binary(
        string='Timbro Ispettore',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help=False
    )

    timbro_rt = fields.Binary(
        string='Timbro Responsabile Tecnico',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help=False
    )

    # vecchio_pin = fields.Char(string="Vecchio PIN", help="PIN (4 cifre)", size=4)
    # nuovo_pin = fields.Char(string="Nuovo PIN", help="PIN (4 cifre)", size=4)
    # conferma_pin = fields.Char(string="Conferma PIN", help="PIN (4 cifre)", size=4)

    # def controllo_pin(self):
    #     if self.nuovo_pin != self.conferma_pin:
    #         return {'error': ('Il nuovo PIN e la sua conferma devono essere identici!'), 'title': ('Attenzione')}
    #     elif self.vecchio_pin != self.pin:
    #         return {'error': ('Il vecchio PIN è errato, per poter continuare è necessario inserire il pin corretto!'), 'title': ('Attenzione')}
    #     return True

    # @api.one
    # def preferenze_cambio_pin(self):
    #     if self.controllo_pin():
    #         self.pin = self.nuovo_pin
    #         self.nuovo_pin = ""
    #         self.conferma_pin = ""
    #         self.vecchio_pin = ""

    # @api.multi
    def preferenze_cambio_pin(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'gevi_pin.wizard.cambiopin',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }

    # versione con specifica v7
    # def preferenze_cambio_pin(self, cr, uid, ids, context=None):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'gevi_pin.wizard.cambiopin',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'target': 'new',
    #     }
