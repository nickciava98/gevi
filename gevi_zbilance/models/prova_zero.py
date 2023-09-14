from odoo import fields, models


class ProvaZero(models.Model):
    _name = 'gevi_zbilance.prova_zero'
    _description = "Prova Zero"

    verbale_id = fields.Many2one(
        'gevi_zbilance.verbale', ondelete='cascade', string="Verbale")

    divisione = fields.Integer("Divis.")
    carico_l = fields.Integer("Massa L")
    indicazione = fields.Float("Ind.")
    add_load = fields.Float("AL")  # carico_addizionale
    p = fields.Float("P")
    errore_e = fields.Float("Err E")
    verifica = fields.Boolean("Pass", default=False)
