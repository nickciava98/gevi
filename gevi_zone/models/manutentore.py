# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Manutentore(models.Model):
    _inherit = 'gevi_contatti.manutentore'

    zona_impianto_id = fields.Many2one('gevi_zone.zona_impianto', string="Zona Impianto", ondelete="cascade")
