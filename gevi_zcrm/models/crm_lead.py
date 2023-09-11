from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = ['crm.lead']

    @api.depends('contratto_ids')
    def _get_contratti_total(self):
        for line in self:
            active = 0
            # for contratto in self.contratto_ids:
            #     if contratto.state in ('attivo'):
            #         active += 1
            line.contratti_total = len(line.contratto_ids)
            # self.contratti_label = "{total}/{active}".format(total=self.contratti_total,active=active)
            line.contratti_label = "{total}".format(total=line.contratti_total)

    contratti_total = fields.Integer(compute='_get_contratti_total', string="N. Contratti", readonly=True)
    contratti_label = fields.Char(compute='_get_contratti_total', string="Contratti (Active)", readonly=True)

    contratto_ids = fields.One2many('gevi_contratti.contratto', 'opportunity_id', string='Contratti')
