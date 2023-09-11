# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ZonaCommerciale(models.Model):
    _inherit = 'gevi_zone.zona_commerciale'

    child_ids = fields.One2many(
        'gevi_zone.zona_commerciale', 'parent_id',
        string="Figli")

    def get_child(self):
        for line in self:
            return line.child_ids
