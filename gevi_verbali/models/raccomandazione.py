# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Raccomandazione(models.Model):
    _name = 'gevi_verbali.raccomandazione'

    name = fields.Char('Nome')
    indice_osservazione = fields.Char('Indice')
    vincolante = fields.Boolean(default=False)
    tipo = fields.Char(string="Tipo")
