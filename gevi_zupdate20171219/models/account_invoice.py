# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    tipo_referente_id = fields.Many2one(
        string='Tipo Amministratore',
        readonly=True,
        comodel_name='gevi_contatti.contatto_categoria',
        related='referente_id.tipo_referente_id',
        store=True
    )

    tipo_cliente_id = fields.Many2one(
        string='Tipo Cliente',
        readonly=True,
        comodel_name='gevi_contatti.contatto_categoria',
        related='commercial_partner_id.tipo_cliente_id',
        store=True
    )

    utente_referente_id = fields.Many2one(
        string='Utente Amministratore',
        readonly=True,
        comodel_name='res.users',
        related='referente_id.utente_assegnato_id',
        store=True
    )

    agente_referente_id = fields.Many2one(
        string='Agente Amministratore',
        readonly=True,
        comodel_name='hr.employee',
        related='referente_id.agente_id',
        store=True
    )

