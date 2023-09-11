# -*- coding: utf-8 -*-
from odoo import fields, models


class ImpiantoCategoria(models.Model):
    _name = 'gevi.impianti.impianto_categoria'
    _description = "Impianto Categoria"

    name = fields.Char(string='name', required=True)
    descrizione = fields.Char(string='Descrizione', required=False)
    codice_categoria = fields.Char(string='Codice Categoria', required=True)

    impianto_attributo_descrittivo_ids = fields.One2many(
        'gevi.impianti.impianto_attributo_descrittivo',
        'impianto_categoria_id',
        string="Lista Attributi")

    impianto_attributo_riscontro_ids = fields.One2many(
        'gevi.impianti.impianto_attributo_riscontro',
        'impianto_categoria_id',
        string="Lista Riscontri")

    impianto_attributo_rilievo_ids = fields.One2many(
        'gevi.impianti.impianto_attributo_rilievo',
        'impianto_categoria_id',
        string="Lista Rilievi")

    impianto_attributo_rilievo_mat_ids = fields.One2many(
        'gevi.impianti.impianto_attributo_rilievo_mat',
        'impianto_categoria_id',
        string="Lista Rilievi MAT")
