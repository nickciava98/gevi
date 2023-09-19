# -*- coding: utf-8 -*-
from odoo import fields, models


class Osservazione(models.Model):
    _name = 'gevi_verbali.osservazione'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Osservazione"

    name = fields.Char('Nome')
    indice_osservazione = fields.Char('Indice')
    vincolante = fields.Boolean(default=False)
    osservazione_categoria_id = fields.Many2one('gevi_verbali.osservazione_categoria')
