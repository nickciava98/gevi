# -*- coding: utf-8 -*-
from odoo import fields, models


class ImpiantoUnitaDiMisura(models.Model):
    _name = 'gevi.impianti.unita_di_misura'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Unità di Misura"

    name = fields.Char('Simbolo')
    descrizione = fields.Char('Descrizione')
