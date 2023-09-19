from odoo import fields, models


class ProvaTara(models.Model):
    _name = 'gevi_zbilance.prova_tara'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Prova Tara"

    verbale_id = fields.Many2one(
        'gevi_zbilance.verbale', ondelete='cascade', string="Verbale")

    divisione = fields.Integer("Divis.")
    carico_l = fields.Integer("Massa L")
    indicazione = fields.Float("Ind.")
    add_load = fields.Float("AL")  # carico_addizionale
    errore_e = fields.Float("Err E0")
    verifica = fields.Boolean("Pass", default=False)
