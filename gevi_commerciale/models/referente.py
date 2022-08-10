# -*- coding: utf-8 -*-
from openerp import fields, models, api, exceptions


class Referente(models.Model):
    _inherit = 'gevi_contatti.referente'

    verbale_ids = fields.One2many(
        string='Verbali',
        comodel_name='gevi_verbali.verbale',
        inverse_name='referente_id',
    )

    appuntamento_ids = fields.One2many(
        string='Appuntamenti',
        comodel_name='gevi_commerciale.appuntamento',
        inverse_name='referente_id',
    )

    comunicazione_ids = fields.One2many(
        string='Comunicazioni',
        comodel_name='gevi_commerciale.comunicazione',
        inverse_name='referente_id',
    )
