from odoo import fields, models, api


class ProvaMobilita(models.Model):
    _name = 'gevi_zbilance.prova_mobilita'

    verbale_id = fields.Many2one(
        'gevi_zbilance.verbale', ondelete='set null', string="Verbale")

    divisione = fields.Integer("Divis.")
    carico_l = fields.Integer("Massa L")
    indicazione = fields.Float("Ind. I")
    add_load = fields.Float("C. extra") # carico_addizionale
    errore_e = fields.Float("I-I2")
    indicazione_i2 = fields.Float("Ind. I2")
    verifica = fields.Boolean("Pass")

    @api.onchange('divisione','carico_l','indicazione','add_load','indicazione_i2')
    def calcola_verifica(self):
        for line in self:
            line.verifica = False
            line.errore_e = abs(line.indicazione-line.indicazione_i2)
            if line.errore_e > 0:
                line.verifica = True

    def write(self, values):
        result = super(ProvaMobilita, self).write(values)
        return result
