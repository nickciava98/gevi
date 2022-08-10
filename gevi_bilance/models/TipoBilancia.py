# -*- coding: utf-8 -*-

from openerp import fields, models, api, exceptions

class TipoBilancia(models.Model):
    _name = 'gevi_bilance.tipobilanciatable'
    _description = "Gevi Bilance Tipo Bilancia"
    name = fields.Char(string="Tipo Bilancia") #tipoBilanciaAttr