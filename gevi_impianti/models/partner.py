# -*- coding: utf-8 -*-
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    impianto_ids = fields.One2many(
        'gevi.impianti.impianto',
        'customer_id',
        string="Impianti",
        readonly=True)
