# -*- coding: utf-8 -*-
from openerp import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    referente_id = fields.Many2one(
        string='Amministratore',
        readonly=True,
        comodel_name='gevi_contatti.referente',
        related='commercial_partner_id.referente_id',
        store=True
    )

    zona_commerciale_referente_id = fields.Many2one(
        string='Zona Commerciale',
        readonly=True,
        comodel_name='gevi_zone.zona_commerciale',
        related='referente_id.zona_commerciale_id',
        store=True
    )
