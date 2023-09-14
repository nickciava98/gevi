from odoo import fields, models
from ..utils import utils


class ClasseStrumento(models.Model):
    _name = 'gevi_zbilance.classe_strumento'
    _description = "Classe Strumento"

    name = fields.Char("Classe strumento")
    campione_massa = fields.Many2one(
        'gevi_zbilance.classe_pesiera', string='Campione di massa',
        required=True, )

    portata = fields.Float("Portata", default=0.00, digits=(12, 2), required=True, )

    um_portata = fields.Selection(
        selection=utils.unita_di_misura,
        string='U. d. M.',
        default=utils.unita_di_misura_default,
        required=True, )

    tipo = fields.Selection(
        [
            ('speciale', 'Speciale'),
            ('fine', 'Fine'),
            ('media', 'Media'),
            ('ordinaria', 'Ordinaria'),
        ],
        string='Tipologia',
        required=True, )
