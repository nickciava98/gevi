# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Comunicazione(models.Model):
    _name = 'gevi_commerciale.comunicazione'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Comunicazione"

    name = fields.Char(related='referente_id.name', store=True)

    referente_id = fields.Many2one(
        string='Amministratore',
        required=True,
        default=None,
        help=False,
        comodel_name='gevi_contatti.referente',
        ondelete='cascade'
    )

    commerciale_id = fields.Many2one(
        string='Impiegato',
        required=True,
        default=None,
        help=False,
        comodel_name='hr.employee',
        # domain=['|', ('job_id.name', 'ilike', 'Commerciale'), ('job_id.name', 'ilike', 'Agente')],
        ondelete='cascade'
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

    # @api.model_create_multi
    # def create(self, values):
    #     result = super(Comunicazione, self).create(values)
    #     return result
