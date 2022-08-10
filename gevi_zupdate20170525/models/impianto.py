# -*- coding: utf-8 -*-
from openerp import fields, models, api, exceptions


class Impianto(models.Model):
    _inherit = 'gevi.impianti.impianto'

    proprietario_diverso = fields.Boolean(
        string='Proprietario Diverso',
        default=False,
        help="Contrassegnare se il proprietario è diverso dal cliente di fatturazione"
    )

    proprietario_id = fields.Many2one(
        'res.partner',
        domain=[('customer', '=', True)],
        string='Proprietario')

