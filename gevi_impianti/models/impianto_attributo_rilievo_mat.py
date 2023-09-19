# -*- coding: utf-8 -*-
from odoo import fields, models


class ImpiantoAttributoRilievoMat(models.Model):
    _name = 'gevi.impianti.impianto_attributo_rilievo_mat'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Impianto Attributo Rilievo MAT"

    name = fields.Char('Nome')
    impianto_categoria_id = fields.Many2one('gevi.impianti.impianto_categoria')
