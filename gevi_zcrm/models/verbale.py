from odoo import fields, models, api


class Verbale(models.Model):
    _inherit = 'gevi_verbali.verbale'

    def _crea_ordine_vendita(self):
        for line in self:
            odvs = super(Verbale, self)._crea_ordine_vendita()
            odv = odvs[0]

            values = dict()
            if line.contratto_id.opportunity_id:
                values['opportunity_id'] = line.contratto_id.opportunity_id.id
            if line.contratto_id.team_id:
                values['team_id'] = line.contratto_id.team_id.id

            odv.write(values)
            return odv
