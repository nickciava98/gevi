from openerp import models, fields, api, _, tools


class CrmLead(models.Model):
    _inherit = ['crm.lead']

    @api.one
    @api.depends('contratto_ids')
    def _get_contratti_total(self):
        active = 0
        # for contratto in self.contratto_ids:
        #     if contratto.state in ('attivo'):
        #         active += 1
        self.contratti_total = len(self.contratto_ids)
        # self.contratti_label = "{total}/{active}".format(total=self.contratti_total,active=active)
        self.contratti_label = "{total}".format(total=self.contratti_total)

    contratti_total = fields.Integer(compute='_get_contratti_total', string="N. Contratti", readonly=True)
    contratti_label = fields.Char(compute='_get_contratti_total', string="Contratti (Active)", readonly=True)

    contratto_ids = fields.One2many('gevi_contratti.contratto', 'opportunity_id', string='Contratti')
