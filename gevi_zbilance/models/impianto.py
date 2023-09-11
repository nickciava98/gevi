from odoo import fields, models


class Impianto(models.Model):
    # _name = 'gevi_zbilance.bilancia'
    _inherit = 'gevi.impianti.impianto'

    descrizione_categoria_impianto = fields.Char(string='Codice Categoria', related='impianto_categoria_id.descrizione',
                                                 readonly=True, store=True)

    # required gestito nella vista
    tipologia_bilancia = fields.Selection(
        [
            ('elettronica', 'Elettronica'),
            ('analogica', 'Analogica (semi-automatica)'),
            ('Meccanica', 'Meccanica (non automatica)'),
        ],
        string='Tipologia',
        required=False, )

    verbale_bilance_ids = fields.One2many('gevi_zbilance.verbale', 'impianto_id', string="Verifiche/Verbali Bilance",
                                          readonly=True)

    # range [almeno 1, massimo 3] (Pmin, Pmax, e, d)
    # required per range 1 gestito nella vista
    range_1 = fields.Many2one(
        'gevi_zbilance.range_bilancia', string='Range 1',
        required=False, )
    range_2 = fields.Many2one(
        'gevi_zbilance.range_bilancia', string='Range 2',
        required=False, )
    range_3 = fields.Many2one(
        'gevi_zbilance.range_bilancia', string='Range 3',
        required=False, )

    # classe (divisioni, classe della bilancia, classe masse)
    # required gestito nella vista
    classe_bilancia = fields.Many2one(
        'gevi_zbilance.classe_pesiera', string='Classe massa',
        required=False, )

    # metodi common

    def apri_verbale_bilance(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Verbale',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': id[0],
            'target': 'current',
        }
