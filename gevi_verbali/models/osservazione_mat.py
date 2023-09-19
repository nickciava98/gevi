# -*- coding: utf-8 -*-
from odoo import fields, models


class OsservazioneMat(models.Model):
    _name = 'gevi_verbali.osservazione_mat'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Osservazione MaT"

    name = fields.Char('Nome')
    indice_osservazione = fields.Char('Indice')
    vincolante = fields.Boolean(default=False)
    tipo = fields.Char(string="Tipo")
