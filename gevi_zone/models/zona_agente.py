# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ZonaAgente(models.Model):
    _name = 'gevi_zone.zona_agente'

    name = fields.Char(string="Nome")
    parent_id = fields.Many2one(
        'gevi_zone.zona_agente',
        string="Zona Agente padre",
        ondelete="cascade")
    agente_id = fields.Many2one(
        'hr.employee',
        string="Agente",
        domain=[('job_id.name', 'ilike', "Agente")])

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from gevi_zone_zona_agente where id IN %s', (tuple(ids), ))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

    _constraints = [
        (_check_recursion, 'Attenzione! Non è possibile creare zone ricorsive.', ['parent_id']),
        ('agente_id_unique', 'UNIQUE(agente_id)', "Una zona agente può essere assegnata ad un solo agente"),
    ]