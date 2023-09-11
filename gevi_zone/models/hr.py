# -*- coding: utf-8 -*-
from odoo import fields, models


class Employee(models.Model):
    _inherit = 'hr.employee'

    # zona_agente_ids = fields.One2many(
    #     'gevi_zone.zona_agente', 'agente_id', string="Zone Agente")
    zona_commerciale_ids = fields.One2many(
        'gevi_zone.zona_commerciale', 'commerciale_id', string="Zone Commerciali")
    zona_responsabile_tecnico_ids = fields.One2many(
        'gevi_zone.zona_impianto', 'responsabile_tecnico_id', string="Zone Impianto RT")
    zona_ispettore_ids = fields.One2many(
        'gevi_zone.zona_impianto', 'ispettore_id', string="Zone Impianto ISP")

    qualifica = fields.Char(related='job_id.name', store=False, string="Qualifica")

    # has_zona_impianto = fields.Boolean(default="False", compute='_zone_qualifica')
    # has_zona_commerciale = fields.Boolean(default="False", compute='_zone_qualifica')
    # has_zona_agente = fields.Boolean(default="False", compute='_zone_qualifica')

    # @api.one
    # @api.depends('qualifica')
    # def _zone_qualifica(self):
    #     record = self
    #     if not record[id].qualifica:
    #         pass
    #     else:
    #         if "Ispettore".upper() in record[id].qualifica.upper():
    #             self.has_zona_impianto = True
    #         if "Responsabile Tecnico".upper() in record[id].qualifica.upper():
    #             self.has_zona_impianto = True
    #         if "Commerciale".upper() in record[id].qualifica.upper():
    #             self.has_zona_commerciale = True
    #         if "Agente".upper() in record[id].qualifica.upper():
    #             self.has_zona_agente = True

    # aggiungere per una zona ad uno solo agente , domain=[('agente_id','=', False)]
