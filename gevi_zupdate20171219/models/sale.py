# -*- coding: utf-8 -*-
from openerp import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    verbale_id = fields.Many2one('gevi_verbali.verbale', string='Verbale', ondelete='set null')
