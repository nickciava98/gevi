from openerp import fields, models, api


class Verbale(models.Model):
    _inherit = 'gevi_verbali.verbale'

    @api.one
    def _crea_ordine_vendita(self):
        odvs = super(Verbale, self)._crea_ordine_vendita()
        odv = odvs[0]

        values = dict()
        if self.contratto_id.opportunity_id:
            values['opportunity_id'] = self.contratto_id.opportunity_id.id
        if self.contratto_id.team_id:
            values['team_id'] = self.contratto_id.team_id.id

        odv.write(values)
        return odv
