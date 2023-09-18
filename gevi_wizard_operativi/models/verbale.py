from odoo import models


class Verbale(models.Model):
    _inherit = "gevi_verbali.verbale"

    def open_wizard_cambio_categoria_impianto(self):
        return self.env.ref("gevi_wizard_operativi.cambio_categoria_impianto_verbale_action_server")
