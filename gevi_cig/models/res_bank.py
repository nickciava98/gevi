# -*- coding: utf-8 -*-
from odoo import models


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    def name_get(self):
        result = super(ResPartnerBank, self).name_get()
        res = []
        for record in self:
            res.append((record.id, record.bank_name + " " + record.acc_number))
        return res
