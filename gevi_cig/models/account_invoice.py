# -*- coding: utf-8 -*-
from openerp import fields, models, api
# from openerp.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    codice_cig = fields.Char(string='Codice CIG')

    contratto_id = fields.Many2one('gevi_contratti.contratto', string="Contratto")

    banca_id = fields.Many2one('res.partner.bank', string="Banca d'appoggio")

    @api.one
    @api.onchange('contratto_id')
    def _onchange_contratto_id(self):
        self.codice_cig = self.contratto_id.codice_cig
