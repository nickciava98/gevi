# -*- coding: utf-8 -*-

from openerp import fields, models, api, exceptions

class Classe(models.Model):
    _name = 'gevi_bilance.classe'
    _description = "Gevi Bilance Classe"
    # classeBilancia
    name = fields.Char(string="Classe Bilancia")
    
    