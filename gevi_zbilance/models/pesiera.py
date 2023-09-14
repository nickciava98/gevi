from odoo import fields, models


class Pesiera(models.Model):
    _name = 'gevi_zbilance.pesiera'
    _description = "Pesiera"

    classe = fields.Many2one(
        'gevi_zbilance.classe_pesiera', string='Classe Pesiera',
        required=True, )

    name = fields.Char("Codice Interno")
    # codice_interno = fields.Char("Codice Interno")
    marca = fields.Char("Marca (costruttore)")
    modello = fields.Char("Modello")
    descrizione = fields.Char("Descrizione")
    matricola = fields.Char("Matricola")
    certificato = fields.Char("Certificato")
    scadenza_certificato = fields.Date("Scadenza certificato")
