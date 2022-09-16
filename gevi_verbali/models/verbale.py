# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions
import time
from datetime import date

import logging

_logger = logging.getLogger(__name__)


class Verbale(models.Model):
    _name = 'gevi_verbali.verbale'

    name = fields.Char('Nome', default="/", readonly=True)
    codice_verifica = fields.Char(
        string='Codice Verifica',
        readonly=True,
        default="/", )

    impianto_id = fields.Many2one('gevi.impianti.impianto', string="Impianto")

    verbale_osservazione_riga_ids = fields.One2many(
        'gevi_verbali.verbale_osservazione_riga',
        'verbale_id',
        string="Osservazioni")

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
    multi_data = fields.Char("Altre Date Verbale")
    # START SDC EDIT 17/12/2016
    data_conferma = fields.Date("Data Conferma")
    data_validazione = fields.Date("Data Validazione")
    # STOP SDC EDIT 17/12/2016

    ispettore_id = fields.Many2one('hr.employee', string="Ispettore", domain=[('job_id.name', 'ilike', 'Ispettore')])
    responsabile_tecnico_id = fields.Many2one('hr.employee', string="Responsabile Tecnico",
                                              domain=[('job_id.name', 'ilike', 'Responsabile Tecnico')])

    # CAMBIATO DA BOOLEAN A SELECTION
    rilievi_precedenti = fields.Selection(
        [
            ('da_selezionare', 'da Selezionare'),
            ('si', 'SI'),
            ('no', 'NO'),
            ('parzialmente', 'PARZIALMENTE'),
        ],
        default='da_selezionare'
    )
    note_di_registro = fields.Boolean(default=False)

    # CAMBIARE IN SELECTION SI/NO
    esito_verifica = fields.Selection(
        [
            ('da_selezionare', 'da Selezionare'),
            ('positivo', 'Positivo'),
            ('negativo', 'Negativo'),
        ],
        default='da_selezionare'
    )
    kit_utilizzato = fields.Char('Kit Utilizzato')

    customer_id = fields.Many2one(
        'res.partner',
        domain=[('customer', '=', True)],
        string='Cliente Fatturazione')

    impianto_categoria_id = fields.Many2one(
        'gevi.impianti.impianto_categoria', string='Categoria Impianto')

    impianto_riga_descrizione_ids = fields.One2many('gevi.impianti.impianto_riga_descrizione', 'impianto_id')

    manutentore_id = fields.Many2one(
        'gevi_contatti.manutentore', string='Manutentore')

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

    verbale_riscontro_riga_ids = fields.One2many(
        'gevi_verbali.verbale_riscontro_riga', 'verbale_id',
        'Lista Riscontri')

    verbale_rilievo_riga_ids = fields.One2many(
        'gevi_verbali.verbale_rilievo_riga', 'verbale_id',
        'Lista Rilievi')

    # MERGE BJ EDIT 19/12/2016
    # START SDC EDIT 12/12/2016
    # fattura_anticipata = fields.Boolean(compute='_anticipa_fattura', default=False)

    periodica = fields.Boolean(string="Periodica", default=False)
    pagato = fields.Boolean()
    ore_lavorate = fields.Float("Ore lavorate", digits=(12, 2))
    impianto_categoria_name = fields.Char(compute='_compute_impianto_categoria_id', store=True)
    prossima_verifica = fields.Date("Prossima Verifica")
    data_prossima_verifica = fields.Date("Data Prossima Verifica")
    non_conformita = fields.Text("Non Conformità")
    norma_riferimento = fields.Char('Norma/e di riferimento')

    contratto_id = fields.Many2one('gevi_contratti.contratto', string='Contratto')

    fattura_anticipata = fields.Boolean(string="Fattura Anticipata", default=False)
    referente_id = fields.Many2one(
        'gevi_contatti.referente', string="Amministratore")

    rilievi_straordinaria = fields.Text("Modifiche", default='Nessuna')
    # START_BJ_Edit_24/02
    tipo_straordinaria = fields.Selection(
        [('per_lavori', 'per lavori'),
         ('a_seguito_di_negativo', 'a seguito di negativo'),
         ('per_tempo_prolungato', 'per fermo prolungato'),
         ('a_seguito_di_incidente', 'a seguito di incidente'),
         ('attivazione', 'attivazione'),
         ]
    )
    mat_non_conformita = fields.Text("Non Conformità", default='Nessuna')
    # END_BJ_Edit_24/02
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
    # STOP SDC EDIT 12/12/2016

    # UPDATE SDC 26/02/2017 per raggruppamento per zona_impianto

    zona_impianto_id = fields.Many2one('gevi_zone.zona_impianto', string="Zona Impianto",
                                       related='impianto_id.zona_impianto_id', store=True)

    # @api.depends('impianto_id.zona_impianto_id')
    # def _compute_zona_impianto(self):
    #     for record in self:
    #         record.zona_impianto_id = record.impianto_id.zona_impianto_id

    # FINE UPDATE SDC 26/02/2017 per raggruppamento per zona_impianto

    # UPDATE SDC 26/02/2017 per cambio stato revisione
    # inserire ('in_revisione', 'In Revisione'), tra gli stati del verbale
    def action_riconfermato(self):
        if self.blocco_amministrativo is True:
            raise exceptions.ValidationError(
                'Sul contratto {0} è presente un blocco amministrativo e pertanto non è possibile procedere in alcun modo.'.format(
                    self.codice_contratto))
        else:
            for record in self:
                self.timbro_ispettore = (self.env.user).timbro_isp
                self.state = 'confermato'

    # Controllo su modifica post validazione
    def write(self, values):
        # _logger.info('******************************** WRITE {0} {1}: VALUES {2} - STATE {3}'.format(self.codice_verifica, self.name, values, self.state))
        if self.state == "validat":
            raise exceptions.ValidationError('ATTENZIONE: Non è possibile modificare un verbale in stato VALIDATO!')
        else:
            result = super(Verbale, self).write(values)
            return result

    # Controllo su cancellazione
    def unlink(self):
        # _logger.info('******************************** WRITE {0} {1}: VALUES {2} - STATE {3}'.format(self.codice_verifica, self.name, values, self.state))
        if self.state != "annullato":
            raise exceptions.ValidationError(
                'ATTENZIONE: Non è possibile cancellare la verifica {0} ({1}). Lo stato deve essere ANNULLATO!'.format(
                    self.name, self.state))
        else:
            result = super(Verbale, self).unlink()
            return result

    # @api.multi
    # def write(self, values):
    #    # gruppo 67 = verbali manager
    #    if self.ispettore_id.user_id.id != self.env.uid and self.responsabile_tecnico_id.user_id.id != self.env.uid and not self.env['res.users'].browse(self.env.uid).has_group('__export__.res_groups_67'):
    #        raise exceptions.ValidationError('ATTENZIONE: Non è possibile salvare le modifiche. Solo il responsabile tecnico e l\'ispettore assegnato possono apportare variazioni')
    #    else:
    #        result = super(Verbale, self).write(values)
    #        return result

    def action_in_revisione(self):
        if self.blocco_amministrativo is True:
            raise exceptions.ValidationError(
                'Sul contratto {0} è presente un blocco amministrativo e pertanto non è possibile procedere in alcun modo.'.format(
                    self.codice_contratto))
        else:
            for record in self:
                self.state = 'in_revisione'

    # FINE UPDATE SDC 26/02/2017 per cambio stato revisione

    def _compute_categoria(self):
        res = {}
        lista_categorie = []
        categoria_obj = self.env['gevi.impianti.impianto_categoria']
        categorie_ids = categoria_obj.search([('customer_id', '=', self.customer_id.id)])
        for record in self.impianti_ids:
            lista_categorie.append(record.id)
        res['domain'] = {'impianto_categoria_id': [('codice_categoria', 'ilike', 'MOD')]}
        return res

    # Personalizzazione terra / scariche

    tempo_tf = fields.Many2one(
        string='tempo_tf',
        help="Tempo di intervento delle protezioni",
        comodel_name='gevi_verbali.utpcei',
        ondelete='cascade',
    )
    utp_cei_993 = fields.Integer('UTP CEI 99-3')
    data_validita_taratura_strumento = fields.Date("Data Validità Taratura")
    mat_verifiche_precedenti = fields.Char('Eventuali verifiche precedenti e/o primo impianto')
    mat_prot_lettere = fields.Char('(Per impianti superiori a 1000V) N. Prot. e data lettera Azienda erogatrice')
    mat_protezione_propria_cabina = fields.Text("Protezione contro i contatti indiretti")
    mat_formula_protezione_propria_cabina = fields.Char('Formula CEI 99-3',
                                                        default="Ue = Re x If = {0} x {1} = {2} V > Utp {3} V.")
    mat_progetto = fields.Selection([('si', 'SI'), ('no', 'NO'), ('na', 'Non Applicabile')], string="Progetto")

    mat_progetto_note = fields.Char('Note Progetto')
    mat_dichiarazione = fields.Selection([('si', 'SI'), ('no', 'NO')], string="Progetto")
    mat_dichiarazione_note = fields.Char('Note Dichiarazione')
    mat_kit_utilizzato = fields.Char('Strumento Utilizzato')

    mat_con_cabina = fields.Boolean('Con Propria Cabina')
    mat_formula_verificata_note = fields.Char('Nota Formula')

    satm_omologazione = fields.Char('Omologazione Impianto')
    verbale_osservazione_mat_riga_ids = fields.One2many(
        'gevi_verbali.verbale_osservazione_mat_riga',
        'verbale_id',
        string="Osservazioni")
    verbale_rilievo_mat_riga_ids = fields.One2many(
        'gevi_verbali.verbale_rilievo_mat_riga',
        'verbale_id',
        string="Controlli e misure eseguite")
    verbale_raccomandazione_riga_ids = fields.One2many(
        'gevi_verbali.verbale_raccomandazione_riga',
        'verbale_id',
        string="Raccomandazioni")

    # dominio_osservazioni = fields.Char('Dominio Osservazioni')

    # dominio_raccomandazioni = fields.Char('Dominio Raccomandazioni')

    # def _calcola_dominio_osservazioni(self):
    #     if 'Ascensore' in self.impianto_categoria_name:
    #         self.dominio_osservazioni = 'ASC'
    #     if 'Piattaforma' in self.impianto_categoria_name:
    #         self.dominio_osservazioni = 'ASC'
    #     if 'Terra' in self.impianto_categoria_name:
    #         self.dominio_osservazioni = 'RISMAT'
    #     if 'Scariche' in self.impianto_categoria_name:
    #         self.dominio_osservazioni = 'RISSATM'

    # def _calcola_dominio_raccomandazioni(self):
    #     if 'Ascensore' in self.impianto_categoria_name:
    #         self.dominio_raccomandazioni = 'ASC'
    #     if 'Piattaforma' in self.impianto_categoria_name:
    #         self.dominio_raccomandazioni = 'ASC'
    #     if 'Terra' in self.impianto_categoria_name:
    #         self.dominio_raccomandazioni = 'RACMAT'
    #     if 'Scariche' in self.impianto_categoria_name:
    #         self.dominio_raccomandazioni = 'RACSATM'

    # Fine personalizzazione terra / scariche

    @api.depends('ispettore_id')
    def _compute_is_ispettore(self):
        for line in self:
            if line.ispettore_id.user_id.id == line.env.uid:
                line.is_ispettore = True
            else:
                line.is_ispettore = False

    @api.depends('responsabile_tecnico_id')
    def _compute_is_responsabile_tecnico(self):
        for line in self:
            if line.responsabile_tecnico_id.user_id.id == line.env.uid:
                line.is_responsabile_tecnico = True
            else:
                line.is_responsabile_tecnico = False

    @api.depends('impianto_categoria_id')
    def _compute_impianto_categoria_id(self):
        for line in self:
            line.impianto_categoria_name = line.impianto_categoria_id.name

    # STOP MERGE

    cf_cliente = fields.Char("CF Cliente", compute='_compute_riferimenti_impianto', store=True)
    piva_cliente = fields.Char("P.IVA Cliente", compute='_compute_riferimenti_impianto', store=True)
    blocco_amministrativo = fields.Boolean("Blocco Amministrativo", compute='_compute_blocco_amministrativo')
    codice_contratto = fields.Char("Codice Contratto", compute='_compute_blocco_amministrativo', store=True)

    @api.depends('impianto_id')
    def _compute_blocco_amministrativo(self):
        for record in self:
            record.blocco_amministrativo = record.contratto_id.blocco_amministrativo
            record.codice_contratto = record.contratto_id.codice_contratto

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form',
    #                     toolbar=False, submenu=False):
    #     res = super(Verbale, self).fields_view_get(
    #         view_id=view_id, view_type=view_type,
    #         toolbar=toolbar, submenu=submenu)
    #     if view_type != 'search' and self.env.uid == 1:
    # Check if user is in group that allow creation
    # has_my_group = self.env.user.has_group('my_group_with_more_access')
    # if not has_my_group:
    #         if self.state == 'validato':
    #             root = etree.fromstring(res['arch'])
    #             root.set('edit', 'false')
    #             res['arch'] = etree.tostring(root)
    #    return res
    #                       ###vedi file /opt/odoo/addons/gevi_zupdate20171219/models/verbale.py

    @api.depends('impianto_id')
    def _compute_riferimenti_impianto(self):
        for record in self:
            self.impianto_etichetta = record.impianto_id.etichetta
            self.impianto_indirizzo = record.impianto_id.indirizzo
            self.impianto_indirizzo2 = record.impianto_id.indirizzo2
            self.impianto_cap = record.impianto_id.cap
            self.impianto_citta = record.impianto_id.citta
            self.impianto_provincia = record.impianto_id.provincia
            self.cf_cliente = record.impianto_id.customer_id.cf
            self.piva_cliente = record.impianto_id.customer_id.piva

    def aggiorna_dati_impianto(self):
        for line in self:
            line._compute_riferimenti_impianto()

    # @api.multi
    # def carica_attributi_descrittivi(self):
    #     for record in self:
    #         attributi_descrittivi_obj = self.env['gevi.impianti.impianto_riga_descrizione'].search([('impianto_id', '=', record.impianto_id.id)])
    #         self.impianto_riga_descrizione_ids = attributi_descrittivi_obj.ids
    #         # self.impianto_categoria_id = record.impianto_id.impianto_categoria_id.id
    #         # self.impianto_categoria_name = record.impianto_id.impianto_categoria_id.name
    #         # self.customer_id = record.impianto_id.customer_id.id
    #         # self.referente_id = record.impianto_id.customer_id.referente_id.id
    #         # self.attributi_caricati = True
    #     # return attributi_descrittivi_obj

    def aggiorna_prossima_verifica(self):
        for line in self:
            periodicita_verifica_int = int(line.contratto_id.periodicita_verifica)
            start = fields.Date.from_string(line.data_verbale)
            line.data_prossima_verifica = start.replace(year=start.year + periodicita_verifica_int)
            line.impianto_id.data_ultima_verifica = line.data_verbale
            line.data_ultima_verifica = line.data_verbale
            # self.contratto_id.data_ultima_verifica_effettuata = self.data_verbale
            # self.contratto_id.n_verifiche_effettuate += 1

    def aggiorna_contratto(self):
        for line in self:
            contratto_obj = self.env['gevi_contratti.contratto'].search([('id', '=', line.contratto_id.id)])
            contratto_obj.data_ultima_verifica_effettuata = line.data_verbale
            contratto_obj.n_verifiche_effettuate += 1
            contratto_obj.data_prossima_verifica = line.data_prossima_verifica
            contratto_obj.data_ultima_verifica = line.data_verbale
            # edit 28/05/2018 bug manutentore in contratto
            contratto_obj.manutentore_id = line.impianto_id.manutentore_id

            contratto_obj.aggiorna_stato()
            contratto_obj._compute_impianto_ubicazione()

    @api.model
    def create(self, values):
        """
             Create a new record for a model Verbale
             @param values: provides a data for new record
             @return: returns a id of new record
         """
        values['codice_verifica'] = self.env['ir.sequence'].next_by_code(
            'gevi_verbali.verifica')
        # _logger.info('******************************** CREAZIONE: {0}'.format(values['codice_verifica']))
        values['name'] = values['codice_verifica']
        result = super(Verbale, self).create(values)
        return result

    def ricarica_attributi_verbale(self):
        self.attributi_caricati = False
        # riga sottostante cancella tutti gli attributi di riga (riscontro e rilievo) del verbale
        self._delete_attributi_verbale()
        self._carica_attributi_verbale()

    def _delete_attributi_verbale(self):
        for linea in self.verbale_riscontro_riga_ids:
            linea.unlink()
        for linea in self.verbale_rilievo_riga_ids:
            linea.unlink()

    def _carica_attributi_verbale(self):
        if not self.attributi_caricati:
            new_linee_attributo = []
            for linea in self.impianto_categoria_id.impianto_attributo_riscontro_ids:
                new_linee_attributo.append([0, 0, {
                    'name': linea.name,
                }])
            self.verbale_riscontro_riga_ids = new_linee_attributo
            new_linee_attributo = []
            for linea in self.impianto_categoria_id.impianto_attributo_rilievo_ids:
                new_linee_attributo.append([0, 0, {
                    'name': linea.name,
                    'unita_di_misura_id': linea.unita_di_misura_id,
                }])
            self.verbale_rilievo_riga_ids = new_linee_attributo
            new_linee_attributo = []
            for linea in self.impianto_categoria_id.impianto_attributo_rilievo_mat_ids:
                new_linee_attributo.append([0, 0, {
                    'name': linea.name,
                }])
            self.verbale_rilievo_mat_riga_ids = new_linee_attributo
            self.attributi_caricati = True

    # START BJ_Edit (da controllare)
    # @api.depends('gevi_contratti.modalita_pagamento_id')
    # def _anticipa_fattura(self):
    #     if (record.gevi_contratti.modalita_pagamento_id.name == "Fattura Anticipata"):
    #             self.fattura_anticipata = True
    # @api.depends('contratto_id')
    # def _verifica(self):
    #     record = self
    #     self.periodica = record.contratto_id.verifica_periodica
    #     self.data_ultima_verifica = record.contratto_id.data_ultima_verifica
    # STOP BJ_Edit

    def action_bozza(self):
        if self.blocco_amministrativo is True:
            raise exceptions.ValidationError(
                'Sul contratto {0} è presente un blocco amministrativo e pertanto non è possibile procedere in alcun modo.'.format(
                    self.codice_contratto))
        else:
            self.state = 'bozza'

    def action_assegnato(self):
        if self.blocco_amministrativo is True:
            raise exceptions.ValidationError(
                'Sul contratto {0} è presente un blocco amministrativo e pertanto non è possibile procedere in alcun modo.'.format(
                    self.codice_contratto))
        else:
            self.state = 'assegnato'
            self.data_assegnazione = fields.Date.context_today(self)

    # START SDC EDIT 17/12/2016
    def action_eseguito(self):
        for line in self:
            if line.blocco_amministrativo is True:
                raise exceptions.ValidationError(
                    'Sul contratto {0} è presente un blocco amministrativo e pertanto non è possibile procedere in alcun modo.'.format(
                        line.codice_contratto))
            else:
                if line.impianto_categoria_id.name == 'Ascensore Generico':
                    raise exceptions.ValidationError("Per procedere è necessario cambiare la categoria dell'impianto")
                else:
                    line.data_esecuzione = fields.Date.context_today(line)
                    line._carica_attributi_verbale()
                    line._calcola_norma_ascensori()
                    line.state = 'eseguito'

    def action_confermato(self):
        if self.blocco_amministrativo is True:
            raise exceptions.ValidationError(
                'Sul contratto {0} è presente un blocco amministrativo e pertanto non è possibile procedere in alcun modo.'.format(
                    self.codice_contratto))
        else:
            for record in self:
                self.data_conferma = fields.Date.context_today(self)
                self.impianto_id.impianto_categoria_id = self.impianto_categoria_id
                # commentato per problema in fase si conferma del verbale su write del res.partner
                # self.contratto_id.impianto_categoria_id = self.impianto_categoria_id
                self.timbro_ispettore = (self.env.user).timbro_isp
                # self.state = 'confermato'
                if self.name.find('Prog') != -1:
                    self.name = self.env['ir.sequence'].with_context(ir_sequence_date='2022-01-01').next_by_code(
                        'gevi_verbali.verbale')
                    # self.name = self.env['ir.sequence'].next_by_code('gevi_verbali.verbale')
                    self.data_verbale = fields.Date.context_today(self)
                self.state = 'confermato'

    # START SDC EDIT 17/12/2016
    def action_validato(self):
        if self.blocco_amministrativo is True:
            raise exceptions.ValidationError(
                'Sul contratto {0} è presente un blocco amministrativo e pertanto non è possibile procedere in alcun modo.'.format(
                    self.codice_contratto))
        else:
            if self.is_responsabile_tecnico:
                self.timbro_responsabile_tecnico = (self.env.user).timbro_rt
                # self.data_validazione = fields.Date.context_today(self)
                self.impianto_id.manutentore_id = self.manutentore_id
                if self.periodica is True:
                    self.aggiorna_prossima_verifica()
                    self.aggiorna_contratto()
                self.state = 'validato'
            else:
                raise exceptions.ValidationError(
                    'Solo il Responsabile Tecnico può validare definitivamente il verbale!')

                # return {
                #     'type': 'ir.actions.client',
                #     'tag': 'action_warn',
                #     'name': 'Warning',
                #     'params': {
                #         'title': 'Attenzione!',
                #         'text': 'Solo il Responsabile Tecnico può validare definitivamente il verbale',
                #         'sticky': True
                #     }
                # }

        # SCADENZA CONTRATTO QUANDO IL VERBALE DA EMETTERE E' L'ULTIMO (vecchia versione)
        # if self.periodica is True:
        #     contratto_obj = self.env['gevi_contratti.contratto'].search([('id', '=', self.contratto_id)], limit=1)
        #     contratto_obj.data_ultima_verifica_effettuata = self.data_verbale
        #     contratto_obj.n_verifiche_effettuate += 1
        #     if contratto_obj.n_verifiche_contratto == contratto_obj.n_verifiche_effettuate:
        #         contratto_obj.action_scaduto()

        if self.fattura_anticipata is False:
            self._crea_ordine_vendita()

    # STOP SDC EDIT 17/12/2016

    def action_annullato(self):
        if self.blocco_amministrativo is True:
            raise exceptions.ValidationError(
                'Sul contratto {0} è presente un blocco amministrativo e pertanto non è possibile procedere in alcun modo.'.format(
                    self.codice_contratto))
        else:
            self.state = 'annullato'

    def _calcola_norma_ascensori(self):
        for line in self:
            if 'Ascensore' in line.impianto_categoria_name:
                anno_collaudo_obj = self.env['gevi.impianti.impianto_riga_descrizione'].search(
                    ['&', ('impianto_id', '=', line.impianto_id.id), ('name', 'ilike', "Data collaudo")], limit=1)
                anno_collaudo_int = 1900
                for anno_collaudo in anno_collaudo_obj:
                    anno_collaudo_int = int(anno_collaudo.valore_attributo)
                norma_obj = self.env['gevi_verbali.normeascensori'].search(
                    ['&', ('anno_inizio', '<=', anno_collaudo_int), ('anno_fine', '>=', anno_collaudo_int)], limit=1)
                line.norma_riferimento = norma_obj.norma_collaudo
                if not line.periodica:
                    if norma_obj.norma_collaudo:
                        line.norma_riferimento = norma_obj.norma_collaudo + ' - ' + norma_obj.norma_straordinaria

    def _crea_ordine_vendita(self):
        for line in self:
            # record = self
            ordine_obj = self.env['sale.order']
            costo = fields.Float(default=0.0, digits=(12, 2))
            ubicazione = fields.Char()
            # if self.impianto_id.indirizzo2 is False:
            #     self.impianto_indirizzo2 = ' '
            codice_prodotto = fields.Char()
            sigla_periodica = fields.Char()
            sigla_impianto = fields.Char()
            ubicazione = '{0} {1}, {2} {3} - {4} {5} ({6})'.format(
                line.customer_id.name.encode('utf-8'),
                line.impianto_id.etichetta.encode('utf-8'),
                line.impianto_id.indirizzo.encode('utf-8'),
                ' ' if line.impianto_id.indirizzo2 is False else line.impianto_id.indirizzo2,
                line.impianto_id.cap,
                line.impianto_id.citta,
                line.impianto_id.provincia
            )

        if line.periodica is True:
            line.sigla_periodica = 'P'
            line.costo = line.contratto_id.costo_verifica_periodica
        else:
            line.sigla_periodica = 'S'
            line.costo = line.contratto_id.costo_verifica_straordinaria

        line.sigla_impianto = self.env['gevi.impianti.impianto_categoria'].search(
            [('name', '=', line.impianto_categoria_id.name)], limit=1).descrizione
        if line.fattura_anticipata is True:
            line.codice_prodotto = 'VV{0}-{1}-FA'.format(line.sigla_periodica, line.sigla_impianto)
        else:
            line.codice_prodotto = 'VV{0}-{1}'.format(line.sigla_periodica, line.sigla_impianto)
        if line.customer_id.tipo_cliente_id.name == "Condominio":
            line.codice_prodotto += 'C'
        # _logger.info('******************************** CODICE PRODOTTO: {0}'.format(self.codice_prodotto))
        prodotto_obj = self.env['product.product'].search([('name', '=', line.codice_prodotto)], limit=1)
        data_verbale_formato_it = fields.Date.from_string(line.data_verbale)
        ordine = ordine_obj.create({
            # 'name': ,
            'origin': line.name,
            'verbale_id': line.id,
            'date_order': fields.Date.context_today(line),
            'partner_id': line.customer_id.id,
            'partner_invoice_id': line.customer_id.id,
            'order_policy': 'manual',
            'order_line': [(0, 0, {
                'product_id': prodotto_obj.id,
                'name': (prodotto_obj.description_sale).format(line.name, data_verbale_formato_it.strftime("%d/%m/%Y"),
                                                               line.ubicazione.decode('utf-8'),
                                                               line.data_ultima_verifica),
                'price_unit': line.costo,
                'discount': 0.0,
                'sequence': 10,
                'verbale_id': line.id,
            })],
        })

        # verifico agente associato ad amministratore per associazione PESCARA
        if line.referente_id and line.referente_id.agente_id:
            if line.referente_id.agente_id.user_id.has_group('__export__.res_groups_90'):
                ordine.write({'user_id': line.referente_id.agente_id.user_id.id})

        ordine.action_confirm()
        return ordine

        # ordine_linea_obj = self.env['sale.order.line']
        # costo = fields.Float("Costo", digits=(12, 2), default=50.0)
        # # if self.periodica is True:
        # #     self.costo = self.contratto_id.costo_verifica_periodica
        # # else:
        # #     self.costo = self.contratto_id.costo_verifica_straordinaria
        # ordine_linea = ordine_linea_obj.create({
        #     'name': 'Verbale di verifica',
        #     'order_id': ordine.id,
        #     'price_unit': self.costo,
        #     'discount': 0.0,
        #     'product_uom_qty': 1,
        #     'product_uos_qty': 1,
        #     'sequence': 10,
        #     'state': 'confirmed',
        #     'delay': 0.0,
        #     })
        # # ordine_obj.action_wait(self)

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

    @api.onchange("ispettore_id", "responsabile_tecnico_id")
    def _onchange_ispettore_id_responsabile_tecnico_id(self):
        if self.ispettore_id and self.responsabile_tecnico_id:
            self.state = "assegnato"
