# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class Partner(models.Model):
    _inherit = 'res.partner'

    referente_id = fields.Many2one(
        'gevi_contatti.referente', string="Referente")

    codice_cliente = fields.Char('Codice Cliente', default="/")

    cf = fields.Char('Codice Fiscale', size=16)
    piva = fields.Char('Partita IVA', size=13)
    codice_contabile = fields.Char('Codice Contabile')
    codice_ipa = fields.Char('Codice IPA')
    split_payment = fields.Boolean('Split Payment', default=False)
    tipo_cliente_name = fields.Char('Tipo Cliente Name')
    customer = fields.Boolean(default=True)

    tipo_cliente_id = fields.Many2one('gevi_contatti.contatto_categoria', string='Tipo Cliente', domain=[('tipo', 'ilike', 'cliente')])

    provincia = fields.Char('Provincia', size=2)
    localita = fields.Char('Località')
    regione = fields.Char('Regione')
    comuni_italiani_id = fields.Many2one('comuni_italiani.comune')
    interlocutore = fields.Char('Interlocutore')
    phone2 = fields.Char('Telefono 2')

    # banca_appoggio_id = fields.Many2one('account.journal', string="Banca d'appoggio", domain=[('type', '=', 'bank')])

    # country_id = fields.Many2one('res.country', string="Nazione")

    _defaults = {
        'is_company': True,
        'company_type': 'company',
        'type': 'contact',
    }


     
    def action_doc_pangea(self):
        url = "http://sederm.icoversrl.it/pangea/{0}".format(self.codice_cliente)
        return {
                    'type': 'ir.actions.act_url',
                    'target': 'new',
                    'url': url
                }


     
    @api.onchange('split_payment')
    def _onchange_split_payment(self):
        if self.split_payment is True:
            self.property_account_position_id = self.env['account.fiscal.position'].search([('name', 'ilike', 'Split Payment')], limit=1).id
        else:
            self.property_account_position_id = 0

     
    def _errore_cliente_presente(self):
            return {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name': 'Warning',
                'params': {
                    'title': 'Attenzione!',
                    'text': 'In anagrafica è già presente un cliente con il Fiscale/Partita Iva indicato.',
                    'sticky': True
                }
            }

    #  
    # @api.constrains('cf', 'piva')
    # def controllo_esistenza_cliente(self, cf, piva):
    #     if cf is not None:
    #         cliente_obj = self.env['res.partner'].search(['&', ('cf', '=', cf), ('id', '!=', self.id)])
    #         count = len(cliente_obj.ids)
    #         if count != 0:
    #             raise exceptions.ValidationError('In anagrafica è già presente un cliente con il Codice Fiscale indicato!')
    #     if piva is not None:
    #         cliente_obj = self.env['res.partner'].search(['&', ('piva', '=', piva), ('id', '!=', self.id)])
    #         count = len(cliente_obj.ids)
    #         if count != 0:
    #             raise exceptions.ValidationError('In anagrafica è già presente un cliente con la Partita Iva indicata!')

     
    def write(self, values):
        """
            Update all record(s) in recordset, with new value comes as {values}
            return True on success, False otherwise

            @param values: dict of new values to be set

            @return: True on success, False otherwise
        """
        # self.controllo_esistenza_cliente(values.get('cf'), values.get('piva'))
        result = super(Partner, self).write(values)
        return result

    @api.model
    def create(self, values):
        """
            Create a new record for a model Impianto
            @param values: provides a data for new record
            @return: returns a id of new record
        """
        # self.controllo_esistenza_cliente(values.get('cf'), values.get('piva'))
        values['codice_cliente'] = self.env['ir.sequence'].next_by_code(
            'gevi_contatti.partner')
        result = super(Partner, self).create(values)
        return result

    @api.onchange('comuni_italiani_id')
    def comuni_italiani_change(self):
        self.city = self.comuni_italiani_id.name
        self.zip = self.comuni_italiani_id.cap
        self.provincia = self.comuni_italiani_id.provincia
        self.regione = self.comuni_italiani_id.regione
        # self.country_id = self.env['res.country'].search([('code', '=', 'IT')], limit=1).id

    @api.onchange('piva')
    def onchange_piva(self):
        self.vat = self.piva

    @api.onchange('tipo_cliente_id')
    def _onchange_tipo_cliente(self):
        self.tipo_cliente_name = self.tipo_cliente_id.name
