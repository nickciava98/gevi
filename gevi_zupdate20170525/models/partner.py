# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class Partner(models.Model):
    _inherit = 'res.partner'

    tipo_attivita = fields.Char('Tipo attivita')