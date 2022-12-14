# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)

try:
    import base64

    from odoo import api, fields, models
    from odoo.exceptions import UserError
    from odoo.tools.translate import _


    from odoo.addons.gevi_fatturapa.bindings.fatturapa_v_1_2 import (
	FatturaElettronica,
	FatturaElettronicaHeaderType,
	DatiTrasmissioneType,
	IdFiscaleType,
	ContattiTrasmittenteType,
	CedentePrestatoreType,
	AnagraficaType,
	IndirizzoType,
	IscrizioneREAType,
	CessionarioCommittenteType,
	RappresentanteFiscaleType,
	DatiAnagraficiCedenteType,
	DatiAnagraficiCessionarioType,
	DatiAnagraficiRappresentanteType,
	TerzoIntermediarioSoggettoEmittenteType,
	DatiAnagraficiTerzoIntermediarioType,
	FatturaElettronicaBodyType,
	DatiGeneraliType,
	DatiRitenutaType,
	DettaglioLineeType,
	DatiBeniServiziType,
	DatiRiepilogoType,
	DatiGeneraliDocumentoType,
	DatiDocumentiCorrelatiType,
	ContattiType,
	DatiPagamentoType,
	DettaglioPagamentoType,
	AllegatiType,
	ScontoMaggiorazioneType,
	CodiceArticoloType
    )

    from odoo.addons.gevi_fatturapa.models.account import (
        RELATED_DOCUMENT_TYPES
    )
except ImportError as err:
    _logger.info("errore import")


try:
    from unidecode import unidecode
    from pyxb.exceptions_ import SimpleFacetValueError, SimpleTypeValueError
except ImportError as err:
    _logger.info("errore in import fatturapa.wizard.export")


