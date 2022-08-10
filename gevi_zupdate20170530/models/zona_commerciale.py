# -*- coding: utf-8 -*-
from openerp import fields, models, api


class ZonaCommerciale(models.Model):
    _inherit = 'gevi_zone.zona_commerciale'

    child_ids = fields.One2many(
        'gevi_zone.zona_commerciale', 'parent_id',
        string="Figli")

    @api.one
    def get_child(self):
        record = self
        return self.child_ids
