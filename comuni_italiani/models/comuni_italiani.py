# -*- coding: utf-8 -*-
from odoo import fields, models


class ComuniItaliani(models.Model):
    _name = 'comuni_italiani.comune'

    name = fields.Char('Comune')
    cap = fields.Char('CAP', size=5)
    provincia = fields.Char('Provincia', size=2)
    regione = fields.Char('Regione')
    priorita = fields.Integer("Priorità")

    _order = 'priorita desc, name asc'
