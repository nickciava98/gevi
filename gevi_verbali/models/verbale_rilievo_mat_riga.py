# -*- coding: utf-8 -*-
from odoo import fields, models, api


class VerbaleRilievoMatRiga(models.Model):
    _name = 'gevi_verbali.verbale_rilievo_mat_riga'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Rilievo MaT Riga"

    name = fields.Char(string="Nome")
    note_rilievo = fields.Char(string="Note")

    verbale_id = fields.Many2one(
        'gevi_verbali.verbale', ondelete='cascade', string="Verbale")

    valore_attributo_id = fields.Many2one(
        'gevi.impianti.valore_attributo',
        string="Verificato",
        domain=[('tipo', '=', 'Rilievo')])

    impianto_attributo_rilievo_id = fields.Many2one(
        'gevi.impianti.impianto_attributo_rilievo_mat',
        string="Attributo Rilievo")

    impianto_categoria_id = fields.Many2one(
        'gevi.impianti.impianto_categoria', string="Rilievo")

    @api.onchange('verbale_id')
    def _onchange_verbale_id(self):
        record = self
        self.impianto_categoria_id = record.verbale_id.impianto_categoria_id
        return {
            'domain': {
                'impianto_attributo_rilievo_id': [('impianto_categoria_id', '=', self.impianto_categoria_id)]
            }
        }
