# -*- coding: utf-8 -*-
from odoo import fields, models


class CaricaAttributiDescrittivi(models.TransientModel):
    _name = 'gevi_wizard_operativi.carica_attributi_descrittivi'
    _description = "Carica Attributi Descrittivi"

    def carica_attributi_descrittivi(self):
        impianti_obj = self.env['gevi.impianti.impianto'].browse(
            self._context.get('active_ids', []))
        for impianto in impianti_obj:
            impianto.ricarica_attributi_impianto()
        return {'type': 'ir.actions.act_window_close'}

    def carica_attributi_descrittivi_pem(self):
        impianti_obj = self.env['gevi.impianti.impianto'].browse(
            self._context.get('active_ids', []))
        categoria_asc = self.env['gevi.impianti.impianto_categoria'].search([('name', '=', 'Ascensore Generico')],
                                                                            limit=1)
        for impianto in impianti_obj:
            impianto_categoria = impianto.impianto_categoria_id
            impianto.impianto_categoria_id = categoria_asc.id
            impianto.attributi_caricati = False
            impianto.carica_attributi_descrittivi()
            impianto.impianto_categoria_id = impianto_categoria
        return {'type': 'ir.actions.act_window_close'}


class CambioCategoriaImpianto(models.TransientModel):
    _name = 'gevi_wizard_operativi.cambio_categoria_impianto'
    _description = "Cambio Categoria Impianto"

    impianto_categoria_id = fields.Many2one(
        'gevi.impianti.impianto_categoria', string='Categoria Impianto',
        domain=[('descrizione', '!=', 'BIL')]
    )

    def cambio_categoria_impianto(self):
        impianti_obj = self.env['gevi.impianti.impianto'].browse(
            self._context.get('active_ids', []))
        for impianto in impianti_obj:
            impianto.impianto_categoria_id = self.impianto_categoria_id
        return {'type': 'ir.actions.act_window_close'}
