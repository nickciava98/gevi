from odoo import fields, models


class Contratto(models.Model):
    _inherit = 'gevi_contratti.contratto'

    verbale_bilance_ids = fields.One2many('gevi_zbilance.verbale', 'contratto_id', string="Verifiche/Verbali Bilance",
                                          readonly=True)
