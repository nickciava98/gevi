# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    verbale_id = fields.Many2one('gevi_verbali.verbale', string='Verbale', ondelete='cascade')
