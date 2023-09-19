# -*- coding: utf-8 -*-
from odoo import fields, models, api


class VerbaleRaccomandazioneRiga(models.Model):
    _name = 'gevi_verbali.verbale_raccomandazione_riga'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Raccomandazione Riga"

    name = fields.Char(string="Specifica")
    verbale_id = fields.Many2one(
        'gevi_verbali.verbale', ondelete='cascade', string="Verbale")
    raccomandazione_id = fields.Many2one(
        'gevi_verbali.raccomandazione', string="Raccomandazione")

    vincolante = fields.Boolean(string="Vincolante")

    @api.onchange('raccomandazione_id')
    def _onchange_vincolante(self):
        record = self
        self.vincolante = record.raccomandazione_id.vincolante
        self.name = record.raccomandazione_id.name
