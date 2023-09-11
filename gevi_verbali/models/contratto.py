# -*- coding: utf-8 -*-
from odoo import fields, models


class Contratto(models.Model):
    _inherit = 'gevi_contratti.contratto'

    verbali_ids = fields.One2many('gevi_verbali.verbale', 'contratto_id', string="Verbali", readonly=True)
