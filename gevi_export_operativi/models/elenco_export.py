# -*- coding: utf-8 -*-
from odoo import fields, models, api
# from openerp.tools.translate import _


class ElencoEsportazioni(models.Model):
    _name = "gevi_export_operativi.elenco_esportazioni"
    _order = "create_date desc"

    name = fields.Char('Nome', size=64)
    excel_file = fields.Binary('Dowload File Excel')
    file_name = fields.Char('Excel File', size=64)
    tipo = fields.Char('Tipo Esportazione', size=64)
