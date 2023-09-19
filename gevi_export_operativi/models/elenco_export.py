# -*- coding: utf-8 -*-
from odoo import fields, models


# from openerp.tools.translate import _


class ElencoEsportazioni(models.Model):
    _name = "gevi_export_operativi.elenco_esportazioni"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Elenco Esportazioni"
    _order = "create_date desc"

    name = fields.Char('Nome', size=64)
    excel_file = fields.Binary('Dowload File Excel')
    file_name = fields.Char('Excel File', size=64)
    tipo = fields.Char('Tipo Esportazione', size=64)
