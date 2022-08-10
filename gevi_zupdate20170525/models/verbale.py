# -*- coding: utf-8 -*-
from openerp import fields, models, api, exceptions


class Verbale(models.Model):
    _inherit = 'gevi_verbali.verbale'

    prioritario = fields.Boolean(
        string='Urgente',
        default=False,
        help="Contrassegnare se verifica urgente"
    )

    tipo_attivita = fields.Char('Tipo attivita')

    periodicita = fields.Selection(
        'gelab.contratto', string="Periodicità", related='contratto_id.periodicita_verifica', store=True)

    utente_assegnato_referente_id = fields.Many2one(
        string='Utente Assegnato ad Amministratore',
        readonly=True,
        comodel_name='res.users',
        related='referente_id.utente_assegnato_id',
        store=True
    )

