# -*- coding: utf-8 -*-
from odoo import fields, models


class ImpiantoUnitaDiMisura(models.Model):
    _name = 'gevi.impianti.unita_di_misura'
    _description = "Unità di Misura"

    name = fields.Char('Simbolo')
    descrizione = fields.Char('Descrizione')
