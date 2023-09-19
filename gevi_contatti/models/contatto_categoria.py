# -*- coding: utf-8 -*-
from odoo import fields, models


class ContattoCategoria(models.Model):
    _name = 'gevi_contatti.contatto_categoria'
    _description = "Categoria di contatto"

    # richiesto per openchatter
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()

    tipo = fields.Selection(
        [
            ('da_selezionare', 'Da Selezionare'),
            ('cliente', 'Cliente'),
            ('referente', 'Amministratore'),
            ('manutentore', 'Manutentore'),
        ],
        default='da_selezionare')
