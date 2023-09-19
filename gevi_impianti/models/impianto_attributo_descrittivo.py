# -*- coding: utf-8 -*-
from odoo import fields, models


class ImpiantoAttributoDescrittivo(models.Model):
    _name = 'gevi.impianti.impianto_attributo_descrittivo'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Impianto Attributo Descrittivo"

    name = fields.Char('Nome')
    unita_di_misura_id = fields.Many2one('gevi.impianti.unita_di_misura', string='Unità di Misura')
    impianto_categoria_id = fields.Many2one('gevi.impianti.impianto_categoria', string='Categoria Impianto')
