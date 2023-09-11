# -*- coding: utf-8 -*-
from odoo import fields, models


class ValoreAttributo(models.Model):
    _name = 'gevi.impianti.valore_attributo'
    _description = "Valore Attributo"

    name = fields.Char()

    tipo = fields.Selection(
        [
            ('da_selezionare', 'Da Selezionare'),
            ('Riscontro', 'Riscontro'),
            ('Rilievo', 'Rilievo'),
        ],
        default='da_selezionare')
