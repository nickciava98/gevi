# -*- coding: utf-8 -*-
from odoo import fields, models, api


class NormeAscensori(models.Model):
    _name = 'gevi_verbali.normeascensori'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Norme collaudo ascensori"

    name = fields.Char('Nome', default="/", readonly=True)
    impianto_categoria_id = fields.Many2one(
        'gevi.impianti.impianto_categoria', string='Categoria Impianto')
    anno_inizio = fields.Integer("Anno Inizio Norma")
    anno_fine = fields.Integer("Anno Fine Norma")
    norma_collaudo = fields.Char('Norma Collaudo', default="/", required=True)
    norma_straordinaria = fields.Char('Norma Straordinaria', default="/", required=True)

    @api.model_create_multi
    def create(self, values):
        result = super(NormeAscensori, self).create(values)
        result.name = result.norma_collaudo + " - " + result.norma_straordinaria

        return result

    def write(self, values):
        if 'norma_collaudo' in values or 'norma_straordinaria' in values:
            values['name'] = values['norma_collaudo'] + " - " + values['norma_straordinaria']
        return super(NormeAscensori, self).write(values)
