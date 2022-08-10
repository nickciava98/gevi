# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class Impianto(models.Model):
    _name = 'gevi.impianti.impianto'
    _description = "Impianto"

    # richiesto per openchatter
    _inherit = ['mail.thread']

    name = fields.Char('Nome', default="/")
    etichetta = fields.Char('Etichetta', required=True)
    indirizzo = fields.Char('Via')
    indirizzo2 = fields.Char('Estensione via')
    citta = fields.Char('Citta')
    localita = fields.Char('Località')
    cap = fields.Char('CAP', size=5)
    provincia = fields.Char('Provincia', size=2)
    regione = fields.Char('Regione')
    note_interne = fields.Text('Note Interne')

    comuni_italiani_id = fields.Many2one('comuni_italiani.comune')

    codice_impianto = fields.Char(
        string="Codice Impianto", default="/")

    impianto_categoria_id = fields.Many2one(
        'gevi.impianti.impianto_categoria', string='Categoria Impianto')

    impianto_riga_descrizione_ids = fields.One2many(
        'gevi.impianti.impianto_riga_descrizione', 'impianto_id',
        'Lista Attributi')

    customer_id = fields.Many2one(
        'res.partner',
        ondelete='cascade',
        domain=[('customer', '=', True)],
        string='Cliente Fatturazione',
        required=True)

    data_ultima_verifica = fields.Date("Data Ultima Verifica")

    # flag di utilità per evitare gli attributi duplicati
    attributi_caricati = fields.Boolean(default=False)

    manutentore_id = fields.Many2one('gevi_contatti.manutentore', string="Manutentore")
    cf_cliente = fields.Char(compute='_compute_cliente', store=True)
    piva_cliente = fields.Char(compute='_compute_cliente', store=True)
    referente_name = fields.Char(string="Amministratore", compute='_compute_cliente', store=True)

     
    def copy(self):
        raise exceptions.ValidationError('Duplicazione non consentita')

    # utility action url doc pangea
     
    def action_doc_pangea(self):
        url = "http://sederm.icoversrl.it/pangea/{0}000".format(self.codice_impianto)
        return {
                    'type': 'ir.actions.act_url',
                    'target': 'new',
                    'url': url
                }

    @api.onchange('comuni_italiani_id')
    def comuni_italiani_change(self):
        self.citta = self.comuni_italiani_id.name
        self.cap = self.comuni_italiani_id.cap
        self.provincia = self.comuni_italiani_id.provincia
        self.regione = self.comuni_italiani_id.regione

     
    @api.onchange('customer_id')
    def _onchange_customer_id(self):
        record = self
        # self.name = record.customer_id.name
        self.indirizzo = record.customer_id.street
        self.indirizzo2 = record.customer_id.street2
        self.localita = record.customer_id.localita
        self.cap = record.customer_id.zip
        self.citta = record.customer_id.city
        self.provincia = record.customer_id.provincia
        self.regione = record.customer_id.regione

    #  
    # def write(self, values):
    #     if 'impianto_categoria_id' in values:
    #         self.carica_attributi_descrittivi()
    #     return super(Impianto, self).write(values)

    @api.model
    def create(self, values):
        """
            Create a new record for a model Impianto
            @param values: provides a data for new record

            @return: returns a id of new record
        """
        values['codice_impianto'] = self.env['ir.sequence'].next_by_code(
            'gevi.impianti.impianto')
        values['name'] = values['codice_impianto']
        result = super(Impianto, self).create(values)
        result.carica_attributi_descrittivi()
        return result

     
    def carica_attributi_descrittivi(self):
        for r in self:
            if (r.attributi_caricati is False):
                new_linee_attributo = []
                for linea in r.impianto_categoria_id.impianto_attributo_descrittivo_ids:
                    new_linee_attributo.append([0, 0, {
                        'name': linea.name,
                        'unita_di_misura_id': linea.unita_di_misura_id,
                        }])
                r.attributi_caricati = True
                self.impianto_riga_descrizione_ids = new_linee_attributo

     
    def name_get(self):
        result = super(Impianto, self).name_get()
        res = []
        for record in self:
            name = record.name
            cliente = record.customer_id.name
            etichetta = record.etichetta
            res.append((record.id, cliente + " " + etichetta + " " + name))
        return res

    @api.depends('customer_id')
    def _compute_cliente(self):
        for record in self:
            self.cf_cliente = record.customer_id.cf
            self.piva_cliente = record.customer_id.piva
            self.referente_name = record.customer_id.referente_id.name

    def _delete_attributi_impianto(self):
        for linea in self.impianto_riga_descrizione_ids:
            linea.unlink()

     
    def ricarica_attributi_impianto(self):
        self.attributi_caricati = False
        # riga sottostante cancella tutti gli attributi descrittivi dell'impianto
        self._delete_attributi_impianto()
        self.carica_attributi_descrittivi()

