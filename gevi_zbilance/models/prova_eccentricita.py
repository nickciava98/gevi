from odoo import fields, models, api


class ProvaEccentricita(models.Model):
    _name = 'gevi_zbilance.prova_eccentricita'

    verbale_id = fields.Many2one(
        'gevi_zbilance.verbale', ondelete='set null', string="Verbale")

    posizione = fields.Integer("Posizione")
    carico_l = fields.Integer("Massa L")
    indicazione = fields.Float("Ind.")
    add_load = fields.Float("AL") # carico_addizionale
    p = fields.Float("P")
    errore_e_zero = fields.Float("Err E0")
    errore_e_c = fields.Float("Err E Corr")
    mpe = fields.Float("mpe")
    verifica = fields.Boolean("Pass", default=False)
