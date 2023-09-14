from odoo import fields, models


class ClassePesiera(models.Model):
    _name = 'gevi_zbilance.classe_pesiera'
    _description = "Classe Pesiera"

    name = fields.Char("Codice")
