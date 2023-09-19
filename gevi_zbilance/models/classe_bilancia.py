from odoo import fields, models


class ClasseBilancia(models.Model):
    _name = 'gevi_zbilance.classe_bilancia'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Classe Bilancia"

    divisioni = fields.Char("Divisioni")
    classe_strumento = fields.Many2one(
        'gevi_zbilance.classe_strumento', string='Classe strumento',
        required=True, )
    classe_massa = fields.Many2one(
        'gevi_zbilance.classe_pesiera', string='Classe massa',
        required=True, )
