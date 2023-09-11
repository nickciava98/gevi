# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    verbale_bilance_id = fields.Many2one('gevi_zbilance.verbale', string='Verbale Bilance', ondelete='cascade')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    verbale_bilance_id = fields.Many2one('gevi_zbilance.verbale', string='Verbale Bilance', ondelete='cascade')
