from odoo import fields, models, api


class ClassePesiera(models.Model):
    _name = 'gevi_zbilance.classe_pesiera'

    name = fields.Char("Codice")

