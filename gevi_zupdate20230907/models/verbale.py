from odoo import models, fields, api


class Verbale(models.Model):
    _inherit = "gevi_verbali.verbale"

    locali_medici = fields.Boolean(
        default=False,
        string="Locali Medici"
    )
    gruppo_0 = fields.Boolean(
        default=False,
        string="Gruppo 0"
    )
    gruppo_1 = fields.Boolean(
        default=False,
        string="Gruppo 1"
    )
    gruppo_2 = fields.Boolean(
        default=False,
        string="Gruppo 1"
    )
    studio_medico_generico = fields.Boolean(
        default=False,
        string="Studio Medico Generico"
    )
    sala_massaggi = fields.Boolean(
        default=False,
        string="Sala Massaggi"
    )
    ambulatorio = fields.Boolean(
        default=False,
        string="Ambulatorio"
    )
    altro_gruppo_0 = fields.Char(
        string="Altro (Gruppo 0)"
    )
    veterinario = fields.Boolean(
        default=False,
        string="Veterinario"
    )
    studio_dentistico = fields.Boolean(
        default=False,
        string="Studio Dentistico"
    )
    sala_fisioterapica = fields.Boolean(
        default=False,
        string="Sala Fisioterapica"
    )
    dentista = fields.Boolean(
        default=False,
        string="Dentista"
    )
    altro_gruppo_1 = fields.Char(
        string="Altro (Gruppo 1)"
    )
    sala_operatoria = fields.Boolean(
        default=False,
        string="Sala Operatoria"
    )
    altro_gruppo_2 = fields.Char(
        string="Altro (Gruppo 2)"
    )
    rilievi_ambiente = fields.Text(
        string="Rilievi Ambiente"
    )

    @api.onchange("locali_medici")
    def _onchange_locali_medici(self):
        for verbale in self:
            if not verbale.locali_medici:
                verbale.gruppo_0 = verbale.studio_medico_generico = verbale.sala_massaggi = verbale.ambulatorio \
                    = verbale.altro_gruppo_0 = verbale.gruppo_1 = verbale.veterinario = verbale.studio_dentistico \
                    = verbale.sala_fisioterapica = verbale.dentista = verbale.altro_gruppo_1 = verbale.gruppo_2 \
                    = verbale.sala_operatoria = verbale.altro_gruppo_2 = verbale.rilievi_ambiente = False

    @api.onchange("gruppo_0")
    def _onchange_gruppo_0(self):
        for verbale in self:
            if not verbale.gruppo_0:
                verbale.studio_medico_generico = verbale.sala_massaggi = verbale.ambulatorio \
                    = verbale.altro_gruppo_0 = False

    @api.onchange("gruppo_1")
    def _onchange_gruppo_1(self):
        for verbale in self:
            if not verbale.gruppo_1:
                verbale.veterinario = verbale.studio_dentistico = verbale.sala_fisioterapica = verbale.dentista \
                    = verbale.altro_gruppo_1 = False

    @api.onchange("gruppo_2")
    def _onchange_gruppo_2(self):
        for verbale in self:
            verbale.sala_operatoria = verbale.altro_gruppo_2 = False
