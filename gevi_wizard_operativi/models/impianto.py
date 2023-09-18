from odoo import models


class Impianto(models.Model):
    _inherit = "gevi.impianti.impianto"

    def open_wizard_carica_attributi_descrittivi(self):
        return self.env["ir.actions.act_window"]._for_xml_id(
            "gevi_wizard_operativi.action_wizard_operativi_carica_attributi_descrittivi"
        )

    def open_wizard_cambio_categoria_impianto(self):
        return self.env["ir.actions.act_window"]._for_xml_id(
            "gevi_wizard_operativi.action_wizard_operativi_cambio_categoria_impianto"
        )
