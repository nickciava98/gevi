from odoo import fields, models
from ..utils import utils


class RangeBilancia(models.Model):
    _name = 'gevi_zbilance.range_bilancia'

    p_min = fields.Float("(Pmin) Portata minima", default=0.00, digits=(12, 2), required=True, )
    p_max = fields.Float("(Pmax) Portata massima", default=0.00, digits=(12, 2), required=True, )
    e_divisione_verifica = fields.Float("(e) Divisione diverifica", default=0.00, digits=(12, 2), required=True, )
    d_divisione_minima = fields.Float("(d) Divisione minima", default=0.00, digits=(12, 2), required=True, )

    um_range = fields.Selection(
        selection=utils.unita_di_misura,
        string='UdM Portata',
        default=utils.unita_di_misura_default,
        required=True, )

    def name_get(self):
        result = super(RangeBilancia, self).name_get()
        res = []
        for record in self:
            p_min = record.p_min
            p_max = record.p_max
            um_range = record.um_range
            res.append((record.id, "{0} - {1} [{2}] ".format(p_min, p_max, um_range)))
        return res
