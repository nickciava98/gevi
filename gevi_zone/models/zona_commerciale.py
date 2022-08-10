# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ZonaCommerciale(models.Model):
    _name = 'gevi_zone.zona_commerciale'

    name = fields.Char(string="Nome")
    parent_id = fields.Many2one(
        'gevi_zone.zona_commerciale', string="Zona Commerciale padre", ondelete="cascade")
    commerciale_id = fields.Many2one(
        'hr.employee',
        string="Commerciale",
        domain=[('job_id.name', 'ilike', "Commerciale")])

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from gevi_zone_zona_commerciale where id IN %s', (tuple(ids), ))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

    _constraints = [
        (_check_recursion, 'Attenzione! Non è possibile creare zone ricorsive.', ['parent_id']),
    ]
