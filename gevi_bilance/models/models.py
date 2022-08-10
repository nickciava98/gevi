# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

# class gevi_bilance(models.Model):
#     _name = 'gevi_bilance.gevi_bilance'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class Verifica(models.Model):
    _name = 'gevi_bilance.verifica'
    _description = "Gevi Bilance Verifica"
    nomeVerifica = fields.Char()
    numVerifica = fields.Integer()
    description = fields.Text()
    
    anagrafica_id = fields.Many2one('gevi_bilance.anagrafica', ondelete='cascade', string="Anagrafica Bilancia")
