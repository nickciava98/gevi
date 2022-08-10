# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ZonaImpianto(models.Model):
    _name = 'gevi_zone.zona_impianto'

    name = fields.Char(string="Nome")
    parent_id = fields.Many2one(
        'gevi_zone.zona_impianto', string="Zona Impianto padre", ondelete="cascade")
    ispettore_id = fields.Many2one(
        'hr.employee',
        string="Ispettore",
        domain=[('job_id.name', 'ilike', "Ispettore")])
    responsabile_tecnico_id = fields.Many2one(
        'hr.employee',
        string="Responsabile Tecnico",
        domain=[('job_id.name', 'ilike', "Responsabile Tecnico")])

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from gevi_zone_zona_impianto where id IN %s', (tuple(ids), ))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

    _constraints = [
        (_check_recursion, 'Attenzione! Non è possibile creare zone ricorsive.', ['parent_id']),
    ]
