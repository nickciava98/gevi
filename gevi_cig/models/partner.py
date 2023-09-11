# -*- coding: utf-8 -*-
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    banca_id = fields.Many2one(
        'res.partner.bank',
        string = "Banca d'appoggio"
    )
