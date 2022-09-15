# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class Verbale(models.Model):
    _inherit = 'gevi_verbali.verbale'

    agente_referente_id = fields.Many2one(
            string='Agente Amministratore',
            readonly=True,
            comodel_name='hr.employee',
            related='referente_id.agente_id',
            store=True
        )
