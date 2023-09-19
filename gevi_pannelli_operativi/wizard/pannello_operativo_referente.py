# -*- coding: utf-8 -*-
from odoo import fields, models


class PannelloOperativoReferente(models.TransientModel):
    _name = 'gevi_pannelli_operativi.pannello_operativo_referente'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Pannello Operativo Referente"

    zona_commerciale_id = fields.Many2one('gevi_zone.zona_commerciale', string="Zona Commerciale")

    def cambio_zona_commerciale(self):
        referenti_obj = self.env['gevi_contatti.referente'].browse(
            self._context.get('active_ids', [])
        )
        for referente in referenti_obj:
            referente.zona_commerciale_id = self.zona_commerciale_id
        return {'type': 'ir.actions.act_window_close'}
