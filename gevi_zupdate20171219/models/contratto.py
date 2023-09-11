# -*- coding: utf-8 -*-
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Contratto(models.Model):
    _inherit = 'gevi_contratti.contratto'

    zona_commerciale_referente_id = fields.Many2one(
        string='Zona Amministratore',
        readonly=True,
        comodel_name='gevi_zone.zona_commerciale',
        related='referente_id.zona_commerciale_id',
        store=True
    )

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
        related='customer_id.tipo_cliente_id',
        store=True
    )

# state = fields.Selection(selection_add=[('disdetta_uv', 'Disdetta UV')])
