# -*- coding: utf-8 -*-
from datetime import timedelta
from openerp import fields, models, api, exceptions


class Appuntamento(models.Model):
    _name = 'gevi_commerciale.appuntamento'

    name = fields.Char('Memo')

    esito = fields.Selection(
        string='Esito',
        required=True,
        selection=[('in_corso', 'In Corso'),('ok', 'OK'), ('ko', 'KO')], default='in_corso'
    )

    referente_id = fields.Many2one(
        string='Amministratore',
        required=False,
        default=None,
        help=False,
        comodel_name='gevi_contatti.referente',
        ondelete='set null'
    )

    commerciale_id = fields.Many2one(
        string='Utente',
        required=True,
        default=lambda self: self._compute_default_commerciale(),
        help=False,
        comodel_name='hr.employee',
        # domain=['|', ('job_id.name', 'ilike', 'Commerciale'), ('job_id.name', 'ilike', 'Agente')],
        ondelete='set null'
    )

    inizio_appuntamento = fields.Datetime(
        string='Inizio appuntamento',
        required=True,
        readonly=False,
        index=False,
        default=fields.datetime.now(),
        help=False
    )

    can_edit_commerciale = fields.Boolean(
        default=lambda self: self._compute_default_can_edit_commerciale(),
#        compute=_compute_can_edit_commerciale,
    )

    fine_appuntamento = fields.Datetime(
        string="Fine appuntamento",
        required=True
    )

    note = fields.Text(
        string='Note',
        help=False
    )

    durata = fields.Float(
        string='Durata',
        default=3600.0,
        digits=(10, 2)
    )

    @api.model
    def _compute_default_can_edit_commerciale(self):
        return self.env.user.has_group('__export__.res_groups_78')

    @api.one
    @api.onchange('referente_id')
    def onchange_referente(self):
        self.name = self.referente_id.name


    @api.one
    @api.onchange('inizio_appuntamento')
    def onchange_inizio_appuntamento(self):
        start = fields.Datetime.from_string(self.inizio_appuntamento)
        duration = timedelta(seconds=3600)
        self.fine_appuntamento = start + duration

    @api.model
    def create(self, values):
        # values['utente_id'] = self.env.uid
        result = super(Appuntamento, self).create(values)
        return result

    @api.model
    def _compute_default_commerciale(self):
        utente_corrente = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit = 1)
        return utente_corrente.id

