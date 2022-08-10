from openerp import fields, models, api, exceptions


class Contratto(models.Model):
    _name = "gevi_contratti.contratto"
    _inherit = 'gevi_contratti.contratto'

    opportunity_id = fields.Many2one('crm.lead', 'Opportunity', domain="[('type', '=', 'opportunity')]")
    team_id = fields.Many2one('crm.team', 'Sales Team', oldname='section_id')

    # @api.multi
    # def action_first_attivo(self):
    #     if not self.impianto_id:
    #         raise exceptions.ValidationError("Associare l'impianto prima di attivare il contratto.")
    #     self._aggiorna_da_create()
    #     self._crea_verifica_periodica()
    #     self.state = 'attivo'

    # @api.multi
    # def action_onchange(self):
    #     self.write({'customer_id': self.customer_id.id})
    #     return self._onchange_customer_id()

    # @api.one
    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(Contratto, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #
    #     if view_type == 'form':
    #
    #         if 'view_type' in self._context['params'] and self._context['params']['view_type'] == 'form':
    #             lista_impianti = []
    #             id_from_form = self._context['params']['id']
    #             impianto_obj = self.env['gevi.impianti.impianto']
    #             contratto_obj = self.env['gevi_contratti.contratto'].search([('id', '=', id_from_form)])
    #             impianti_ids = impianto_obj.search([('customer_id', '=', contratto_obj.customer_id.id)])
    #             c_impianto_ids = contratto_obj.customer_id.impianto_ids.ids
    #             for record in impianti_ids:
    #                 lista_impianti.append(record.id)
    #             res['fields']['impianto_id']['domain'] = [('id', 'in', lista_impianti)]
    #         else:
    #             doc = etree.XML(res['arch'])
    #             # for field in res['fields']:
    #             for node in doc.xpath("//field[@name='impianto_id']"):
    #                 node.set("domain", "[('customer_id', '=', customer_id)]")
    #             res['arch'] = etree.tostring(doc)
    #     return res

