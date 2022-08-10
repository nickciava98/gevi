# -*- coding: utf-8 -*-
from openerp import fields, models, api, exceptions


class Comunicazione(models.Model):
    _name = 'gevi_commerciale.comunicazione'

    name = fields.Char(related='referente_id.name', store=True)

    referente_id = fields.Many2one(
        string='Amministratore',
        required=True,
        default=None,
        help=False,
        comodel_name='gevi_contatti.referente',
        ondelete='set null'
    )

    commerciale_id = fields.Many2one(
        string='Impiegato',
        required=True,
        default=None,
        help=False,
        comodel_name='hr.employee',
        # domain=['|', ('job_id.name', 'ilike', 'Commerciale'), ('job_id.name', 'ilike', 'Agente')],
        ondelete='set null'
    )

    tipo_comunicazione = fields.Selection(
        string='Tipo Comunicazione',
        required=True,
        selection=[('callin', 'Chiamata Ingresso'), ('callout', 'Chiamata Uscita'), ('payin', 'Pagamento Ricevuto')]
    )

    data_comunicazione = fields.Date(
        string='Data Comunicazione',
        required=True,
        default=fields.datetime.now(),
    )

    note = fields.Text(
        string='Note',
        help=False
    )

    @api.model
    def create(self, values):
        result = super(Comunicazione, self).create(values)
        return result
