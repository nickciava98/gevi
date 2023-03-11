from odoo import fields, models, api


class ProvaLinearita(models.Model):
    _name = 'gevi_zbilance.prova_linearita'

    verbale_id = fields.Many2one(
        'gevi_zbilance.verbale', ondelete='set null', string="Verbale")

    divisione = fields.Integer("Divis.")
    carico_l = fields.Integer("Massa L")
    indicazione_cres = fields.Float("Ind. Cresc")
    indicazione_decr = fields.Float("Ind. Decres.")
    add_load_cres = fields.Float("Add Load Cresc.") # carico_addizionale
    add_load_decr = fields.Float("Add Load Decres.")
    errore_e_zero_cres = fields.Float("Err E0 Cresc.")
    errore_e_zero_decr = fields.Float("Err E0 Decres.")
    errore_e_corr_cres = fields.Float("Err Corr Cresc.")
    errore_e_corr_decr = fields.Float("Err Corr Decres.")
    mpe = fields.Float("mpe")
    verifica_cres = fields.Boolean("Pass Cresc", default=False)
    verifica_decr = fields.Boolean("Pass Decres", default=False)
