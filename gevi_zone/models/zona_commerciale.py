# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ZonaCommerciale(models.Model):
    _name = 'gevi_zone.zona_commerciale'
    _description = "Zona Commerciale"

    name = fields.Char(string="Nome")
    parent_id = fields.Many2one(
        'gevi_zone.zona_commerciale', string="Zona Commerciale padre", ondelete="cascade")
    commerciale_id = fields.Many2one(
        'hr.employee',
        string="Commerciale",
        domain=[('job_id.name', 'ilike', "Commerciale")])

    @api.constrains("parent_id")
    def _constrains_parent_id(self):
        for line in self:
            if line.parent_id.id in self.search([("parent_id", "!=", False)]).ids:
                raise ValidationError("Attenzione! Non è possibile creare zone ricorsive.")
