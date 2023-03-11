# coding=utf-8
from odoo import fields, models, api, exceptions

import logging
_logger = logging.getLogger(__name__)


class VerbaleBilance(models.Model):
    _name = 'gevi_zbilance.verbale'

    name = fields.Char('Nome', default="/", readonly=True)
    codice_verifica = fields.Char(
        string='Codice Verifica',
        readonly=True,
        default="/", )

    impianto_id = fields.Many2one('gevi.impianti.impianto', string="Impianto")

    impianto_indirizzo = fields.Char(
        compute='_compute_riferimenti_impianto', store=True)
    impianto_indirizzo2 = fields.Char(
        compute='_compute_riferimenti_impianto', store=False)
    impianto_cap = fields.Char(compute='_compute_riferimenti_impianto', store=True)
    impianto_citta = fields.Char(
        compute='_compute_riferimenti_impianto', store=True)
    impianto_provincia = fields.Char(
        compute='_compute_riferimenti_impianto', store=True)
    impianto_etichetta = fields.Char(
        compute='_compute_riferimenti_impianto', store=True)

    range_p_min = fields.Float(
        compute='_compute_riferimenti_impianto', store=True)
    range_p_max = fields.Float(
        compute='_compute_riferimenti_impianto', store=True)
    range_e_divisione_verifica = fields.Float(
        compute='_compute_riferimenti_impianto', store=True)
    range_d_divisione_minima = fields.Float(
        compute='_compute_riferimenti_impianto', store=True)

    state = fields.Selection(
        [
            ('bozza', 'Bozza'),
            ('assegnato', 'Assegnato'),
            ('eseguito', 'Eseguito'),
            ('confermato', 'Confermato'),
            ('in_revisione', 'In Revisione'),
            ('validato', 'Validato'),
            ('annullato', 'Annullato'),
        ],
        default="bozza",
        string="Stato")

    data_assegnazione = fields.Date("Data Assegnazione", readonly=True)
    data_programmazione = fields.Date("Data Programmazione")
    data_ultima_verifica = fields.Date("Data Ultima Verifica")
    data_esecuzione = fields.Date("Data Esecuzione", readonly=True)
    data_verbale = fields.Date("Data Verbale")
    data_conferma = fields.Date("Data Conferma")
    data_validazione = fields.Date("Data Validazione")

    ispettore_id = fields.Many2one('hr.employee', string="Ispettore", domain=[('job_id.name', 'ilike', 'Ispettore')])
    responsabile_tecnico_id = fields.Many2one('hr.employee', string="Responsabile Tecnico",
                                              domain=[('job_id.name', 'ilike', 'Responsabile Tecnico')])

    esito_verifica = fields.Selection(
        [
            ('da_selezionare', 'da Selezionare'),
            ('positivo', 'Positivo'),
            ('negativo', 'Negativo'),
        ],
        default='da_selezionare'
        )

    customer_id = fields.Many2one(
        'res.partner',
        domain=[('customer', '=', True)],
        string='Cliente Fatturazione')

    referente_id = fields.Many2one(
        'gevi_contatti.referente', string="Amministratore")

    impianto_categoria_id = fields.Many2one(
        'gevi.impianti.impianto_categoria', string='Categoria Impianto')
    impianto_categoria_name = fields.Char(compute='_compute_impianto_categoria_id', store=True)

    impianto_riga_descrizione_ids = fields.One2many('gevi.impianti.impianto_riga_descrizione', 'impianto_id')

    contratto_id = fields.Many2one('gevi_contratti.contratto', string='Contratto')

    fattura_anticipata = fields.Boolean(string="Fattura Anticipata", default=False)

    prossima_verifica = fields.Date("Prossima Verifica")
    data_prossima_verifica = fields.Date("Data Prossima Verifica")

    periodica = fields.Boolean(string="Periodica", default=False)

    tipo_verbale = fields.Selection(
        [('periodica', 'Verifica Periodica'),
         ('periodica_controllo_casuale', 'Verifica Periodica Controllo Casuale'),
         ('a_seguito_riparazione', 'A seguito Riparazione'),
         ],
        "Tipo verifica"
    )
    attributi_caricati = fields.Boolean("Attributi Caricati", default=False)

    note_interne = fields.Text("Note Interne")

    is_ispettore = fields.Boolean("Is Ispettore", compute='_compute_is_ispettore')

    is_responsabile_tecnico = fields.Boolean("Is Responsabile Tecnico", compute='_compute_is_responsabile_tecnico')

    timbro_ispettore = fields.Binary(
        string='Timbro',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help=False
    )

    timbro_responsabile_tecnico = fields.Binary(
        string='Timbro',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help=False
    )

    zona_impianto_id = fields.Many2one('gevi_zone.zona_impianto', string="Zona Impianto",
                                       related='impianto_id.zona_impianto_id', store=True)

    cf_cliente = fields.Char("CF Cliente", compute='_compute_riferimenti_impianto', store=True)
    piva_cliente = fields.Char("P.IVA Cliente", compute='_compute_riferimenti_impianto', store=True)
    blocco_amministrativo = fields.Boolean("Blocco Amministrativo", compute='_compute_blocco_amministrativo',
                                           store=False)
    codice_contratto = fields.Char("Codice Contratto", compute='_compute_blocco_amministrativo', store=True, ondelete='cascade',)


    # campi ispezione visiva
    n_sigilli = fields.Integer("Sigilli N.", default=False)
    sigilli_regolari = fields.Boolean("Sigilli Regolari", default=False)
    indicazioni_metr_regolari = fields.Boolean("Indicazioni metrologiche regolari", default=False)
    note_sigilli = fields.Char("Note Sigilli", default=False)
    n_libretto_metr = fields.Char("Sigilli N.", default=False)
    libretto_presente = fields.Boolean("Libretto Presente", default=True)
    rilascio_nuovo_libretto = fields.Boolean("Rilascio di un nuovo SI", default=False)
    anno_marcatura_ce = fields.Char("Anno Marcatura (CE)", default=False)
    anno_fabbricazione = fields.Char("Anno di fabbricazione", default=False)
    data_inizio_utilizzo = fields.Date("Data Inizio Utilizzo", default=False)
    release_sw_bilancia = fields.Char("Release software Bilancia", default=False)
    rif_numero = fields.Char("n di amm. ver. metrica", default=False)

    pesiera_ids = fields.Many2many(
        comodel_name="gevi_zbilance.pesiera",
        column1="verbale_id",
        column2="pesiera_id",
        string="Pesiere"
    )

    schema_eccentricita = fields.Selection(
        [
            ('a', 'Schema A'),
            ('b', 'Schema B'),
            ('c', 'Schema C'),
            ('d', 'Schema D'),
            ('e', 'Schema E'),
        ],
        )

    # Rif. EN 45501:2015 A 4.2.3
    prova_zero_ids = fields.One2many(
        'gevi_zbilance.prova_zero', 'verbale_id',
        'Prova di Zero')

    # Rif. EN 45501:2015 A 4.10
    prova_ripetibilita_ids = fields.One2many(
        'gevi_zbilance.prova_ripetibilita', 'verbale_id',
        'Prova di Ripetibilità')

    # Rif. EN 45501:2015 A 4.7
    prova_eccentricita_ids = fields.One2many(
        'gevi_zbilance.prova_eccentricita', 'verbale_id',
        'Prova di Eccentricità')

    # Rif. EN 45501:2015 A 4.4.1
    prova_linearita_ids = fields.One2many(
        'gevi_zbilance.prova_linearita', 'verbale_id',
        'Prova di Linearità')

    # Rif. EN 45501:2015 A 4.6.1
    prova_tara_ids = fields.One2many(
        'gevi_zbilance.prova_tara', 'verbale_id',
        'Prova di Tara')

    # Rif. EN 45501:2015 A 4.9
    prova_mobilita_ids = fields.One2many(
        'gevi_zbilance.prova_mobilita', 'verbale_id',
        'Prova di Mobilità')

    esito_zero = fields.Boolean("Esito Prova di Zero - Rif. EN 45501:2015 A 4.2.3", default=False)
    esito_ripetibilita = fields.Boolean("Esito Prova di Ripetibilità - Rif. EN 45501:2015 A 4.10", default=False)
    esito_eccentricita = fields.Boolean("Esito Prova di Eccentricità - Rif. EN 45501:2015 A 4.7", default=False)
    esito_linearita = fields.Boolean("Esito Prova di Linearità - Rif. EN 45501:2015 A 4.4.1", default=False)
    esito_tara = fields.Boolean("Esito Prova di Tara - Rif. EN 45501:2015 A 4.6.1", default=False)
    esito_mobilita = fields.Boolean("Esito Prova di Mobilità - Rif. EN 45501:2015 A 4.9", default=False)

    ripetibilita_carico = fields.Float("Carico da")
    ripetibilita_diff_pmax_pmin = fields.Float("Pmax - Pmin")
    ripetibilita_tolleranza = fields.Float("Tolleranza +/-")

    # campi related

    stato_contratto = fields.Selection(
            string='Stato Contratto',
            readonly=True,
            related='contratto_id.state',
            store=True
        )

    periodicita = fields.Selection(
        'gelab.contratto', string="Periodicità", related='contratto_id.periodicita_verifica', store=True)

    utente_assegnato_referente_id = fields.Many2one(
        string='Utente Assegnato ad Amministratore',
        readonly=True,
        comodel_name='res.users',
        related='referente_id.utente_assegnato_id',
        store=True
    )

    def send_mail(self):
        for line in self:
            # do export
            # id 11 = Invia verbale
            domain_template = [('id', '=', 11)]
            if line.state == 'validato':
                template_mail = self.env['mail.template'].search(domain_template)
                if line.customer_id.referente_id and line.customer_id.referente_id.email:
                    template_mail.email_to = line.customer_id.referente_id.email
                    template_mail.send_mail(line.id, force_send=True)
                    template_mail.email_to = None

                if line.manutentore_id and line.manutentore_id:
                    template_mail.email_to = line.manutentore_id.email
                    template_mail.send_mail(line.id, force_send=True)
                    template_mail.email_to = None

    # metodi compute

    @api.depends('impianto_id')
    def _compute_riferimenti_impianto(self):
        for record in self:
            record.impianto_etichetta = record.impianto_id.etichetta
            record.impianto_indirizzo = record.impianto_id.indirizzo
            record.impianto_indirizzo2 = record.impianto_id.indirizzo2
            record.impianto_cap = record.impianto_id.cap
            record.impianto_citta = record.impianto_id.citta
            record.impianto_provincia = record.impianto_id.provincia
            record.cf_cliente = record.impianto_id.customer_id.cf
            record.piva_cliente = record.impianto_id.customer_id.piva
            record.range_p_min = record.impianto_id.range_1.p_min
            record.range_p_max = record.impianto_id.range_1.p_max
            record.range_e_divisione_verifica = record.impianto_id.range_1.e_divisione_verifica
            record.range_d_divisione_minima = record.impianto_id.range_1.d_divisione_minima

    @api.depends('impianto_categoria_id')
    def _compute_impianto_categoria_id(self):
        for record in self:
            record.impianto_categoria_name = record.impianto_categoria_id.name


    @api.depends('ispettore_id')
    def _compute_is_ispettore(self):
        for line in self:
            if line.ispettore_id.user_id.id == self.env.uid:
                line.is_ispettore = True
            else:
                line.is_ispettore = False

    @api.depends('responsabile_tecnico_id')
    def _compute_is_responsabile_tecnico(self):
        for line in self:
            if line.responsabile_tecnico_id.user_id.id == self.env.uid:
                line.is_responsabile_tecnico = True
            else:
                line.is_responsabile_tecnico = False

    @api.depends('impianto_id')
    def _compute_blocco_amministrativo(self):
        for record in self:
            record.blocco_amministrativo = record.contratto_id.blocco_amministrativo
            record.codice_contratto = record.contratto_id.codice_contratto

    # metodi action

    def action_bozza(self):
        self.verifica_blocco_amministrativo()
        self.popola_prove()
        self.state = 'bozza'

    def action_assegnato(self):
        self.verifica_blocco_amministrativo()
        self.state = 'assegnato'
        self.data_assegnazione = fields.Date.context_today(self)

    def action_eseguito(self):
        self.verifica_blocco_amministrativo()
        self.data_esecuzione = fields.Date.context_today(self)
        self.state = 'eseguito'

    def action_confermato(self):
        self.verifica_blocco_amministrativo()
        for record in self:
            self.data_conferma = fields.Date.context_today(self)
            self.impianto_id.impianto_categoria_id = self.impianto_categoria_id
            self.timbro_ispettore = (self.env.user).timbro_isp
            if self.name.find('Prog') != -1:
                self.name = self.env['ir.sequence'].with_context(
                    ir_sequence_date='2022-01-01').next_by_code('gevi_zbilance.verbale')
                # self.name = self.env['ir.sequence'].next_by_code('gevi_zbilance.verbale')
                self.data_verbale = fields.Date.context_today(self)
            self.state = 'confermato'

    def action_in_revisione(self):
        self.verifica_blocco_amministrativo()
        for record in self:
            self.state = 'in_revisione'

    def action_riconfermato(self):
        self.verifica_blocco_amministrativo()
        for record in self:
            self.timbro_ispettore = (self.env.user).timbro_isp
            self.state = 'confermato'

    def action_validato(self):
        self.verifica_blocco_amministrativo()
        self.verifica_is_responsabile_tecnico()
        self.timbro_responsabile_tecnico = (self.env.user).timbro_rt
        # self.data_validazione = fields.Date.context_today(self)
        self.impianto_id.manutentore_id = self.manutentore_id
        if self.periodica is True:
            self.aggiorna_prossima_verifica()
            self.aggiorna_contratto()
        self.state = 'validato'
        if self.fattura_anticipata is False:
            self._crea_ordine_vendita()

    def action_annullato(self):
        self.verifica_blocco_amministrativo()
        for prova in self.prova_zero_ids:
            prova.unlink()
        for prova in self.prova_ripetibilita_ids:
            prova.unlink()
        for prova in self.prova_linearita_ids:
            prova.unlink()
        for prova in self.prova_tara_ids:
            prova.unlink()
        for prova in self.prova_mobilita_ids:
            prova.unlink()
        for prova in self.prova_eccentricita_ids:
            prova.unlink()
        self.state = 'annullato'

    # metodi model
    def popola_prove(self):
        self.prova_zero_ids = [[0, 0, {}]]
        prova_ripetibilita = []
        # PER CLASSE I e II => 6 pesate all’80%, PER CLASSE III e IV => 3 pesate all’80%
        x = range(3)
        for n in x:
            prova_ripetibilita.append([0, 0, {'indicazione': self.range_p_max * 0.8}])
            # prova_ripetibilita.append([0, 0, {}])
        self.prova_ripetibilita_ids = prova_ripetibilita
        prova_linearita = []
        x = range(5)
        for n in x:
            prova_linearita.append([0, 0, {}])
        self.prova_linearita_ids = prova_linearita
        self.prova_tara_ids = [[0, 0, {}]]
        prova_mobilita = []
        x = range(3)
        for n in x:
            prova_mobilita.append([0, 0, {}])
        self.prova_mobilita_ids = prova_mobilita

    def popola_prova_eccentricita(self):
        for prova in self.prova_eccentricita_ids:
            prova.unlink()
        x = 0
        prova_eccentricita = []
        if self.schema_eccentricita in ('b', 'e'):
            x = range(3)
        if self.schema_eccentricita == 'd':
            x = range(4)
        if self.schema_eccentricita == 'a':
            x = range(5)
        if self.schema_eccentricita == 'c':
            x = range(8)
        for n in x:
            prova_eccentricita.append([0, 0, {'posizione': (n+1)}])
        self.prova_eccentricita_ids = prova_eccentricita

    @api.onchange('schema_eccentricita')
    def schema_eccentricita_change(self):
        self.popola_prova_eccentricita()

    @api.onchange('prova_mobilita_ids')
    def provamobilita_change(self, do_update=True):
        prova_superata = True
        for prova in self.prova_mobilita_ids:
            prova.calcola_verifica()
            prova_superata = prova_superata and prova.verifica
            if do_update:
                dati_calc_prova = {
                    'verifica': prova.verifica,
                    'errore_e': prova.errore_e,
                }
                prova.write(dati_calc_prova)
        self.esito_mobilita = prova_superata

    @api.onchange('prova_ripetibilita_ids')
    def provaripetibilita_change(self):
        # prova_superata = False
        # tot_carico = 0.0
        # max_p = 0.0
        # min_p = self.range_p_max
        # for prova in self.prova_ripetibilita_ids:
        #     if prova.p > max_p:
        #         max_p = prova.p
        #     if prova.p < min_p:
        #         min_p = prova.p
        #     tot_carico += prova.indicazione
        # diff_max_min_p = max_p - min_p
        diff_max_min_p, tot_carico, prova_superata = self.calcola_provaripetibilita()
        self.ripetibilita_diff_pmax_pmin = diff_max_min_p
        self.ripetibilita_tolleranza = self.range_d_divisione_minima
        self.ripetibilita_carico = tot_carico
        self.esito_ripetibilita = prova_superata

    def calcola_provaripetibilita(self):
        prova_superata = False
        tot_carico = 0.0
        max_p = 0.0
        min_p = self.range_p_max
        for prova in self.prova_ripetibilita_ids:
            if prova.p > max_p:
                max_p = prova.p
            if prova.p < min_p:
                min_p = prova.p
            tot_carico += prova.indicazione
        diff_max_min_p = max_p - min_p
        if diff_max_min_p < self.range_d_divisione_minima:
            prova_superata = True
        return diff_max_min_p, tot_carico, prova_superata

    @api.model
    def create(self, values):
        """
             Create a new record for a model Verbale
             @param values: provides a data for new record
             @return: returns a id of new record
         """
        values['codice_verifica'] = self.env['ir.sequence'].next_by_code(
            'gevi_zbilance.verifica')
        # _logger.info('******************************** CREAZIONE: {0}'.format(values['codice_verifica']))
        values['name'] = values['codice_verifica']
        result = super(VerbaleBilance, self).create(values)
        result.popola_prove()
        return result

    def write(self, values):
        if 'esito_mobilita' not in values:
            self.provamobilita_change(do_update=False)
        if 'esito_ripetibilita' not in values:
            diff_max_min_p, tot_carico, prova_superata = self.calcola_provaripetibilita()
            values['esito_ripetibilita'] = prova_superata
        result = super(VerbaleBilance, self).write(values)
        return result

    def unlink(self):
        # _logger.info('******************************** WRITE {0} {1}: VALUES {2} - STATE {3}'.format(
        # self.codice_verifica, self.name, values, self.state))
        if self.state != "annullato":
            raise exceptions.ValidationError('ATTENZIONE: Non è possibile cancellare la verifica {0} ({1}). Lo stato '
                                             'deve essere ANNULLATO!'.format(self.name, self.state))
        else:
            result = super(VerbaleBilance, self).unlink()
            return result


    # metodi common

    def aggiorna_dati_impianto(self):
        self._compute_riferimenti_impianto()

    def verifica_blocco_amministrativo(self):
        if self.blocco_amministrativo is True:
            raise exceptions.ValidationError('Sul contratto {0} è presente un blocco amministrativo e pertanto non è '
                                             'possibile procedere in alcun modo.'.format(self.codice_contratto))

    def verifica_is_responsabile_tecnico(self):
        if self.is_responsabile_tecnico is False:
            raise exceptions.ValidationError('Solo il Responsabile Tecnico può validare definitivamente il verbale!')

    def aggiorna_prossima_verifica(self):
        record = self
        periodicita_verifica_int = int(record.contratto_id.periodicita_verifica)
        start = fields.Date.from_string(self.data_verbale)
        self.data_prossima_verifica = start.replace(year=start.year + periodicita_verifica_int)
        self.impianto_id.data_ultima_verifica = self.data_verbale
        self.data_ultima_verifica = self.data_verbale

    def aggiorna_contratto(self):
        contratto_obj = self.env['gevi_contratti.contratto'].search([('id', '=', self.contratto_id.id)])
        contratto_obj.data_ultima_verifica_effettuata = self.data_verbale
        contratto_obj.n_verifiche_effettuate += 1
        contratto_obj.data_prossima_verifica = self.data_prossima_verifica
        contratto_obj.data_ultima_verifica = self.data_verbale
        contratto_obj.manutentore_id = self.impianto_id.manutentore_id
        contratto_obj.aggiorna_stato()
        contratto_obj._compute_impianto_ubicazione()

    def apri_verbale_bilance(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Verbale',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'target': 'current',
        }

    def _crea_ordine_vendita(self):
        ordine_obj = self.env['sale.order']
        self.ubicazione = '{0} {1}, {2} {3} - {4} {5} ({6})'.format(
                self.customer_id.name.encode('utf-8'),
                self.impianto_id.etichetta.encode('utf-8'),
                self.impianto_id.indirizzo.encode('utf-8'),
                ' ' if self.impianto_id.indirizzo2 is False else self.impianto_id.indirizzo2,
                self.impianto_id.cap,
                self.impianto_id.citta,
                self.impianto_id.provincia
            )

        if self.periodica is True:
            self.sigla_periodica = 'P'
            self.costo = self.contratto_id.costo_verifica_periodica
        else:
            self.sigla_periodica = 'S'
            self.costo = self.contratto_id.costo_verifica_straordinaria

        self.sigla_impianto = self.env['gevi.impianti.impianto_categoria'].search(
            [('name', '=', self.impianto_categoria_id.name)], limit=1).descrizione
        if self.fattura_anticipata is True:
            self.codice_prodotto = 'VV{0}-{1}-FA'.format(self.sigla_periodica, self.sigla_impianto)
        else:
            self.codice_prodotto = 'VV{0}-{1}'.format(self.sigla_periodica, self.sigla_impianto)
        # _logger.info('******************************** CODICE PRODOTTO: {0}'.format(self.codice_prodotto))
        prodotto_obj = self.env['product.product'].search([('name', '=', self.codice_prodotto)], limit=1)
        data_verbale_formato_it = fields.Date.from_string(self.data_verbale)
        odv = {
            # 'name': ,
            'origin': self.name,
            'verbale_bilance_id': self.id,
            'date_order': fields.Date.context_today(self),
            'partner_id': self.customer_id.id,
            'partner_invoice_id': self.customer_id.id,
            'order_line': [(0, 0, {
                'product_id': prodotto_obj.id,
                'name': (prodotto_obj.description_sale).format(self.name, data_verbale_formato_it.strftime("%d/%m/%Y"),
                                                               self.ubicazione,
                                                               self.data_ultima_verifica),
                'price_unit': self.costo,
                'discount': 0.0,
                'sequence': 10,

            })],
        }
        if self.contratto_id.opportunity_id:
            odv['opportunity_id'] = self.contratto_id.opportunity_id.id
        if self.contratto_id.team_id:
            odv['team_id'] = self.contratto_id.team_id.id
        ordine = ordine_obj.create(odv)

        # verifico agente associato ad amministratore per associazione PESCARA
        if self.referente_id and self.referente_id.agente_id:
            if self.referente_id.agente_id.user_id.has_group('__export__.res_groups_90'):
                ordine.write({'user_id': self.referente_id.agente_id.user_id.id})

        ordine.action_confirm()
        return ordine

    def wizard_bil_assegna_isp(self):
        return {
            "name": "Assegna Ispettore",
            "type": "ir.actions.act_window",
            "res_model": "gevi_zbilance.wizard_assegna_isp",
            "view_mode": "form",
            "view_type": "form",
            "views": [(False, "form")],
            "target": "new"
        }

    def wizard_bil_assegna_rt(self):
        return {
            "name": "Assegna Responsabile Tecnico",
            "type": "ir.actions.act_window",
            "res_model": "gevi_zbilance.wizard_assegna_rt",
            "view_mode": "form",
            "view_type": "form",
            "views": [(False, "form")],
            "target": "new"
        }

    def wizard_bil_conferma(self):
        return {
            "name": "Conferma con PIN",
            "type": "ir.actions.act_window",
            "res_model": "gevi_zbilance.wizardconferma",
            "view_mode": "form",
            "view_type": "form",
            "views": [(False, "form")],
            "target": "new"
        }

