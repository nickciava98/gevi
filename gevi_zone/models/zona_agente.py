# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ZonaAgente(models.Model):
    _name = 'gevi_zone.zona_agente'
    _description = "Zona Agente"

    name = fields.Char(string="Nome")
    parent_id = fields.Many2one(
        'gevi_zone.zona_agente',
        string="Zona Agente padre",
        ondelete="cascade")
    agente_id = fields.Many2one(
        'hr.employee',
        string="Agente",
        domain=[('job_id.name', 'ilike', "Agente")])

    @api.constrains("parent_id")
    def _constrains_parent_id(self):
        for line in self:
            if line.parent_id.id in self.search([("parent_id", "!=", False)]).ids:
                raise ValidationError("Attenzione! Non è possibile creare zone ricorsive.")

    _sql_constraints = [
        ('agente_id_unique', 'UNIQUE(agente_id)', "Una zona agente può essere assegnata ad un solo agente"),
    ]
