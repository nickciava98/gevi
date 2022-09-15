# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class CambioCategoriaImpiantoVerbale(models.TransientModel):
    _name = 'gevi_wizard_operativi.cambio_categoria_impianto_verbale'

    impianto_categoria_id = fields.Many2one(
        'gevi.impianti.impianto_categoria', string='Categoria Impianto')

    def cambio_categoria_impianto(self):
        verbali_obj = self.env['gevi_verbali.verbale'].browse(
            self._context.get('active_ids', []))
        for verbale in verbali_obj:
            verbale.impianto_categoria_id = self.impianto_categoria_id
            verbale.ricarica_attributi_verbale()
        return {'type': 'ir.actions.act_window_close'}


    def aggiorna_manutentore(self):
        verbali_obj = self.env['gevi_verbali.verbale'].browse(
            self._context.get('active_ids', []))
        for verbale in verbali_obj:
            if verbale.state in ['bozza', 'assegnato']:
                verbale.manutentore_id = verbale.contratto_id.manutentore_id
        return {'type': 'ir.actions.act_window_close'}

