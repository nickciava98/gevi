# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Impianto(models.Model):
    _inherit = 'gevi.impianti.impianto'

    zona_impianto_id = fields.Many2one('gevi_zone.zona_impianto', string="Zona Impianto", ondelete="cascade")
