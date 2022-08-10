# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    zona_commerciale_id = fields.Many2one('gevi_zone.zona_commerciale', string="Zona Commerciale", ondelete="cascade")
