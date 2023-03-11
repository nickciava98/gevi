from odoo import fields, models, api


class ProvaRipetibilita(models.Model):
    _name = 'gevi_zbilance.prova_ripetibilita'

    verbale_id = fields.Many2one(
        'gevi_zbilance.verbale', ondelete='set null', string="Verbale")

    indicazione = fields.Float("Indicazione I")
    delta_l = fields.Float("Add Load") # carico_addizionale
    p = fields.Float("P")
