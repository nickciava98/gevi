# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Referente(models.Model):
    _inherit = 'gevi_contatti.referente'

    zona_commerciale_id = fields.Many2one('gevi_zone.zona_commerciale', string="Zona Commerciale", ondelete="cascade")

    #zona_agente_id = fields.Many2one('gevi_zone.zona_agente', string="Zona Agente", ondelete="cascade")
