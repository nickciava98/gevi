# -*- coding: utf-8 -*-
from odoo import fields, models, api


class UtpCei(models.Model):
    _name = 'gevi_verbali.utpcei'

    name = fields.Char('Valore Tf')
    utp_cei_993 = fields.Integer("UTP CEI 99-3")
