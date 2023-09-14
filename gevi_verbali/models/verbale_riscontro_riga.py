# -*- coding: utf-8 -*-
from odoo import fields, models, api


class VerbaleRiscontroRiga(models.Model):
    _name = 'gevi_verbali.verbale_riscontro_riga'
    _description = "Riscontro Riga"

    name = fields.Char(string="Nome")
    verbale_id = fields.Many2one(
        'gevi_verbali.verbale', ondelete='cascade', string="Verbale")

    valore_attributo_id = fields.Many2one(
        'gevi.impianti.valore_attributo',
        string="Valore",
        domain=[('tipo', '=', 'Riscontro')])

    impianto_attributo_riscontro_id = fields.Many2one(
        'gevi.impianti.impianto_attributo_riscontro',
        string="Attributo Riscontro")

    impianto_categoria_id = fields.Many2one(
        'gevi.impianti.impianto_categoria', string="Riscontro")

    @api.onchange('verbale_id')
    def _onchange_verbale_id(self):
        record = self
        self.impianto_categoria_id = record.verbale_id.impianto_categoria_id
        return {
            'domain': {
                'impianto_attributo_riscontro_id': [('impianto_categoria_id', '=', self.impianto_categoria_id)]
            }
        }
