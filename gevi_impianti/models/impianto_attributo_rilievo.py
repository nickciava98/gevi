# -*- coding: utf-8 -*-
from odoo import fields, models


class ImpiantoAttributoRilievo(models.Model):
    _name = 'gevi.impianti.impianto_attributo_rilievo'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Impianto Attributo Rilievo"

    name = fields.Char('Nome')
    unita_di_misura_id = fields.Many2one('gevi.impianti.unita_di_misura', string='Unità di Misura')
    impianto_categoria_id = fields.Many2one('gevi.impianti.impianto_categoria')
