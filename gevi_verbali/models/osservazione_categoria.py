# -*- coding: utf-8 -*-
from odoo import fields, models


class OsservazioneCategoria(models.Model):
    _name = 'gevi_verbali.osservazione_categoria'

    name = fields.Char('Nome')
    indice_categoria = fields.Char(string='Categoria delle Osservazioni')