class WizardExportFatturapa(models.TransientModel):
    _name = "fatturapa.wizard.export"
    _description = "Export Fattura Elettronica"

    @api.model
    def _domain_ir_values(self):
        """Get all print actions for current model"""
        return [('model', '=', self.env.context.get('active_model', False)),
                ('key2', '=', 'client_print_multi')]

    report_print_menu = fields.Many2one(
        comodel_name='ir.values',
        domain=_domain_ir_values,
        help="Questo report verr?? automaticamente incluso nell XML creato")

    def saveAttachment(self, fatturapa, number):

        company = self.env.user.company_id

        if not company.vat:
            raise UserError(
                _('La partita iva di %s non ?? impostata.') % company.name)
        if (
                company.fatturapa_sender_partner and not
        company.fatturapa_sender_partner.vat
        ):
            raise UserError(
                _('Partner %s TIN not set.')
                % company.fatturapa_sender_partner.name
            )
        vat = company.vat
        if company.fatturapa_sender_partner:
            vat = company.fatturapa_sender_partner.vat
        vat = vat.replace(' ', '').replace('.', '').replace('-', '')
        attach_obj = self.env['fatturapa.attachment.out']
        attach_vals = {
            'name': '%s_%s.xml' % (vat, str(number)),
            'datas_fname': '%s_%s.xml' % (vat, str(number)),
            'datas': base64.encodestring(fatturapa.toxml("UTF-8")),
            'type': 'binary',
        }
        return attach_obj.create(attach_vals)

    def setProgressivoInvio(self, fatturapa):

        company = self.env.user.company_id

        # La richiesta del cliente ?? quella di avere progressivo uguale a numero fattura
        # quindi questo metodo non dovrebbe essere mai richiamato
        fatturapa_sequence = company.fatturapa_sequence_id

        if not fatturapa_sequence:
            raise UserError("La sequence per la Fattura Elettronica non ?? configurata")
        number = fatturapa_sequence.next_by_id()
        try:
            fatturapa.FatturaElettronicaHeader.DatiTrasmissione. \
                ProgressivoInvio = number
        except (SimpleFacetValueError, SimpleTypeValueError) as e:
            msg = _(
                'FatturaElettronicaHeader.DatiTrasmissione.'
                'ProgressivoInvio:\n%s'
            ) % unicode(e)
            raise UserError(msg)
        return number

    def setProgressivoAsFattura(self, inv, fatturapa):
        # ottengo le ultime cinque cifre del
        pa_number = inv.number[-5:]
        try:
            fatturapa.FatturaElettronicaHeader.DatiTrasmissione. \
                ProgressivoInvio = pa_number
        except (SimpleFacetValueError, SimpleTypeValueError) as e:
            msg = _(
                'FatturaElettronicaHeader.DatiTrasmissione.'
                'ProgressivoInvio:\n%s'
            ) % unicode(e)
            raise UserError(msg)
        return pa_number

    def _setIdTrasmittente(self, company, fatturapa):

        if not company.country_id:
            raise UserError(
                "Il codice nazione dell'azienda non ?? impostato")
        IdPaese = company.fatturapa_trasmittente[0:2]

        IdCodice = company.fatturapa_trasmittente[2:]
        if not IdCodice:
            if company.vat:
                IdCodice = company.vat[2:]
        if not IdCodice:
            raise UserError("La partita iva dell'azienda non ?? impostata")

        fatturapa.FatturaElettronicaHeader.DatiTrasmissione. \
            IdTrasmittente = IdFiscaleType(
            IdPaese=IdPaese, IdCodice=IdCodice)

        return True

    def _setFormatoTrasmissione(self, partner, fatturapa):
        if partner.is_pa():
            fatturapa.FatturaElettronicaHeader.DatiTrasmissione. \
                FormatoTrasmissione = 'FPA12'
        else:
            fatturapa.FatturaElettronicaHeader.DatiTrasmissione. \
                FormatoTrasmissione = 'FPR12'

        return True

    def _setCodiceDestinatario(self, partner, fatturapa):
        pec_destinatario = None
        if partner.is_pa():
            if not partner.codice_ipa:
                raise UserError(
                    "Il cliente {} ?? una Pubblica Amministrazione ma il codice IPA non ?? impostato".format(partner.name))
            code = partner.codice_ipa
        else:
            if not partner.codice_destinatario:
                raise UserError(
                    "Il cliente {} non ?? una Pubblica Amministrazione ma il Codice Destinatario non ?? impostato".format(partner.name))
            code = partner.codice_destinatario
            if code == '0000000':
                if not partner.pec_destinatario:
                    # se cliente tipo condominio allora puo non avere la pec
                    if partner.tipo_cliente_id.id != 5 and partner.company_type != 'person':
                        raise UserError(
                            "Il cliente %s con Codice Destinatario '0000000' deve avere la PEC impostata" % partner.name)
                pec_destinatario = partner.pec_destinatario
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione. \
            CodiceDestinatario = code.upper()
        if pec_destinatario:
            fatturapa.FatturaElettronicaHeader.DatiTrasmissione. \
                PECDestinatario = pec_destinatario

        return True

    def _setContattiTrasmittente(self, company, fatturapa):

        if not company.phone:
            raise UserError("Il numero di telefono dell'azienda non ?? impostato")
        Telefono = company.phone

        if not company.email:
            raise UserError("L'indirizzo email dell'azienda non ?? impostato")
        Email = company.email
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione. \
            ContattiTrasmittente = ContattiTrasmittenteType(
            Telefono=Telefono, Email=Email)

        return True

    def setDatiTrasmissione(self, company, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione = (
            DatiTrasmissioneType())
        self._setIdTrasmittente(company, fatturapa)
        self._setFormatoTrasmissione(partner, fatturapa)
        self._setCodiceDestinatario(partner, fatturapa)
        # self._setContattiTrasmittente(company, fatturapa)

    def _setDatiAnagraficiCedente(self, CedentePrestatore, company):

        if not company.vat:
            raise UserError("La partita iva dell'azienda non ?? impostata")
        CedentePrestatore.DatiAnagrafici = DatiAnagraficiCedenteType()
        fatturapa_fp = company.fatturapa_fiscal_position_id
        if not fatturapa_fp:
            raise UserError(
                "La posizione fiscale per la Fatturazione Elettronica "
                "non ?? impostata per l'azienda {}. "
                "(Impostare su Contabilit?? --> Configurazione --> Impostazioni --> "
                "Fatturazione Elettronica)".format(company.name)
            )
        CedentePrestatore.DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
            IdPaese=company.country_id.code, IdCodice=company.vat[2:])
        CedentePrestatore.DatiAnagrafici.Anagrafica = AnagraficaType(
            Denominazione=company.name)

        if company.partner_id.cf:
            CedentePrestatore.DatiAnagrafici.CodiceFiscale = (
                company.partner_id.cf)
        CedentePrestatore.DatiAnagrafici.RegimeFiscale = fatturapa_fp.code
        return True

    def _setAlboProfessionaleCedente(self, CedentePrestatore, company):
        # TODO Albo professionale, for now the main company is considered
        # to be a legal entity and not a single person
        # 1.2.1.4   <AlboProfessionale>
        # 1.2.1.5   <ProvinciaAlbo>
        # 1.2.1.6   <NumeroIscrizioneAlbo>
        # 1.2.1.7   <DataIscrizioneAlbo>
        return True

    def _setSedeCedente(self, CedentePrestatore, company):

        if not company.street:
            raise UserError("Impostare l'indirizzo dell'azienda")
        if not company.zip:
            raise UserError("Impostare il CAP dell'azienda")
        if not company.city:
            raise UserError("Impostare la citt?? dell'azienda")
        #commentato per implementazione provincia in gevi
        # if not company.country_id:
        #     raise UserError("Impostare la provincia dell'azienda")

        if not company.partner_id.provincia:
            raise UserError("Impostare la provincia dell'azienda")

        # TODO: manage address number in <NumeroCivico>
        # see https://github.com/OCA/partner-contact/pull/96
        CedentePrestatore.Sede = IndirizzoType(
            Indirizzo=company.street,
            CAP=company.zip,
            Comune=company.city,
            Nazione=company.country_id.code,
            Provincia=company.partner_id.provincia)
        return True

    def _setStabileOrganizzazione(self, CedentePrestatore, company):
        if company.fatturapa_stabile_organizzazione:
            stabile_organizzazione = company.fatturapa_stabile_organizzazione
            if not stabile_organizzazione.street:
                raise UserError(
                    _('Street not set for %s') % stabile_organizzazione.name)
            if not stabile_organizzazione.zip:
                raise UserError(
                    _('ZIP not set for %s') % stabile_organizzazione.name)
            if not stabile_organizzazione.city:
                raise UserError(
                    _('City not set for %s') % stabile_organizzazione.name)
            if not stabile_organizzazione.country_id:
                raise UserError(
                    _('Country not set for %s') % stabile_organizzazione.name)
            CedentePrestatore.StabileOrganizzazione = IndirizzoType(
                Indirizzo=stabile_organizzazione.street,
                CAP=stabile_organizzazione.zip,
                Comune=stabile_organizzazione.city,
                Nazione=stabile_organizzazione.country_id.code,
                Provincia=stabile_organizzazione.partner_id.provincia)
        return True

    def _setRea(self, CedentePrestatore, company):

        if company.fatturapa_rea_provincia and company.fatturapa_rea_number:
            CedentePrestatore.IscrizioneREA = IscrizioneREAType(
                Ufficio=(
                        company.fatturapa_rea_provincia or None),
                NumeroREA=company.fatturapa_rea_number or None,
                CapitaleSociale=(
                        company.fatturapa_rea_capital and
                        '%.2f' % company.fatturapa_rea_capital or None),
                SocioUnico=(company.fatturapa_rea_partner or None),
                StatoLiquidazione=company.fatturapa_rea_liquidation or None
            )

    def _setContatti(self, CedentePrestatore, company):
        CedentePrestatore.Contatti = ContattiType(
            Telefono=company.fatturapa_tel or None,
            Fax=company.fatturapa_fax or None,
            Email=company.fatturapa_email or None
        )

    def _setPubAdministrationRef(self, CedentePrestatore, company):
        if company.fatturapa_pub_administration_ref:
            CedentePrestatore.RiferimentoAmministrazione = (
                company.fatturapa_pub_administration_ref)

    def setCedentePrestatore(self, company, fatturapa):
        fatturapa.FatturaElettronicaHeader.CedentePrestatore = (
            CedentePrestatoreType())
        self._setDatiAnagraficiCedente(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)
        self._setSedeCedente(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)
        self._setAlboProfessionaleCedente(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)
        self._setStabileOrganizzazione(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)
        # TODO: add Contacts
        self._setRea(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)
        self._setContatti(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)
        self._setPubAdministrationRef(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)

    def _setDatiAnagraficiCessionario(self, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader.CessionarioCommittente. \
            DatiAnagrafici = DatiAnagraficiCessionarioType()
        if not partner.piva and not partner.cf:
            raise UserError("La Partita Iva e il Codice Fiscale non sono impostati per il Cliente %s" % partner.name)
        if partner.cf:
            fatturapa.FatturaElettronicaHeader.CessionarioCommittente. \
                DatiAnagrafici.CodiceFiscale = partner.cf
        if partner.piva:
            if partner.piva[2:]=='IT' and len(partner.piva)<12:
                raise UserError("La Partita Iva del Cliente %s non sembra essere delle giuste dimensioni" % partner.name)
            fatturapa.FatturaElettronicaHeader.CessionarioCommittente. \
                DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
                IdPaese=partner.piva[0:2], IdCodice=partner.piva[2:])
        if partner.company_type == 'company':
            fatturapa.FatturaElettronicaHeader.CessionarioCommittente. \
                DatiAnagrafici.Anagrafica = AnagraficaType(
                Denominazione=partner.name)
        elif partner.company_type == 'person':
            if not partner.lastname or not partner.firstname:
                raise UserError("Il Cliente privato %s deve avere nome e cognome" % partner.name)
            fatturapa.FatturaElettronicaHeader.CessionarioCommittente. \
                DatiAnagrafici.Anagrafica = AnagraficaType(
                Cognome=partner.lastname,
                Nome=partner.firstname
            )

        if partner.eori_code:
            fatturapa.FatturaElettronicaHeader.CessionarioCommittente. \
                DatiAnagrafici.Anagrafica.CodEORI = partner.eori_code

        return True

    def _setDatiAnagraficiRappresentanteFiscale(self, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader.RappresentanteFiscale = (
            RappresentanteFiscaleType())
        fatturapa.FatturaElettronicaHeader.RappresentanteFiscale. \
            DatiAnagrafici = DatiAnagraficiRappresentanteType()
        if not partner.piva and not partner.cf:
            raise UserError("Il Cliente privato %s deve avere nome e cognome" % partner.name)
        if partner.cf:
            fatturapa.FatturaElettronicaHeader.RappresentanteFiscale. \
                DatiAnagrafici.CodiceFiscale = partner.cf
        if partner.piva:
            fatturapa.FatturaElettronicaHeader.RappresentanteFiscale. \
                DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
                IdPaese=partner.piva[0:2], IdCodice=partner.piva[2:])
        fatturapa.FatturaElettronicaHeader.RappresentanteFiscale. \
            DatiAnagrafici.Anagrafica = AnagraficaType(
            Denominazione=partner.name)
        if partner.eori_code:
            fatturapa.FatturaElettronicaHeader.RappresentanteFiscale. \
                DatiAnagrafici.Anagrafica.CodEORI = partner.eori_code

        return True

    def _setTerzoIntermediarioOSoggettoEmittente(self, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader. \
            TerzoIntermediarioOSoggettoEmittente = (
            TerzoIntermediarioSoggettoEmittenteType()
        )
        fatturapa.FatturaElettronicaHeader. \
            TerzoIntermediarioOSoggettoEmittente. \
            DatiAnagrafici = DatiAnagraficiTerzoIntermediarioType()
        if not partner.vat and not partner.fiscalcode:
            raise UserError("La Partita Iva e il Codice Fiscale  del Terzo Intermediario non sono impostati")
        if partner.cf:
            fatturapa.FatturaElettronicaHeader. \
                TerzoIntermediarioOSoggettoEmittente. \
                DatiAnagrafici.CodiceFiscale = partner.cf
        if partner.piva:
            fatturapa.FatturaElettronicaHeader. \
                TerzoIntermediarioOSoggettoEmittente. \
                DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
                IdPaese=partner.piva[0:2], IdCodice=partner.piva[2:])
        fatturapa.FatturaElettronicaHeader. \
            TerzoIntermediarioOSoggettoEmittente. \
            DatiAnagrafici.Anagrafica = AnagraficaType(
            Denominazione=partner.name)
        if partner.eori_code:
            fatturapa.FatturaElettronicaHeader. \
                TerzoIntermediarioOSoggettoEmittente. \
                DatiAnagrafici.Anagrafica.CodEORI = partner.eori_code
        fatturapa.FatturaElettronicaHeader.SoggettoEmittente = 'TZ'
        return True

    def _setSedeCessionario(self, partner, fatturapa):

        if not partner.street:
            raise UserError("Impostare l'indirizzo del Cliente")
        if not partner.zip:
            raise UserError("Impostare il CAP del Cliente")
        if not partner.city:
            raise UserError("Impostare la citt?? del Cliente")
        if not partner.provincia:
            raise UserError("Impostare la provincia del Cliente")
        if not partner.country_id:
            raise UserError("Impostare la nazione del Cliente")

        # TODO: manage address number in <NumeroCivico>
        fatturapa.FatturaElettronicaHeader.CessionarioCommittente.Sede = (
            IndirizzoType(
                Indirizzo=partner.street,
                CAP=partner.zip,
                Comune=partner.city,
                Provincia=partner.provincia,
                Nazione=partner.country_id.code))

        return True

    def setRappresentanteFiscale(self, company, fatturapa):
        if company.fatturapa_tax_representative:
            self._setDatiAnagraficiRappresentanteFiscale(
                company.fatturapa_tax_representative, fatturapa)
        return True

    def setCessionarioCommittente(self, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader.CessionarioCommittente = (
            CessionarioCommittenteType())
        self._setDatiAnagraficiCessionario(partner, fatturapa)
        self._setSedeCessionario(partner, fatturapa)

    def setTerzoIntermediarioOSoggettoEmittente(self, company, fatturapa):
        if company.fatturapa_sender_partner:
            self._setTerzoIntermediarioOSoggettoEmittente(
                company.fatturapa_sender_partner, fatturapa)
        return True

    def setDatiGeneraliDocumento(self, invoice, body):

        # TODO DatiSAL

        body.DatiGenerali = DatiGeneraliType()

        if invoice.type == 'out_invoice':
            TipoDocumento = 'TD01'
            if not invoice.number:
                raise UserError("La Fattura non ha un numero")

        if invoice.type == 'out_refund':
            TipoDocumento = 'TD04'
            if not invoice.number:
                raise UserError("La Nota credito non ha un numero")

        ImportoTotaleDocumento = invoice.amount_total
        if invoice.split_payment:
            ImportoTotaleDocumento += invoice.amount_sp
        body.DatiGenerali.DatiGeneraliDocumento = DatiGeneraliDocumentoType(
            TipoDocumento=TipoDocumento,
            Divisa=invoice.currency_id.name,
            Data=invoice.date_invoice,
            Numero=invoice.number,
            ImportoTotaleDocumento='%.2f' % ImportoTotaleDocumento)

        # TODO: DatiRitenuta, DatiBollo, DatiCassaPrevidenziale,
        # ScontoMaggiorazione, Arrotondamento,

        # DatiRitenuta
        for tax in invoice.tax_line_ids:
            if "Ritenuta" in tax.name:
                tipo_ritenuta = False
                importo_ritenuta = '%.2f' % abs(tax.amount)
                aliquota_ritenuta = '%.2f' % abs(tax.tax_id.amount)
                causale_pagamento = 'A'
                if invoice.partner_id.referente_id.x_tipo_persona == 'fisica':
                    tipo_ritenuta = 'RT01'
                if invoice.partner_id.referente_id.x_tipo_persona == 'giuridica':
                    tipo_ritenuta = 'RT02'
                if not tipo_ritenuta:
                    raise UserError("L'amministratore {} non ha un Tipo Persona impostato".format(invoice.partner_id.referente_id.name))
                body.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta = DatiRitenutaType(
                    ImportoRitenuta=importo_ritenuta,
                    AliquotaRitenuta=aliquota_ritenuta,
                    CausalePagamento=causale_pagamento,
                    TipoRitenuta=tipo_ritenuta
                )



        if invoice.comment:
            # max length of Causale is 200
            caus_list = invoice.comment.split('\n')
            for causale in caus_list:
                # Remove non latin chars, but go back to unicode string,
                # as expected by String200LatinType
                causale = causale.encode(
                    'latin', 'ignore').decode('latin')
                body.DatiGenerali.DatiGeneraliDocumento.Causale.append(causale)

        if invoice.company_id.fatturapa_art73:
            body.DatiGenerali.DatiGeneraliDocumento.Art73 = 'SI'

        return True

    def setRelatedDocumentTypes(self, invoice, body):
        for line in invoice.invoice_line_ids:
            for related_document in line.related_documents:
                doc_type = RELATED_DOCUMENT_TYPES[related_document.type]
                documento = DatiDocumentiCorrelatiType()
                if related_document.name:
                    documento.IdDocumento = related_document.name
                if related_document.lineRef:
                    documento.RiferimentoNumeroLinea.append(
                        line.ftpa_line_number)
                if related_document.date:
                    documento.Data = related_document.date
                if related_document.numitem:
                    documento.NumItem = related_document.numitem
                if related_document.code:
                    documento.CodiceCommessaConvenzione = related_document.code
                if related_document.cup:
                    documento.CodiceCUP = related_document.cup
                if related_document.cig:
                    documento.CodiceCIG = related_document.cig
                getattr(body.DatiGenerali, doc_type).append(documento)
        for related_document in invoice.related_documents:
            doc_type = RELATED_DOCUMENT_TYPES[related_document.type]
            documento = DatiDocumentiCorrelatiType()
            if related_document.name:
                documento.IdDocumento = related_document.name
            if related_document.date:
                documento.Data = related_document.date
            if related_document.numitem:
                documento.NumItem = related_document.numitem
            if related_document.code:
                documento.CodiceCommessaConvenzione = related_document.code
            if related_document.cup:
                documento.CodiceCUP = related_document.cup
            if related_document.cig:
                documento.CodiceCIG = related_document.cig
            getattr(body.DatiGenerali, doc_type).append(documento)
        return True

    def setDatiTrasporto(self, invoice, body):
        return True

    def setDatiDDT(self, invoice, body):
        return True

    def _get_prezzo_unitario(self, line):
        res = line.price_unit
        if (
                line.invoice_line_tax_ids and
                line.invoice_line_tax_ids[0].price_include
        ):
            res = line.price_unit / (
                    1 + (line.invoice_line_tax_ids[0].amount / 100))
        return res

    def setDettaglioLinee(self, invoice, body):

        body.DatiBeniServizi = DatiBeniServiziType()
        # TipoCessionePrestazione not handled

        line_no = 1
        price_precision = self.env['decimal.precision'].precision_get(
            'Product Price')
        uom_precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for line in invoice.invoice_line_ids:
            has_ritenuta = False

            if not line.invoice_line_tax_ids:
                raise UserError(
                    _("Invoice line %s does not have tax") % line.name)
            # if len(line.invoice_line_tax_ids) > 1:
            #     raise UserError(
            #         _("Too many taxes for invoice line %s") % line.name)
            for tax_line in line.invoice_line_tax_ids:
                if tax_line.amount < 0:
                    has_ritenuta = True
                else:
                    aliquota = tax_line.amount

#            if line.invoice_line_tax_ids[0].amount < 0:
#                aliquota = line.invoice_line_tax_ids[1].amount
#                has_ritenuta = True
#            else:
#                aliquota = line.invoice_line_tax_ids[0].amount

            AliquotaIVA = '%.2f' % (aliquota)
            line.ftpa_line_number = line_no
            prezzo_unitario = self._get_prezzo_unitario(line)
            quantita = '%.2f' % (line.quantity)
            unita_misura = line.uom_id and (unidecode(line.uom_id.name))
            if unita_misura == 'Unita':
                unita_misura = 'NR'
            DettaglioLinea = DettaglioLineeType(
                NumeroLinea=str(line_no),
                # can't insert newline with pyxb
                # see https://tinyurl.com/ycem923t
                # and '&#10;' would not be correctly visualized anyway
                # (for example firefox replaces '&#10;' with space
                Descrizione=line.name.replace('\n', ' '),
                PrezzoUnitario=('%.' + str(
                    price_precision
                ) + 'f') % prezzo_unitario,
                Quantita=quantita,
                UnitaMisura=unita_misura or None,
                PrezzoTotale='%.2f' % line.price_subtotal,
                AliquotaIVA=AliquotaIVA)
            if has_ritenuta:
                DettaglioLinea.Ritenuta = 'SI'

            if line.discount:
                ScontoMaggiorazione = ScontoMaggiorazioneType(
                    Tipo='SC',
                    Percentuale='%.2f' % line.discount
                )
                DettaglioLinea.ScontoMaggiorazione.append(ScontoMaggiorazione)
            if aliquota == 0.0:
                # ivaaaaa
                if line.invoice_line_tax_ids[0].amount < 0:
                    if not line.invoice_line_tax_ids[0].kind_id:
                        raise UserError(
                            _("No 'nature' field for tax %s") %
                        line.invoice_line_tax_ids[0].name)
                else:
                    if not line.invoice_line_tax_ids[0].kind_id:
                        raise UserError(
                            _("No 'nature' field for tax %s") %
                        line.invoice_line_tax_ids[0].name)
                DettaglioLinea.Natura = line.invoice_line_tax_ids[
                    0
                ].kind_id.code
            if line.admin_ref:
                DettaglioLinea.RiferimentoAmministrazione = line.admin_ref
            if line.product_id:
                if line.product_id.default_code:
                    CodiceArticolo = CodiceArticoloType(
                        CodiceTipo='ODOO',
                        CodiceValore=line.product_id.default_code
                    )
                    DettaglioLinea.CodiceArticolo.append(CodiceArticolo)
                if line.product_id.barcode:
                    CodiceArticolo = CodiceArticoloType(
                        CodiceTipo='EAN',
                        CodiceValore=line.product_id.barcode
                    )
                    DettaglioLinea.CodiceArticolo.append(CodiceArticolo)
            line_no += 1

            body.DatiBeniServizi.DettaglioLinee.append(DettaglioLinea)

        return True

    def setDatiRiepilogo(self, invoice, body):
        for tax_line in invoice.tax_line_ids:
            if tax_line.amount > 0:
                tax = tax_line.tax_id
                riepilogo = DatiRiepilogoType(
                    AliquotaIVA='%.2f' % tax.amount,
                    ImponibileImporto='%.2f' % tax_line.base,
                    Imposta='%.2f' % tax_line.amount
                )
                if tax.amount == 0.0:
                    if not tax.kind_id:
                        raise UserError(
                            _("No 'nature' field for tax %s") % tax.name)
                    riepilogo.Natura = tax.kind_id.code
                    if not tax.law_reference:
                        raise UserError(
                            _("No 'law reference' field for tax %s") % tax.name)
                    riepilogo.RiferimentoNormativo = tax.law_reference
                if tax.payability:
                    riepilogo.EsigibilitaIVA = tax.payability
                # TODO

                # el.remove(el.find('SpeseAccessorie'))
                # el.remove(el.find('Arrotondamento'))

                body.DatiBeniServizi.DatiRiepilogo.append(riepilogo)

        return True

    def setDatiPagamento(self, invoice, body):
        if invoice.payment_term_id:
            DatiPagamento = DatiPagamentoType()
            if not invoice.payment_term_id.fatturapa_pt_id:
                raise UserError(
                    _('Payment term %s does not have a linked e-invoice '
                      'payment term') % invoice.payment_term_id.name)
            if not invoice.payment_term_id.fatturapa_pm_id:
                raise UserError(
                    _('Payment term %s does not have a linked e-invoice '
                      'payment method') % invoice.payment_term_id.name)
            DatiPagamento.CondizioniPagamento = (
                invoice.payment_term_id.fatturapa_pt_id.code)
            move_line_pool = self.env['account.move.line']
            payment_line_ids = invoice.get_receivable_line_ids()
            for move_line_id in payment_line_ids:
                move_line = move_line_pool.browse(move_line_id)
                ImportoPagamento = '%.2f' % move_line.debit
                DettaglioPagamento = DettaglioPagamentoType(
                    ModalitaPagamento=(
                        invoice.payment_term_id.fatturapa_pm_id.code),
                    DataScadenzaPagamento=move_line.date_maturity,
                    ImportoPagamento=ImportoPagamento
                )
                if invoice.banca_id:
                    DettaglioPagamento.IstitutoFinanziario = (
                        invoice.banca_id.bank_id.name)
                    if invoice.banca_id.acc_number:
                        DettaglioPagamento.IBAN = (
                            ''.join(invoice.banca_id.acc_number.split())
                        )
                    # if invoice.partner_bank_id.bank_bic:
                    #     DettaglioPagamento.BIC = (
                    #         invoice.partner_bank_id.bank_bic)
                DatiPagamento.DettaglioPagamento.append(DettaglioPagamento)
            body.DatiPagamento.append(DatiPagamento)
        return True

    def setAttachments(self, invoice, body):
        if invoice.fatturapa_doc_attachments:
            for doc_id in invoice.fatturapa_doc_attachments:
                AttachDoc = AllegatiType(
                    NomeAttachment=doc_id.datas_fname,
                    Attachment=base64.decodestring(doc_id.datas)
                )
                body.Allegati.append(AttachDoc)
        return True

    def setFatturaElettronicaHeader(self, company, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader = (
            FatturaElettronicaHeaderType())
        self.setDatiTrasmissione(company, partner, fatturapa)
        self.setCedentePrestatore(company, fatturapa)
        self.setRappresentanteFiscale(company, fatturapa)
        self.setCessionarioCommittente(partner, fatturapa)
        self.setTerzoIntermediarioOSoggettoEmittente(company, fatturapa)

    def setFatturaElettronicaBody(self, inv, FatturaElettronicaBody):

        self.setDatiGeneraliDocumento(inv, FatturaElettronicaBody)
        self.setDettaglioLinee(inv, FatturaElettronicaBody)
        self.setDatiDDT(inv, FatturaElettronicaBody)
        self.setDatiTrasporto(inv, FatturaElettronicaBody)
        self.setRelatedDocumentTypes(inv, FatturaElettronicaBody)
        self.setDatiRiepilogo(inv, FatturaElettronicaBody)
        self.setDatiPagamento(inv, FatturaElettronicaBody)
        self.setAttachments(inv, FatturaElettronicaBody)

    def getPartnerId(self, invoice_ids):

        invoice_model = self.env['account.invoice']
        partner = False

        invoices = invoice_model.browse(invoice_ids)

        for invoice in invoices:
            if not partner:
                partner = invoice.partner_id
            if invoice.partner_id != partner:
                raise UserError(
                    _('Invoices must belong to the same partner'))

        return partner

    def group_invoices_by_partner(self):
        invoice_ids = self.env.context.get('active_ids', False)
        res = {}
        for invoice in self.env['account.invoice'].browse(invoice_ids):
            if invoice.partner_id.id not in res:
                res[invoice.partner_id.id] = []
            res[invoice.partner_id.id].append(invoice.id)
        return res

    def exportFatturaPA(self):
        invoice_obj = self.env['account.invoice']
        invoices_by_partner = self.group_invoices_by_partner()
        attachments = self.env['fatturapa.attachment.out']
        for partner_id in invoices_by_partner:
            invoice_ids = invoices_by_partner[partner_id]
            partner = self.getPartnerId(invoice_ids)
            if partner.is_pa():
                fatturapa = FatturaElettronica(versione='FPA12')
            else:
                fatturapa = FatturaElettronica(versione='FPR12')

            company = self.env.user.company_id
            context_partner = self.env.context.copy()
            context_partner.update({'lang': partner.lang})
            try:
                self.with_context(context_partner).setFatturaElettronicaHeader(
                    company, partner, fatturapa)
                for invoice_id in invoice_ids:
                    inv = invoice_obj.with_context(context_partner).browse(
                        invoice_id)
                    # if inv.fatturapa_attachment_out_id:
                    #     raise UserError(
                    #         _("Invoice %s has E-invoice Export File yet") % (
                    #             inv.number))
                    if self.report_print_menu:
                        self.generate_attach_report(inv)
                    invoice_body = FatturaElettronicaBodyType()
                    inv.preventive_checks()
                    self.with_context(
                        context_partner
                    ).setFatturaElettronicaBody(
                        inv, invoice_body)
                    fatturapa.FatturaElettronicaBody.append(invoice_body)
                    # TODO DatiVeicoli
                    # commentare questa riga decommentare la riga dopo il nessun nuovo progressivo
                    number = self.setProgressivoAsFattura(inv, fatturapa)

                # nessun nuovo progressivo
                # number = self.setProgressivoInvio(fatturapa)
            except (SimpleFacetValueError, SimpleTypeValueError) as e:
                raise UserError(unicode(e))

            attach = self.saveAttachment(fatturapa, number)
            attachments |= attach

            for invoice_id in invoice_ids:
                inv = invoice_obj.browse(invoice_id)
                inv.write({'fatturapa_attachment_out_id': attach.id})

        action = {
            'view_type': 'form',
            'name': "Export Fattura Elettronica",
            'res_model': 'fatturapa.attachment.out',
            'type': 'ir.actions.act_window',
        }
        if len(attachments) == 1:
            action['view_mode'] = 'form'
            action['res_id'] = attachments[0].id
        else:
            action['view_mode'] = 'tree,form'
            action['domain'] = [('id', 'in', attachments.ids)]
        return action

    def generate_attach_report(self, inv):
        action_report_model, action_report_id = (
            self.report_print_menu.value.split(',')[0],
            int(self.report_print_menu.value.split(',')[1]))
        action_report = self.env[action_report_model] \
            .browse(action_report_id)
        report_model = self.env['report']
        attachment_model = self.env['ir.attachment']
        # Generate the PDF: if report_action.attachment is set
        # they will be automatically attached to the invoice,
        # otherwise use res to build a new attachment
        res = report_model.get_pdf(
            inv.ids, action_report.report_name)
        if action_report.attachment:
            # If the report is configured to be attached
            # to the current invoice, just get that from the attachments.
            # Note that in this case the attachment in
            # fatturapa_doc_attachments is exactly the same
            # that is attached to the invoice.
            attachment = report_model._attachment_stored(
                inv, action_report)[inv.id]
        else:
            # Otherwise, create a new attachment to be stored in
            # fatturapa_doc_attachments.
            filename = inv.number
            data_attach = {
                'name': filename,
                'datas': base64.b64encode(res),
                'datas_fname': filename,
                'type': 'binary'
            }
            attachment = attachment_model.create(data_attach)
        inv.write({
            'fatturapa_doc_attachments': [(0, 0, {
#                'is_pdf_invoice_print': True,
                'ir_attachment_id': attachment.id,
                'description': _("Attachment generated by "
                                 "Electronic invoice export")})]
        })

#    @api.model
#    def create(self, vals):
#        return super(WizardExportFatturapa, self).create(vals)
