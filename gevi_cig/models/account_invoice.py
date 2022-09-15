# -*- coding: utf-8 -*-
from odoo import fields, models, api
# from openerp.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    codice_cig = fields.Char()
    contratto_id = fields.Many2one(
        'gevi_contratti.contratto'
    )
    banca_id = fields.Many2one(
        'res.partner.bank',
        string = "Banca d'appoggio"
    )

    @api.onchange('contratto_id')
    def _onchange_contratto_id(self):
        for line in self:
            line.codice_cig = line.contratto_id.codice_cig
