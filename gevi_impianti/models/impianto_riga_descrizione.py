# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ImpiantoRigaDescrizione(models.Model):
    _name = 'gevi.impianti.impianto_riga_descrizione'
    name = fields.Char('Nome')
    impianto_id = fields.Many2one(
        'gevi.impianti.impianto',
        ondelete='cascade',
        string="Riferimento Impianto")

    valore_attributo = fields.Char(string="Valore")
    unita_di_misura_id = fields.Many2one(
        'gevi.impianti.unita_di_misura',
        ondelete='set null',
        string="Unità di misura")
