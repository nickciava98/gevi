# -*- coding: utf-8 -*-
from odoo import fields, models


class ZonaImpianto(models.Model):
    _inherit = 'gevi_zone.zona_impianto'

    child_ids = fields.One2many(
        'gevi_zone.zona_impianto', 'parent_id',
        string="Figli")

    def get_child(self):
        for line in self:
            return line.child_ids
