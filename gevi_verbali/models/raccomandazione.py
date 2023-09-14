# -*- coding: utf-8 -*-
from odoo import fields, models


class Raccomandazione(models.Model):
    _name = 'gevi_verbali.raccomandazione'
    _description = "Raccomandazione"

    name = fields.Char('Nome')
    indice_osservazione = fields.Char('Indice')
    vincolante = fields.Boolean(default=False)
    tipo = fields.Char(string="Tipo")
