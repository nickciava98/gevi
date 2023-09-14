# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ZonaImpianto(models.Model):
    _name = 'gevi_zone.zona_impianto'
    _description = "Zona Impianto"

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

    @api.constrains("parent_id")
    def _constrains_parent_id(self):
        for line in self:
            if line.parent_id.id in self.search([("parent_id", "!=", False)]).ids:
                raise ValidationError("Attenzione! Non è possibile creare zone ricorsive.")
