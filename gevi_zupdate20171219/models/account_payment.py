# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class account_payment(models.Model):
    _inherit = "account.payment"

    referente_id = fields.Many2one(
        string='Amministratore',
        readonly=True,
        comodel_name='gevi_contatti.referente',
        related='partner_id.referente_id',
        store=True
    )

    zona_commerciale_referente_id = fields.Many2one(
        string='Zona Amministratore',
        readonly=True,
        comodel_name='gevi_zone.zona_commerciale',
        related='referente_id.zona_commerciale_id',
        store=True
    )

    tipo_cliente_id = fields.Many2one(
        string='Tipo Cliente',
        readonly=True,
        comodel_name='gevi_contatti.contatto_categoria',
        related='partner_id.tipo_cliente_id',
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

