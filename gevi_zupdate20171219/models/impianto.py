# -*- coding: utf-8 -*-
from openerp import fields, models, api, exceptions


class Impianto(models.Model):
    _inherit = 'gevi.impianti.impianto'

    verbali_ids = fields.One2many(
        string=u'Verbali',
        comodel_name='gevi_verbali.verbale',
        inverse_name='impianto_id',
    )

    @api.multi
    def apri_verbale(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Verbale', 
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': id[0],
            'target': 'current',
        }
