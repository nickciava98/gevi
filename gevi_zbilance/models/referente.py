# -*- coding: utf-8 -*-
from odoo import fields, models


class Referente(models.Model):
    _inherit = 'gevi_contatti.referente'

    verbale_bilance_ids = fields.One2many(
        string='Verbali',
        comodel_name='gevi_zbilance.verbale',
        inverse_name='referente_id',
    )
