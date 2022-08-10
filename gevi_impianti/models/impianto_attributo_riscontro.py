# -*- coding: utf-8 -*-
from odoo import fields, models


class ImpiantoAttributoRiscontro(models.Model):
    _name = 'gevi.impianti.impianto_attributo_riscontro'

    name = fields.Char('Nome')
    impianto_categoria_id = fields.Many2one('gevi.impianti.impianto_categoria')
