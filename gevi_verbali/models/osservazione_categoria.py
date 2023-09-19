# -*- coding: utf-8 -*-
from odoo import fields, models


class OsservazioneCategoria(models.Model):
    _name = 'gevi_verbali.osservazione_categoria'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Osservazione Categoria"

    name = fields.Char('Nome')
    indice_categoria = fields.Char(string='Categoria delle Osservazioni')
