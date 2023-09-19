# -*- coding: utf-8 -*-
from odoo import fields, models, api


class VerbaleRilievoRiga(models.Model):
    _name = 'gevi_verbali.verbale_rilievo_riga'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Rilievo Riga"

    name = fields.Char(string="Nome")
    valore_rilievo = fields.Float(string="Valore Rilievo", digits=(10, 2))
    note_rilievo = fields.Char(string="Note")
    impianto_categoria_name = fields.Char(compute='_compute_impianto_categoria_id', string="Categoria Impianto Name",
                                          store=True)

    verbale_id = fields.Many2one(
        'gevi_verbali.verbale', ondelete='cascade', string="Verbale")

    valore_attributo_id = fields.Many2one(
        'gevi.impianti.valore_attributo',
        string="Verificato",
        domain=[('tipo', '=', 'Rilievo')])

    impianto_attributo_rilievo_id = fields.Many2one(
        'gevi.impianti.impianto_attributo_rilievo',
        string="Attributo Rilievo")

    impianto_categoria_id = fields.Many2one(
        'gevi.impianti.impianto_categoria', string="Rilievo")

    unita_di_misura_id = fields.Many2one(
        'gevi.impianti.unita_di_misura',
        string="Unità di misura")

    @api.onchange('verbale_id')
    def _onchange_verbale_id(self):
        record = self
        self.impianto_categoria_id = record.verbale_id.impianto_categoria_id
        return {
            'domain': {
                'impianto_attributo_rilievo_id': [('impianto_categoria_id', '=', self.impianto_categoria_id)]
            }
        }

    @api.depends('impianto_categoria_id')
    def _compute_impianto_categoria_id(self):
        for line in self:
            line.impianto_categoria_name = line.impianto_categoria_id.name
