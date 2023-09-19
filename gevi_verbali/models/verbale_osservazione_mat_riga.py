# -*- coding: utf-8 -*-
from odoo import fields, models, api


class VerbaleOsservazioneMatRiga(models.Model):
    _name = 'gevi_verbali.verbale_osservazione_mat_riga'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Osservazione MaT Riga"

    name = fields.Char(string="Specifica")
    verbale_id = fields.Many2one(
        'gevi_verbali.verbale', ondelete='cascade', string="Verbale")
    osservazione_id = fields.Many2one(
        'gevi_verbali.osservazione_mat', string="Osservazione")

    vincolante = fields.Boolean(string="Vincolante")

    @api.onchange('osservazione_id')
    def _onchange_vincolante(self):
        record = self
        self.vincolante = record.osservazione_id.vincolante
        self.name = record.osservazione_id.name
