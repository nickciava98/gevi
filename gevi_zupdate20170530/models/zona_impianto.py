# -*- coding: utf-8 -*-
from openerp import fields, models, api


class ZonaImpianto(models.Model):
    _inherit = 'gevi_zone.zona_impianto'

    child_ids = fields.One2many(
        'gevi_zone.zona_impianto', 'parent_id',
        string="Figli")

    @api.one
    def get_child(self):
        record = self
        return self.child_ids
