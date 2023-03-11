# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions
from lxml import etree

import logging
_logger = logging.getLogger(__name__)


class Contratto(models.Model):
    _name = 'gevi_contratti.contratto'

    name = fields.Char('Nome', default="/", readonly=True)
    codice_contratto = fields.Char(
        string='Codice Contratto',
        readonly=True,
        default="/", )

    impianto_categoria_id = fields.Many2one(
        'gevi.impianti.impianto_categoria', string='Categoria Impianto')

    verifica_periodica = fields.Boolean('Verifica Periodica', default=False)
    verifica_straordinaria = fields.Boolean(
        'Verifica Straordinaria', default=False)

    altre_norme = fields.Char('Altre norme')

    modalita_pagamento_id = fields.Many2one('account.payment.term', string="Modalità di Pagamento")

    durata_contratto = fields.Selection(
            [
                ('1', 'Una Verifica'),
                ('2', 'Due Verifiche'),
                ('-1', 'Senza Scadenza'),
            ],
            required=True,
            string="Durata del Contratto")

    referente_id = fields.Many2one(
        'gevi_contatti.referente', string="Referente", required=True)
    # #riga seguente per aggiornare in automatico l'agente in base alla zona assegnata'
    # #agente_id = fields.Many2one('res.users', string="Agente", domain=[('zona','=',referente_id.zona)])

    cliente_name = fields.Char(
        compute='_compute_impianto_ubicazione', string="Denominazione Cliente", store=False)

    customer_id = fields.Many2one(
        'res.partner',
        ondelete='cascade',
        #domain=[('customer', '=', True)],
        string='Cliente Fatturazione',
        required=True)

    # Cerca cliente per Codice Fiscale e Partita Iva
    # cliente_cf_piva = fields.Char('Cerca Cliente per Cod.Fiscale e P.Iva')

    impianto_id = fields.Many2one(
        'gevi.impianti.impianto',
        string="Impianto",
        required=False,
    )
    manutentore_id = fields.Many2one(
        'gevi_contatti.manutentore', string="Manutentore")

    campi_validati = fields.Boolean(compute='_valida_campi', string="Verifica Periodica/Straordinaria", store=False, default=False, required=True)

    data_ultima_verifica = fields.Date('Data Ultima Verifica')

    costo_verifica_periodica = fields.Float(
        default=0.00,
        digits=(12, 2),
        string="Costo Verifica Periodica €",
        help="Costo Verifica Periodica più IVA")

    costo_verifica_straordinaria = fields.Float(
        default=0.00,
        digits=(12, 2),
        string="Costo Verifica Straordinaria €",
        help="Costo Verifica Straordinaria più IVA")

    valore_contratto = fields.Float(compute='_compute_valore_contratto', store=True)

    data_stipula = fields.Date(
        'Data Stipula Contratto', default=fields.Date.today, required=True)

    codice_cig = fields.Char('Codice Identificativo Gara (CIG)')

    cliente_cf = fields.Char(
        compute='_compute_dati_cliente', store=False)
    cliente_piva = fields.Char(
        compute='_compute_dati_cliente', store=False)
    cliente_tipo = fields.Char(
        compute='_compute_dati_cliente', store=False)
    cliente_street = fields.Char(
        compute='_compute_dati_cliente', store=False)
    cliente_street2 = fields.Char(
        compute='_compute_dati_cliente', store=False)
    cliente_localita = fields.Char(
        compute='_compute_dati_cliente', store=False)
    cliente_zip = fields.Char(
        compute='_compute_dati_cliente', store=False)
    cliente_city = fields.Char(
        compute='_compute_dati_cliente', store=False)
    cliente_provincia = fields.Char(
        compute='_compute_dati_cliente', store=False)
    cliente_mod_pagamento = fields.Char(
        compute='_compute_dati_cliente', store=False)

    referente_indirizzo = fields.Char(
        compute='_compute_dati_referente', store=False)
    referente_indirizzo2 = fields.Char(
        compute='_compute_dati_referente', store=False)
    referente_localita = fields.Char(
        compute='_compute_dati_referente', store=False)
    referente_cap = fields.Char(
        compute='_compute_dati_referente', store=False)
    referente_citta = fields.Char(
        compute='_compute_dati_referente', store=False)
    referente_provincia = fields.Char(
        compute='_compute_dati_referente', store=False)
    referente_tel = fields.Char(
        compute='_compute_dati_referente', store=False)
    referente_cell = fields.Char(
        compute='_compute_dati_referente', store=False)
    referente_fax = fields.Char(
        compute='_compute_dati_referente', store=False)
    referente_email = fields.Char(
        compute='_compute_dati_referente', store=False)
    referente_interlocutore = fields.Char(
        compute='_compute_dati_referente', store=False)

    impianto_etichetta = fields.Char(
        compute='_compute_impianto_ubicazione', store=False)
    impianto_indirizzo = fields.Char(
        compute='_compute_impianto_ubicazione', store=False)
    impianto_indirizzo2 = fields.Char(
        compute='_compute_impianto_ubicazione', store=False)
    impianto_localita = fields.Char(
        compute='_compute_impianto_ubicazione', store=False)
    impianto_cap = fields.Char(compute='_compute_impianto_ubicazione', store=False)
    impianto_citta = fields.Char(
        compute='_compute_impianto_ubicazione', store=False)
    impianto_provincia = fields.Char(
        compute='_compute_impianto_ubicazione', store=False)
    impianto_categoria_name = fields.Char(compute='_compute_impianto_ubicazione', string="Categoria Impianto", store=True)

    manutentore_citta = fields.Char(
        compute='_compute_dati_mautentore', store=False)
    manutentore_tel = fields.Char(
        compute='_compute_dati_mautentore', store=False)
    manutentore_cell = fields.Char(
        compute='_compute_dati_mautentore', store=False)
    manutentore_fax = fields.Char(
        compute='_compute_dati_mautentore', store=False)
    manutentore_email = fields.Char(
        compute='_compute_dati_mautentore', store=False)
    manutentore_interlocutore = fields.Char(
        compute='_compute_dati_mautentore', store=False)

    state = fields.Selection(
        [
            ('bozza', 'Bozza'),
            ('attivo', 'Attivo'),
            ('scaduto', 'Scaduto'),
            ('rescisso', 'Rescisso'),
            ('disdetta_uv','Disdetta UV'),
            ('annullato', 'Annullato'),
        ],
        string="Stato")

    data_ultima_verifica_effettuata = fields.Date('Data Ultima Verifica Effettuata')

    n_verifiche_contratto = fields.Integer('Totale verifiche da effettuare')

    n_verifiche_effettuate = fields.Integer('N. verifiche effettuate')

    note_interne = fields.Text("Note Interne")

    note_amministratore = fields.Text("Note Amministratore")

    periodicita_verifica = fields.Selection(
        [
            ('2', 'Ogni 2 anni'),
            ('5', 'Ogni 5 anni'),
        ],
        default='2',
        required=True,
        string="Periodicità verifica")

    data_prossima_verifica = fields.Date("Prossima Verifica")

    blocco_amministrativo = fields.Boolean('Blocco Amministrativo', default=False)
    causale_blocco = fields.Selection(
            [
                ('moroso', 'Amministratore Moroso'),
                ('fuori_fido', 'Fuori Fido'),
                ('fattura_anticipata', 'Fattura Anticipata'),
            ],
            string="Causale Blocco")

    def action_attivo(self):
        self.state = 'attivo'

    def action_scaduto(self):
        self.state = 'scaduto'

    def action_rescisso(self):
        self.state = 'rescisso'

    def action_disdetta_uv(self):
        self.state = 'disdetta_uv'

    def action_first_attivo(self):
        if not self.impianto_id:
            raise exceptions.ValidationError("Associare l'impianto prima di attivare il contratto.")
        self._aggiorna_da_create()
        self.state = 'attivo'
        self._crea_verifica_periodica()

    def action_annullato(self):
        self.state = 'annullato'
        verbale_obj = self.env['gevi_verbali.verbale'].search(['&',('contratto_id', '=', self.id),('state','in',('bozza','assegnato'))])
        for verbale in verbale_obj:
            verbale.action_annullato()

    @api.onchange('durata_contratto')
    def _onchange_durata_contratto(self):
        for line in self:
            line.n_verifiche_contratto = int(line.durata_contratto)

    @api.depends('customer_id')
    def _compute_dati_cliente(self):
        for record in self:
            self.cliente_cf = record.customer_id.cf
            self.cliente_piva = record.customer_id.piva
            self.cliente_tipo = record.customer_id.tipo_cliente_id.name
            self.cliente_street = record.customer_id.street
            self.cliente_street2 = record.customer_id.street2
            self.cliente_localita = record.customer_id.localita
            self.cliente_zip = record.customer_id.zip
            self.cliente_city = record.customer_id.city
            self.cliente_provincia = record.customer_id.provincia
            self.cliente_mod_pagamento = record.customer_id.property_payment_term_id.name

    @api.depends('referente_id')
    def _compute_dati_referente(self):
        for record in self:
            self.referente_indirizzo = record.referente_id.indirizzo
            self.referente_indirizzo2 = record.referente_id.indirizzo2
            self.referente_localita = record.referente_id.localita
            self.referente_cap = record.referente_id.cap
            self.referente_citta = record.referente_id.citta
            self.referente_provincia = record.referente_id.provincia
            self.referente_tel = record.referente_id.tel
            self.referente_cell = record.referente_id.cell
            self.referente_fax = record.referente_id.fax
            self.referente_email = record.referente_id.email
            self.referente_interlocutore = record.referente_id.interlocutore

    @api.depends('impianto_id')
    def _compute_impianto_ubicazione(self):
        for record in self:
            self.impianto_etichetta = record.impianto_id.etichetta
            self.impianto_indirizzo = record.impianto_id.indirizzo
            self.impianto_indirizzo2 = record.impianto_id.indirizzo2
            self.impianto_localita = record.impianto_id.localita
            self.impianto_cap = record.impianto_id.cap
            self.impianto_citta = record.impianto_id.citta
            self.impianto_provincia = record.impianto_id.provincia
            self.cliente_name = record.impianto_id.customer_id.name
            self.impianto_categoria_name = record.impianto_id.impianto_categoria_id.name

    @api.depends('manutentore_id')
    def _compute_dati_mautentore(self):
        for record in self:
            self.manutentore_citta = record.manutentore_id.citta
            self.manutentore_tel = record.manutentore_id.tel
            self.manutentore_cell = record.manutentore_id.cell
            self.manutentore_fax = record.manutentore_id.fax
            self.manutentore_email = record.manutentore_id.email
            self.manutentore_interlocutore = record.manutentore_id.interlocutore

    # Azione riferita al button filtra_cliente
    # @api.one
    # @api.onchange('cliente_cf_piva')
    # def _onchange_cliente_cf_piva(self):
    #     # cliente_obj = self.env['res.partner']
    #     # clienti = cliente_obj.search(
    #     #     ['|',('piva', '=', self.cliente_cf_piva),('cf', '=', self.cliente_cf_piva)] )

    #     return {
    #         'domain': {
    #             'customer_id': ['|',('piva', '=', self.cliente_cf_piva),('cf', '=', self.cliente_cf_piva)]
    #         }
    #     }

    # @api.one
    # @api.onchange('impianto_id')
    # def _onchange_impianto_id(self):
    #     for record in self:
    #         self.impianto_categoria_id = record.impianto_id.impianto_categoria_id.id
    #         self.customer_id = record.impianto_id.customer_id.id
    #         self.referente_id = record.impianto_id.customer_id.referente_id.id

    def carica_riferimenti(self):
        for record in self:
            self.impianto_categoria_id = record.impianto_id.impianto_categoria_id.id
            self.customer_id = record.impianto_id.customer_id.id
            self.referente_id = record.impianto_id.customer_id.referente_id.id

    @api.depends('verifica_periodica','verifica_straordinaria','costo_verifica_periodica','costo_verifica_straordinaria')
    def _valida_campi(self):
        self.campi_validati = False
        if (self.verifica_periodica or self.verifica_straordinaria):
            if (self.costo_verifica_straordinaria != 0.00 or self.costo_verifica_periodica != 0.00):
                self.campi_validati = True

    @api.depends('costo_verifica_periodica', 'costo_verifica_straordinaria')
    def _compute_valore_contratto(self):
        for record in self:
            self.valore_contratto = self.costo_verifica_periodica + self.costo_verifica_straordinaria

    @api.onchange('impianto_categoria_id')
    def _onchange_impianto_categoria_id(self):
        for line in self:
            if line.impianto_categoria_name in ['Piattaforma Elevatrice', 'Montacarichi']:
                line.verifica_straordinaria = False
                line.periodicita_verifica = '2'
            if line.impianto_categoria_name in ['Ascensore Generico', 'Ascensore Oleodinamico', 'Ascensore Elettromeccanico']:
                line.periodicita_verifica = '2'
            if line.impianto_categoria_name in ['Scariche Atmosferiche', 'Messa a Terra']:
                pass
            if line.impianto_categoria_id is not False:
                pass

    @api.onchange('customer_id')
    def _onchange_customer_id(self):
        self.referente_id = self.customer_id.referente_id
        self.modalita_pagamento_id = self.customer_id.property_payment_term_id
        # res = {}
        # lista_impianti = []
        # impianto_obj = self.env['gevi.impianti.impianto']
        # impianti_ids = impianto_obj.search([('customer_id', '=', self.customer_id.id)])
        # for record in impianti_ids:
        #     lista_impianti.append(record.id)
        # res['domain'] = {'impianto_id': [('id', 'in', lista_impianti)]}
        # return res

    # metodo non utilizzato
    def verifica_periodica_effettuata(self, verbale):
        self.data_ultima_verifica_effettuata = verbale.data_verbale
        self.n_verifiche_effettuate += 1
        if self.n_verifiche_contratto == self.n_verifiche_effettuate:
            # self.action_scaduto()
            pass

    def aggiorna_stato(self):
        for record in self:
            if record.state == 'disdetta_uv':
                record.action_scaduto()
            if record.state == 'attivo':
                if record.n_verifiche_contratto == -1:
                    record.action_crea_verifica_periodica()
                else:
                    if record.n_verifiche_contratto > record.n_verifiche_effettuate:
                        record.action_crea_verifica_periodica()
                    else:
                        record.action_scaduto()

    def _crea_verifica_periodica(self):
        for record in self:
            if record.state == 'attivo':
                verbale_obj = self.env['gevi_verbali.verbale']
                fa = False
                if record.causale_blocco == 'fattura_anticipata':
                    fa = True
                if record.verifica_periodica:
                    verbale = verbale_obj.create({
                        'impianto_id': self.impianto_id.id,
                        'data_ultima_verifica': self.data_ultima_verifica,
                        'contratto_id': self.id,
                        'manutentore_id': self.manutentore_id.id,
                        'periodica': True,
                        'impianto_categoria_id': self.impianto_id.impianto_categoria_id.id,
                        'impianto_categoria_name': self.impianto_id.impianto_categoria_id.name,
                        'customer_id': self.impianto_id.customer_id.id,
                        'referente_id': self.impianto_id.customer_id.referente_id.id,
                        'data_programmazione': self.data_prossima_verifica,
                        'fattura_anticipata': fa,
                    })
                    # verbale.carica_attributi_descrittivi()

    # @api.one
    # def crea_verifica_periodica(self):
    #     attributi_descrittivi = []
    #     record = self
    #     for linea in record.impianto_id.impianto_riga_descrizione_ids:
    #         attributi_descrittivi.append([0, 0, {
    #             'name': linea.name,
    #             'unita_di_misura_id': linea.unita_di_misura_id,
    #             }])

    def _crea_verifica_straordinaria(self):
        for record in self:
            if record.state == 'attivo' or record.state == 'disdetta_uv':
                verbale_obj = self.env['gevi_verbali.verbale']
                fa = False
                if record.causale_blocco == 'fattura_anticipata':
                    fa = True
                # attributi_descrittivi_obj = self.env['gevi.impianti.impianto_riga_descrizione'].search([('impianto_id', '=', record.impianto_id.id)])
                if record.verifica_straordinaria is True:
                    verbale = verbale_obj.create({
                        'impianto_id': self.impianto_id.id,
                        'data_ultima_verifica': self.data_ultima_verifica,
                        'contratto_id': self.id,
                        'manutentore_id': self.manutentore_id.id,
                        'periodica': False,
                        'impianto_categoria_id': self.impianto_id.impianto_categoria_id.id,
                        'impianto_categoria_name': self.impianto_id.impianto_categoria_id.name,
                        'customer_id': self.impianto_id.customer_id.id,
                        'referente_id': self.impianto_id.customer_id.referente_id.id,
                        'data_programmazione': self.data_prossima_verifica,
                        'fattura_anticipata': fa,
                        # 'impianto_riga_descrizione_ids': [attributi_descrittivi_obj.ids],
                    })
                    # verbale.carica_attributi_descrittivi()

    def action_crea_verifica_periodica(self):
        self._crea_verifica_periodica()

    def action_crea_verifica_straordinaria(self):
        self._crea_verifica_straordinaria()

    def write(self, values):
        """
            Update all record(s) in recordset, with new value comes as {values}
            return True on success, False otherwise
            @param values: dict of new values to be set
            @return: True on success, False otherwise
        """
        result = super(Contratto, self).write(values)
        for record in self:
            self.customer_id.property_payment_term_id = record.modalita_pagamento_id
            self.customer_id.referente_id = record.referente_id
        return result

    # Controllo su cancellazione
    def unlink(self):
        # _logger.info('******************************** DELETE {0} {1}'.format(self.name, self.state))
        if self.state != "annullato":
            raise exceptions.ValidationError('ATTENZIONE: Non è possibile cancellare la verifica {0} ({1}). Lo stato deve essere ANNULLATO!'.format(self.name, self.state))
        else:
            result = super(Contratto, self).unlink()
            return result


    def _aggiorna_da_create(self):
        for line in self:
            line.impianto_id.manutentore_id = line.manutentore_id
            line.customer_id.referente_id = line.referente_id
            line.customer_id.property_payment_term_id = line.modalita_pagamento_id

    def _aggiorna_da_import(self):
        for line in self:
            line.customer_id = line.impianto_id.customer_id
            line.referente_id = line.customer_id.referente_id

    @api.model
    def create(self, values):
        """
            Create a new record for a model Contratto
            @param values: provides a data for new record
            @return: returns a id of new record
        """
        # per l'importazione dei dati, si può modificare il prefisso della
        # sequence in modo da avere un prefisso tipo c/2016 così si capisce
        # che è un contratto vecchio.

        values['codice_contratto'] = self.env['ir.sequence'].get(
            'gevi_contratti.contratto')
        values['name'] = values['codice_contratto']
        values['state'] = 'bozza'
        result = super(Contratto, self).create(values)

        return result

    def create_old(self, values):
        """
            Create a new record for a model Contratto
            @param values: provides a data for new record
            @return: returns a id of new record
        """
        # per l'importazione dei dati, si può modificare il prefisso della
        # sequence in modo da avere un prefisso tipo c/2016 così si capisce
        # che è un contratto vecchio.

        values['codice_contratto'] = self.env['ir.sequence'].get(
            'gevi_contratti.contratto')
        values['name'] = values['codice_contratto']
        values['state'] = 'attivo'
        result = super(Contratto, self).create(values)
        result._aggiorna_da_create()

        # commentare la riga seguente che serve solo per l'importazione
        # result._aggiorna_da_import()

        result._crea_verifica_periodica()

        return result

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(Contratto, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='impianto_id']"):
                node.set("domain", "[('customer_id', '=', customer_id)]")
            res['arch'] = etree.tostring(doc)
        return res

    def get_verbale_obj_name_by_cat_impianto(self):
        if self.impianto_id.impianto_categoria_id.descrizione == 'BIL':
            return 'gevi_zbilance.verbale'
        else:
            return 'gevi_verbali.verbale'
        pass