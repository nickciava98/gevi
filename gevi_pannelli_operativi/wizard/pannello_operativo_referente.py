# -*- coding: utf-8 -*-
from openerp import fields, models, api, exceptions


class PannelloOperativoReferente(models.TransientModel):
    _name = 'gevi_pannelli_operativi.pannello_operativo_referente'

    zona_commerciale_id = fields.Many2one('gevi_zone.zona_commerciale', string="Zona Commerciale")

    @api.multi
    def cambio_zona_commerciale(self):
        referenti_obj = self.env['gevi_contatti.referente'].browse(
            self._context.get('active_ids', [])
        )
        for referente in referenti_obj:
            referente.zona_commerciale_id = self.zona_commerciale_id
        return {'type': 'ir.actions.act_window_close'}
