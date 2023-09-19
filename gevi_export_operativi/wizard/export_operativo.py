# -*- coding: utf-8 -*-
# from calender import monthrange
import base64
import logging
from datetime import datetime
# from xlsxwriter.workbook import Workbook
from io import BytesIO

import xlwt

from odoo import fields, models, exceptions

_logger = logging.getLogger(__name__)


class ExportOperativo(models.TransientModel):
    _name = "gevi_export_operativi.export_operativo"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Export Operativo"

    verbale_data_da = fields.Date(string='Data Verbale inizio', default=fields.Date.today)
    verbale_data_a = fields.Date(string='Data Verbale fine', default=fields.Date.today)

    esecuzione_data_da = fields.Date(
        string=u'Data Esecuzione inizio',
        default=fields.Date.context_today,
    )
    esecuzione_data_a = fields.Date(
        string=u'Data Esecuzione fine',
        default=fields.Date.context_today,
    )

    conferma_data_da = fields.Date(
        string=u'Data Conferma inizio',
        default=fields.Date.context_today,
    )
    conferma_data_a = fields.Date(
        string=u'Data Conferma fine',
        default=fields.Date.context_today,
    )

    zona_impianto_id = fields.Many2one(
        string=u'Zona Impianto',
        comodel_name='gevi_zone.zona_impianto'
    )

    manutentore_ids = fields.Many2many(
        string=u'Manutentori',
        comodel_name='gevi_contatti.manutentore',
        readonly=False,
        relation='manutentori_ids_export_operativo_ids_rel',
    )

    template_export_isp = fields.Selection(
        string=u'Template Esportazione',
        selection=[('template1', 'Template 1')],
        default='template1',
    )

    programmazione_data_da = fields.Date(
        string=u'Data Programmazione inizio',
        default=fields.Date.context_today,
    )
    programmazione_data_a = fields.Date(
        string=u'Data Programmazione fine',
        default=fields.Date.context_today,
    )

    zona_impianto_ids = fields.Many2many(
        string=u'Zone Impianto',
        comodel_name='gevi_zone.zona_impianto',
        readonly=False,
        relation='zone_impianto_ids_export_operativo_ids_rel',
    )

    # @api.onchange("zona_impianto_id")
    # def _onchange_zona_impianto_id(self):
    #     vals = {}

    #     # # Remove warning if necessary
    #     # vals['warning'] = {
    #     #     'title': _('Titolo'),
    #     #     'message': _('Messaggio'),
    #     # }

    #     # Remove domain if necessary
    #     lista_manutentori = []
    #     insieme_manutentori = set()
    #     verbale_man_ids = self.env['gevi_verbali.verbale'].search([
    #         '&',
    #         ('ispettore_id.user_id.id', '=', self.env.uid),
    #         ('state', '=', 'assegnato')
    #         ])
    #     for v in verbale_man_ids:
    #         if v.manutentore_id.id not in insieme_manutentori:
    #             insieme_manutentori.add(v.manutentore_id.id)
    #             lista_manutentori.append(v.manutentore_id.id)

    #     vals['domain'] = {
    #         "manutentore_ids": [("id", "in", lista_manutentori)],
    #     }
    #     vals['readonly'] = {
    #         'manutentore_ids': False
    #     }
    #     return vals

    def action_export_manutentori(self):
        for line in self:
            if not line.programmazione_data_da or not line.programmazione_data_a:
                raise exceptions.ValidationError('ATTENZIONE: Le date devono essere valorizzate!')

            # Preparo le intestazioni per il foglio excel
            filename = 'ProssimeVerifiche_{0}_{1}.xls'.format(
                line.programmazione_data_da, line.programmazione_data_a)
            workbook = xlwt.Workbook(encoding="UTF-8")
            ws_name = "ProssimeVerifiche".format(line.programmazione_data_a, line.programmazione_data_a)
            worksheet = workbook.add_sheet("Elenco Prossime Verifiche")
            # style = xlwt.easyxf('font:height 400, bold True, name Arial; align: horiz center, vert center;borders: top medium,right medium,bottom medium,left medium')
            style_date = xlwt.easyxf(num_format_str='DD-MM-YYYY')
            style_title = xlwt.easyxf('font:bold True')
            common_style = xlwt.easyxf('font:bold False')
            warning_style = xlwt.easyxf('pattern: pattern solid, fore_colour light_yellow;')
            style = common_style
            # Preparo la query per la preparazione dei dati
            # colonna0 = Manutentore
            # colonna1 = Zona Impianto
            # colonna2 = Tipo Impianto
            # colonna3 = Tipo Verifica
            # colonna4 = Amministratore
            # colonna5 = Cliente
            # colonna6 = Ubicazione Impianto
            # colonna7 = Localita
            # colonna8 = Prov
            # colonna9 = Data Programmazione
            # colonna10 = Data Prossima Verifica
            # colonna11 = Data Ultima Verifica
            # colonna12 = Nr Programmazione
            # colonna13 = Matricola
            # colonna14 = Verificatore
            # colonna15 = Stato
            request = ("SELECT CONCAT(gcm.name, ' ', gcm.provincia), " + \
                       "gzzi.name, " + \
                       "CASE WHEN giic.name LIKE 'Asc%' THEN 'Ascensore' WHEN giic.name LIKE 'Pia%' THEN 'Piattaforma Elevatrice' WHEN giic.name LIKE 'Montac%' THEN 'Montacarichi' WHEN giic.name LIKE 'Montas%' THEN 'Montascale' END, " + \
                       "CASE WHEN gvv.periodica is True THEN 'Periodica' WHEN gvv.periodica is False THEN 'Straordinaria' END, " + \
                       "CONCAT(gcr.name, ' ', gcr.indirizzo, ' - ', gcr.cap, ' ', gcr.citta, ' ', gcr.provincia), " + \
                       "CASE WHEN gii.proprietario_diverso is True THEN rppd.name ELSE rpcf.name END, " + \
                       "gii.indirizzo, " + \
                       "gii.citta, " + \
                       "gii.provincia, " + \
                       "gvv.data_programmazione, " + \
                       "gvv.data_prossima_verifica, " + \
                       "gvv.data_ultima_verifica, " + \
                       "gvv.name, " + \
                       "CASE WHEN giird.name = 'Matricola' THEN giird.valore_attributo ELSE '-' END, " + \
                       "hre.name_related, " + \
                       "gvv.state " + \
                       "FROM gevi_verbali_verbale gvv " + \
                       "LEFT JOIN gevi_impianti_impianto gii ON gvv.impianto_id = gii.id " + \
                       "LEFT JOIN gevi_impianti_impianto_categoria giic ON gvv.impianto_categoria_id = giic.id " + \
                       "LEFT JOIN gevi_impianti_impianto_riga_descrizione giird ON giird.impianto_id = gvv.impianto_id " + \
                       "LEFT JOIN hr_employee hre ON gvv.ispettore_id = hre.id " + \
                       "LEFT JOIN res_partner rpcf ON rpcf.id = gvv.customer_id " + \
                       "LEFT JOIN res_partner rppd ON rppd.id = gii.proprietario_id " + \
                       "LEFT JOIN gevi_contatti_referente gcr ON gcr.id = rpcf.referente_id " + \
                       "LEFT JOIN gevi_contatti_manutentore gcm ON gcm.id = gvv.manutentore_id " + \
                       "LEFT JOIN gevi_zone_zona_impianto gzzi ON gii.zona_impianto_id = gzzi.id " + \
                       "WHERE data_programmazione >= '{0}' " + \
                       "AND data_programmazione <= '{1}' " + \
                       "AND giird.name = 'Matricola' " + \
                       "AND gvv.state in ('bozza','assegnato') ").format(line.programmazione_data_da,
                                                                         line.programmazione_data_a)
            if line.zona_impianto_ids:
                request = request + ("AND gzzi.id in {0} ").format(
                    str(tuple(line.zona_impianto_ids.ids)).replace(',)', ')'))
            request = request + ("ORDER BY gzzi.name, gii.citta, gii.indirizzo")
            # _logger.info('******************************** QueryMinistero: {0}'.format(request))
            title = worksheet.row(0)
            title.write(0, 'Manutentore', style_title)
            title.write(1, 'Zona Impianto', style_title)
            title.write(2, 'Tipo Impianto', style_title)
            title.write(3, 'Tipo Verifica', style_title)
            title.write(4, 'Amministratore', style_title)
            title.write(5, 'Cliente', style_title)
            title.write(6, 'Ubicazione Impianto', style_title)
            title.write(7, 'Localita', style_title)
            title.write(8, 'Prov', style_title)
            title.write(9, 'Data Programmazione', style_title)
            title.write(10, 'Data Prossima Verifica', style_title)
            title.write(11, 'Data Ultima Verifica', style_title)
            title.write(12, 'Nr Programmazione', style_title)
            title.write(13, 'Matricola', style_title)
            title.write(14, 'Verificatore', style_title)
            title.write(15, 'Stato', style_title)

            xls_row_index = 1
            self.env.cr.execute(request)
            for sql_row in self.env.cr.fetchall():
                worksheet.write(xls_row_index, 0, sql_row[0], style)
                worksheet.write(xls_row_index, 1, sql_row[1], style)
                worksheet.write(xls_row_index, 2, sql_row[2], style)
                worksheet.write(xls_row_index, 3, sql_row[3], style)
                worksheet.write(xls_row_index, 4, sql_row[4], style)
                worksheet.write(xls_row_index, 5, sql_row[5], style)
                worksheet.write(xls_row_index, 6, sql_row[6], style)
                worksheet.write(xls_row_index, 7, sql_row[7], style)
                worksheet.write(xls_row_index, 8, sql_row[8], style)
                worksheet.write(xls_row_index, 9,
                                (datetime.strptime(sql_row[9], '%Y-%m-%d')).strftime('%d/%m/%Y') if sql_row[9] else "",
                                style)
                worksheet.write(xls_row_index, 10,
                                (datetime.strptime(sql_row[10], '%Y-%m-%d')).strftime('%d/%m/%Y') if sql_row[
                                    10] else "", style)
                worksheet.write(xls_row_index, 11,
                                (datetime.strptime(sql_row[11], '%Y-%m-%d')).strftime('%d/%m/%Y') if sql_row[
                                    11] else "", style)
                worksheet.write(xls_row_index, 12, sql_row[12], style)
                worksheet.write(xls_row_index, 13, sql_row[13], style)
                worksheet.write(xls_row_index, 14, sql_row[14], style)
                worksheet.write(xls_row_index, 15, sql_row[15], style)
                xls_row_index += 1
                style = common_style

            filestream = BytesIO()
            workbook.save(filestream)
            export_id = self.env['gevi_export_operativi.elenco_esportazioni'].create({
                'name': ws_name,
                'excel_file': base64.encodestring(filestream.getvalue()),
                'file_name': filename,
                'tipo': 'Manutentori'})
            filestream.close()

            return {
                'view_id': self.env.ref('gevi_export_operativi.view_elenco_esportazioni_form').id,
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'gevi_export_operativi.elenco_esportazioni',
                'target': 'new',
                'res_id': export_id.id,
                'type': 'ir.actions.act_window',
            }

    def action_export_ispettore(self):
        for line in self:
            if not line.manutentore_ids or not line.zona_impianto_id:
                raise exceptions.ValidationError('ATTENZIONE: Tutti i campi devono essere valorizzati!')
            if line.template_export_isp == 'template1':
                line.export_assegnati_ispettore_v1()

    def export_assegnati_ispettore_v1(self):
        for line in self:
            # Preparo le intestazioni per il foglio excel
            oggi = datetime.now().strftime("%Y-%m-%d")
            filename = 'Verifiche_{0}_{1}.xls'.format(line.zona_impianto_id.name, oggi)
            workbook = xlwt.Workbook(encoding="UTF-8")
            ws_name = "Verifiche_{0}_{1}.xls".format(line.zona_impianto_id.name, oggi)
            worksheet = workbook.add_sheet("Verifiche {0}".format(line.zona_impianto_id.name))
            # style = xlwt.easyxf('font:height 400, bold True, name Arial; align: horiz center, vert center;borders: top medium,right medium,bottom medium,left medium')
            style_date = xlwt.easyxf(num_format_str='DD-MM-YYYY')
            style_title = xlwt.easyxf('font:bold True')
            common_style = xlwt.easyxf('font:bold False')
            warning_style = xlwt.easyxf('pattern: pattern solid, fore_colour light_yellow;')
            error_style = xlwt.easyxf('pattern: pattern solid, fore_colour tan;')
            style = common_style
            # Preparo la query per la preparazione dei dati
            # title.write(0, 'Codice Programmazione', style_title)
            # title.write(1, 'Cliente Fatturazione', style_title)
            # title.write(2, 'Codice Impianto', style_title)
            # title.write(3, 'Etichetta Impianto', style_title)
            # title.write(4, 'Indirizzo Impianto', style_title)
            # title.write(5, 'Citta Impianto', style_title)
            # title.write(6, 'Matricola', style_title)
            # title.write(7, 'N. Impianto', style_title)
            # title.write(8, 'N. Impianto', style_title)
            # title.write(9, 'Data Prossima Verifica', style_title)
            # title.write(10, 'Data Ultima Verifica', style_title)
            # title.write(11, 'Zona Impianto', style_title)
            # title.write(12, 'Amministratore', style_title)
            # title.write(13, 'Altro', style_title) utilizzato per blocco amministrativo etc

            title = worksheet.row(0)
            title.write(0, 'Codice Programmazione', style_title)
            title.write(1, 'Cliente Fatturazione', style_title)
            title.write(2, 'Codice Impianto', style_title)
            title.write(3, 'Etichetta Impianto', style_title)
            title.write(4, 'Indirizzo Impianto', style_title)
            title.write(5, 'Citta Impianto', style_title)
            title.write(6, 'Matricola', style_title)
            title.write(7, 'N. Impianto', style_title)
            title.write(8, 'Marca', style_title)
            title.write(9, 'Data Prossima Verifica', style_title)
            title.write(10, 'Data Ultima Verifica', style_title)
            title.write(11, 'Zona Impianto', style_title)
            title.write(12, 'Amministratore', style_title)
            title.write(13, 'Periodica', style_title)
            title.write(14, 'Altro', style_title)

            xls_row_index = 1
            verbale_ids = self.env['gevi_verbali.verbale'].search([
                '&', '&',
                ('manutentore_id', 'in', line.manutentore_ids.ids),
                ('impianto_id.zona_impianto_id', '=', line.zona_impianto_id.id),
                ('state', '=', 'assegnato')
            ], order="impianto_citta, impianto_indirizzo, customer_id")

            for verbale in verbale_ids:
                impianto_riga_desc_obj = self.env['gevi.impianti.impianto_riga_descrizione']
                matricola_obj = impianto_riga_desc_obj.search(
                    ['&', ('impianto_id', '=', verbale.impianto_id.id), ('name', '=', "Matricola")], limit=1)
                n_impianto_obj = impianto_riga_desc_obj.search(
                    ['&', ('impianto_id', '=', verbale.impianto_id.id), ('name', '=', "N. Impianto")], limit=1)
                marca_obj = impianto_riga_desc_obj.search(
                    ['&', ('impianto_id', '=', verbale.impianto_id.id), ('name', '=', "Marca")], limit=1)

                altro = ""
                if verbale.contratto_id.blocco_amministrativo:
                    altro = altro + "{0}: {1} ".format("Blocco Ammm.",
                                                       verbale.contratto_id.causale_blocco if verbale.contratto_id.causale_blocco else "")
                    style = warning_style

                # worksheet.write(riga, colonna, valore, stilexf)
                # _logger.info('******************************** verbale.id ID#{0}'.format(verbale.id))
                # _logger.info('******************************** verbale.manutentore_id.name_get()[0][1]:ID#{1} {0}'.format(verbale.manutentore_id.name_get()[0][1],verbale.id))
                # _logger.info('******************************** verbale.impianto_id.name_get()[0][1]:ID#{1} {0}'.format(verbale.impianto_id.name_get()[0][1],verbale.id))

                worksheet.write(xls_row_index, 0, verbale.codice_verifica, style)
                worksheet.write(xls_row_index, 1, verbale.customer_id.name, style)
                worksheet.write(xls_row_index, 2, verbale.impianto_id.codice_impianto, style)
                worksheet.write(xls_row_index, 3, verbale.impianto_id.etichetta, style)
                worksheet.write(xls_row_index, 4,
                                verbale.impianto_id.indirizzo if verbale.impianto_id.indirizzo else "", style)
                worksheet.write(xls_row_index, 5, verbale.impianto_id.citta if verbale.impianto_id.citta else "", style)
                worksheet.write(xls_row_index, 6,
                                matricola_obj.valore_attributo if matricola_obj.valore_attributo else "", style)
                worksheet.write(xls_row_index, 7,
                                n_impianto_obj.valore_attributo if n_impianto_obj.valore_attributo else "", style)
                worksheet.write(xls_row_index, 8, marca_obj.valore_attributo if marca_obj.valore_attributo else "",
                                style)
                worksheet.write(xls_row_index, 9, (datetime.strptime(verbale.data_programmazione, '%Y-%m-%d')).strftime(
                    '%d/%m/%Y') if verbale.data_programmazione else "", style)
                worksheet.write(xls_row_index, 10,
                                (datetime.strptime(verbale.impianto_id.data_ultima_verifica, '%Y-%m-%d')).strftime(
                                    '%d/%m/%Y') if verbale.impianto_id.data_ultima_verifica else "", style)
                worksheet.write(xls_row_index, 11,
                                verbale.impianto_id.zona_impianto_id.name if verbale.impianto_id.zona_impianto_id else "",
                                style)
                worksheet.write(xls_row_index, 12, verbale.referente_id.name if verbale.referente_id else "", style)
                worksheet.write(xls_row_index, 13, "Periodica" if verbale.periodica else "Straordinaria", style)
                worksheet.write(xls_row_index, 14, altro, style)

                xls_row_index += 1
                style = common_style

            filestream = BytesIO()
            workbook.save(filestream)
            export_id = self.env['gevi_export_operativi.elenco_esportazioni'].create({
                'name': ws_name,
                'excel_file': base64.encodestring(filestream.getvalue()),
                'file_name': filename,
                'tipo': 'Programmazione'})
            filestream.close()

            return {
                'view_id': self.env.ref('gevi_export_operativi.view_elenco_esportazioni_form').id,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'gevi_export_operativi.elenco_esportazioni',
                'target': 'new',
                'res_id': export_id.id,
                'type': 'ir.actions.act_window',
            }

    def action_export_confermati(self):
        for line in self:
            if not line.conferma_data_da or not line.conferma_data_a:
                raise exceptions.ValidationError('ATTENZIONE: Le date devono essere valorizzate!')

            # Preparo le intestazioni per il foglio excel
            filename = 'VerificheConfermate_{0}_{1}.xls'.format(line.conferma_data_da, line.conferma_data_a)
            workbook = xlwt.Workbook(encoding="UTF-8")
            ws_name = "Verifiche Confermate dal {0} al {1}".format(line.conferma_data_da, line.conferma_data_a)
            worksheet = workbook.add_sheet("Verifiche Confermate")
            # style = xlwt.easyxf('font:height 400, bold True, name Arial; align: horiz center, vert center;borders: top medium,right medium,bottom medium,left medium')
            style_date = xlwt.easyxf(num_format_str='DD-MM-YYYY')
            style_title = xlwt.easyxf('font:bold True')
            common_style = xlwt.easyxf('font:bold False')
            warning_style = xlwt.easyxf('pattern: pattern solid, fore_colour light_yellow;')
            style = common_style
            # Preparo la query per la preparazione dei dati
            # colonna0 = Ispettore
            # colonna1 = Codice Programmazione
            # colonna2 = Data Esecuzione
            # colonna3 = Data Programmazione
            # colonna4 = Data Assegnazione
            # colonna5 = Data Conferma
            # colonna6 = Nr Verbale
            # colonna7 = Data Verbale
            # colonna8 = Manutentore
            # colonna9 = Impianto
            # colonna10 = Zona Impianto
            # colonna11 = Amministratore
            title = worksheet.row(0)
            title.write(0, 'Ispettore', style_title)
            title.write(1, 'Codice Programmazione', style_title)
            title.write(2, 'Data Esecuzione', style_title)
            title.write(3, 'Data Programmazione', style_title)
            title.write(4, 'Data Assegnazione', style_title)
            title.write(5, 'Data Conferma', style_title)
            title.write(6, 'Nr Verbale', style_title)
            title.write(7, 'Data Verbale', style_title)
            title.write(8, 'Manutentore', style_title)
            title.write(9, 'Impianto', style_title)
            title.write(10, 'Zona Impianto', style_title)
            title.write(11, 'Amministratore', style_title)

            xls_row_index = 1
            verbale_ids = self.env['gevi_verbali.verbale'].search([
                '&', '&',
                ('data_conferma', '>=', line.conferma_data_da),
                ('data_conferma', '<=', line.conferma_data_a),
                ('state', '=', 'confermato')
            ], order="ispettore_id, data_conferma, codice_verifica")

            for verbale in verbale_ids:
                # worksheet.write(riga, colonna, valore, stilexf)
                # _logger.info('******************************** verbale.id ID#{0}'.format(verbale.id))
                # _logger.info('******************************** verbale.manutentore_id.name_get()[0][1]:ID#{1} {0}'.format(verbale.manutentore_id.name_get()[0][1],verbale.id))
                # _logger.info('******************************** verbale.impianto_id.name_get()[0][1]:ID#{1} {0}'.format(verbale.impianto_id.name_get()[0][1],verbale.id))

                worksheet.write(xls_row_index, 0, verbale.ispettore_id.name, style)
                worksheet.write(xls_row_index, 1, verbale.codice_verifica, style)
                worksheet.write(xls_row_index, 2,
                                (datetime.strptime(verbale.data_esecuzione, '%Y-%m-%d')).strftime('%d/%m/%Y'),
                                style_date)
                worksheet.write(xls_row_index, 3, (datetime.strptime(verbale.data_programmazione, '%Y-%m-%d')).strftime(
                    '%d/%m/%Y') if verbale.data_programmazione else "", style_date)
                worksheet.write(xls_row_index, 4,
                                (datetime.strptime(verbale.data_assegnazione, '%Y-%m-%d')).strftime('%d/%m/%Y'),
                                style_date)
                worksheet.write(xls_row_index, 5,
                                (datetime.strptime(verbale.data_conferma, '%Y-%m-%d')).strftime('%d/%m/%Y'), style_date)
                worksheet.write(xls_row_index, 6, verbale.name, style)
                worksheet.write(xls_row_index, 7, (datetime.strptime(verbale.data_verbale, '%Y-%m-%d')).strftime(
                    '%d/%m/%Y') if verbale.data_verbale else "", style_date)
                worksheet.write(xls_row_index, 8,
                                verbale.manutentore_id.name_get()[0][1] if verbale.manutentore_id else "", style)
                worksheet.write(xls_row_index, 9, verbale.impianto_id.name_get()[0][1], style)
                worksheet.write(xls_row_index, 10,
                                verbale.impianto_id.zona_impianto_id.name if verbale.impianto_id.zona_impianto_id else "",
                                style)
                worksheet.write(xls_row_index, 11, verbale.referente_id.name if verbale.referente_id else "", style)
                xls_row_index += 1
                style = common_style

            filestream = BytesIO()
            workbook.save(filestream)
            export_id = self.env['gevi_export_operativi.elenco_esportazioni'].create({
                'name': ws_name,
                'excel_file': base64.encodestring(filestream.getvalue()),
                'file_name': filename,
                'tipo': 'Monitoraggio'})
            filestream.close()

            return {
                'view_id': self.env.ref('gevi_export_operativi.view_elenco_esportazioni_form').id,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'gevi_export_operativi.elenco_esportazioni',
                'target': 'new',
                'res_id': export_id.id,
                'type': 'ir.actions.act_window',
            }

    def action_export_eseguiti(self):
        for line in self:
            if not line.esecuzione_data_da or not line.esecuzione_data_a:
                raise exceptions.ValidationError('ATTENZIONE: Le date devono essere valorizzate!')

            # Preparo le intestazioni per il foglio excel
            filename = 'VerificheEseguite_{0}_{1}.xls'.format(line.esecuzione_data_da, line.esecuzione_data_a)
            workbook = xlwt.Workbook(encoding="UTF-8")
            ws_name = "Verifiche Eseguite dal {0} al {1}".format(line.esecuzione_data_da, line.esecuzione_data_a)
            worksheet = workbook.add_sheet("Verifiche Eseguite")
            # style = xlwt.easyxf('font:height 400, bold True, name Arial; align: horiz center, vert center;borders: top medium,right medium,bottom medium,left medium')
            style_date = xlwt.easyxf(num_format_str='DD-MM-YYYY')
            style_title = xlwt.easyxf('font:bold True')
            common_style = xlwt.easyxf('font:bold False')
            warning_style = xlwt.easyxf('pattern: pattern solid, fore_colour light_yellow;')
            style = common_style
            # Preparo la query per la preparazione dei dati
            # colonna0 = Codice Programmazione
            # colonna1 = Data Esecuzione
            # colonna2 = Data Programmazione
            # colonna3 = Data Assegnazione
            # colonna4 = Manutentore
            # colonna5 = Impianto
            # colonna6 = Amministratore
            # zona impianto
            title = worksheet.row(0)
            title.write(0, 'Ispettore', style_title)
            title.write(1, 'Codice Programmazione', style_title)
            title.write(2, 'Data Esecuzione', style_title)
            title.write(3, 'Data Programmazione', style_title)
            title.write(4, 'Data Assegnazione', style_title)
            title.write(5, 'Manutentore', style_title)
            title.write(6, 'Impianto', style_title)
            title.write(7, 'Zona Impianto', style_title)
            title.write(8, 'Amministratore', style_title)

            xls_row_index = 1
            verbale_ids = self.env['gevi_verbali.verbale'].search([
                '&', '&',
                ('data_esecuzione', '>=', line.esecuzione_data_da),
                ('data_esecuzione', '<=', line.esecuzione_data_a),
                ('state', '=', 'eseguito')
            ], order="ispettore_id, data_esecuzione, codice_verifica")

            for verbale in verbale_ids:
                # worksheet.write(riga, colonna, valore, stilexf)
                # _logger.info('******************************** verbale.id ID#{0}'.format(verbale.id))
                # _logger.info('******************************** verbale.manutentore_id.name_get()[0][1]:ID#{1} {0}'.format(verbale.manutentore_id.name_get()[0][1],verbale.id))
                # _logger.info('******************************** verbale.impianto_id.name_get()[0][1]:ID#{1} {0}'.format(verbale.impianto_id.name_get()[0][1],verbale.id))
                worksheet.write(xls_row_index, 0, verbale.ispettore_id.name, style)
                worksheet.write(xls_row_index, 1, verbale.codice_verifica, style)
                worksheet.write(xls_row_index, 2,
                                (datetime.strptime(verbale.data_esecuzione, '%Y-%m-%d')).strftime('%d/%m/%Y'),
                                style_date)
                worksheet.write(xls_row_index, 3, (datetime.strptime(verbale.data_programmazione, '%Y-%m-%d')).strftime(
                    '%d/%m/%Y') if verbale.data_programmazione else "", style_date)
                worksheet.write(xls_row_index, 4,
                                (datetime.strptime(verbale.data_assegnazione, '%Y-%m-%d')).strftime('%d/%m/%Y'),
                                style_date)
                worksheet.write(xls_row_index, 5,
                                verbale.manutentore_id.name_get()[0][1] if verbale.manutentore_id else "", style)
                worksheet.write(xls_row_index, 6, verbale.impianto_id.name_get()[0][1], style)
                worksheet.write(xls_row_index, 7,
                                verbale.impianto_id.zona_impianto_id.name if verbale.impianto_id.zona_impianto_id else "",
                                style)
                worksheet.write(xls_row_index, 8, verbale.referente_id.name if verbale.referente_id else "", style)
                xls_row_index += 1
                style = common_style

            filestream = BytesIO()
            workbook.save(filestream)
            export_id = self.env['gevi_export_operativi.elenco_esportazioni'].create({
                'name': ws_name,
                'excel_file': base64.encodestring(filestream.getvalue()),
                'file_name': filename,
                'tipo': 'Monitoraggio'})
            filestream.close()

            return {
                'view_id': self.env.ref('gevi_export_operativi.view_elenco_esportazioni_form').id,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'gevi_export_operativi.elenco_esportazioni',
                'target': 'new',
                'res_id': export_id.id,
                'type': 'ir.actions.act_window',
            }

    def action_export_ministero(self):
        for line in self:
            if not line.verbale_data_da or not line.verbale_data_a:
                raise exceptions.ValidationError('ATTENZIONE: Le date devono essere valorizzate!')

            # Preparo le intestazioni per il foglio excel
            filename = 'Ministero_{0}_{1}.xls'.format(line.verbale_data_da, line.verbale_data_a)
            workbook = xlwt.Workbook(encoding="UTF-8")
            ws_name = "Elenco Certificati dal {0} al {1}".format(line.verbale_data_da, line.verbale_data_a)
            worksheet = workbook.add_sheet("Elenco Verbali")
            # style = xlwt.easyxf('font:height 400, bold True, name Arial; align: horiz center, vert center;borders: top medium,right medium,bottom medium,left medium')
            style_date = xlwt.easyxf(num_format_str='DD-MM-YYYY')
            style_title = xlwt.easyxf('font:bold True')
            common_style = xlwt.easyxf('font:bold False')
            warning_style = xlwt.easyxf('pattern: pattern solid, fore_colour light_yellow;')
            style = common_style
            # Preparo la query per la preparazione dei dati
            # colonna0 = Tipo Impianto
            # colonna1 = Tipo Verbale
            # colonna2 = Cliente
            # colonna3 = Ubicazione Impianto
            # colonna4 = Localita
            # colonna5 = Prov
            # colonna6 = Data Certificato
            # colonna7 = Nr Verbale
            # colonna8 = Matricola
            # colonna9 = Esito
            # colonna10 = Verificatore
            # colonna11 = Codice Fiscale Verificatore
            # colonna12 = Stato
            request = (
                        "SELECT CASE WHEN giic.name LIKE 'Asc%' THEN 'Ascensore' WHEN giic.name LIKE 'Pia%' THEN 'Piattaforma Elevatrice' WHEN giic.name LIKE 'Montac%' THEN 'Montacarichi' WHEN giic.name LIKE 'Montas%' THEN 'Montascale' WHEN giic.name LIKE 'Mess%' THEN 'Messa a Terra' WHEN giic.name LIKE 'Scar%' THEN 'Scariche Atmosferiche' END AS TipoImpianto, CASE WHEN gvv.periodica is True THEN 'Periodica' WHEN gvv.periodica is False THEN 'Straordinaria' END AS TipoVerbale, CASE WHEN gii.proprietario_diverso is True THEN rppd.name ELSE rpcf.name END AS Cliente, gii.indirizzo AS UbicazioneImpianto, gii.citta AS Localita, gii.provincia AS Prov, gvv.data_verbale AS DataCertificato, gvv.name AS NrVerbale, CASE WHEN giird.name = 'Matricola' THEN giird.valore_attributo WHEN giird.name = 'Potenza' THEN giird.valore_attributo WHEN giird.name = 'Tipo di captatore%' THEN giird.valore_attributo ELSE '-' END AS Matricola, gvv.esito_verifica AS Esito, hre.name_related AS Verificatore, hre.identification_id AS CodiceFiscaleVerificatore, gvv.state AS Stato " + \
                        "FROM gevi_verbali_verbale gvv " + \
                        "LEFT JOIN gevi_impianti_impianto gii ON gvv.impianto_id = gii.id " + \
                        "LEFT JOIN gevi_impianti_impianto_categoria giic ON gvv.impianto_categoria_id = giic.id " + \
                        "LEFT JOIN gevi_impianti_impianto_riga_descrizione giird ON giird.impianto_id = gvv.impianto_id " + \
                        "LEFT JOIN hr_employee hre ON gvv.ispettore_id = hre.id " + \
                        "LEFT JOIN res_partner rpcf ON rpcf.id = gvv.customer_id " + \
                        "LEFT JOIN res_partner rppd ON rppd.id = gii.proprietario_id " + \
                        "WHERE data_verbale >= '{0}' " + \
                        "AND data_verbale <= '{1}' " + \
                        "AND (giird.name = 'Matricola' OR giird.name like 'Potenza%' OR giird.name like 'Tipo di captatore%') " + \
                        "ORDER BY gvv.name").format(line.verbale_data_da, line.verbale_data_a)
            # _logger.info('******************************** QueryMinistero: {0}'.format(request))
            title = worksheet.row(0)
            title.write(0, 'Tipo Impianto', style_title)
            title.write(1, 'Tipo Verbale', style_title)
            title.write(2, 'Cliente', style_title)
            title.write(3, 'Ubicazione Impianto', style_title)
            title.write(4, 'Localita', style_title)
            title.write(5, 'Prov', style_title)
            title.write(6, 'Data Certificato', style_title)
            title.write(7, 'Nr Verbale', style_title)
            title.write(8, 'Matricola', style_title)
            title.write(9, 'Esito', style_title)
            title.write(10, 'Verificatore', style_title)
            title.write(11, 'Codice Fiscale Verificatore', style_title)
            title.write(12, 'Stato', style_title)

            xls_row_index = 1
            self.env.cr.execute(request)
            for sql_row in self.env.cr.fetchall():
                if sql_row[12] != 'validato':
                    style = warning_style
                if sql_row[9] == 'da_selezionare':
                    style = warning_style
                worksheet.write(xls_row_index, 0, sql_row[0], style)
                worksheet.write(xls_row_index, 1, sql_row[1], style)
                worksheet.write(xls_row_index, 2, sql_row[2], style)
                worksheet.write(xls_row_index, 3, sql_row[3], style)
                worksheet.write(xls_row_index, 4, sql_row[4], style)
                worksheet.write(xls_row_index, 5, sql_row[5], style)
                worksheet.write(xls_row_index, 6, (datetime.strptime(sql_row[6], '%Y-%m-%d')).strftime('%d/%m/%Y'),
                                style)
                worksheet.write(xls_row_index, 7, sql_row[7], style)
                worksheet.write(xls_row_index, 8, sql_row[8], style)
                worksheet.write(xls_row_index, 9, sql_row[9], style)
                worksheet.write(xls_row_index, 10, sql_row[10], style)
                worksheet.write(xls_row_index, 11, sql_row[11], style)
                worksheet.write(xls_row_index, 12, sql_row[12], style)
                xls_row_index += 1
                style = common_style

            filestream = BytesIO()
            workbook.save(filestream)
            export_id = self.env['gevi_export_operativi.elenco_esportazioni'].create({
                'name': ws_name,
                'excel_file': base64.encodestring(filestream.getvalue()),
                'file_name': filename,
                'tipo': 'Ministero'})
            filestream.close()

            return {
                'view_id': self.env.ref('gevi_export_operativi.view_elenco_esportazioni_form').id,
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'gevi_export_operativi.elenco_esportazioni',
                'target': 'new',
                'res_id': export_id.id,
                'type': 'ir.actions.act_window',
            }
