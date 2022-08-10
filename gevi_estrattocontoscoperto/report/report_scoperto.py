
# -*- coding: utf-8 -*-

from datetime import datetime
import time
from openerp import api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ReportScoperto(models.AbstractModel):
    _name = 'report.gevi_estrattocontoscoperto.report_scoperto'
    _description = 'Estratto Conto Scoperto'

    @api.multi
    def render_html(self, data=None):
        amministratore = self.env['gevi_contatti.referente'].search([('id', '=', self.id)], limit=1)
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('gevi_estrattocontoscoperto.report_scoperto')
        # ordini = self.env['sale.order'].search(['&', '&', ('user_id', '=', pian.collaboratore_id.id), ('contratto_id', '!=', False), ('state', 'in', ['draft'])])
        # cli = []
        # for ordine in ordini:
        #     cli.append(ordine.partner_id.id)
        # clienti = self.env['res.partner'].search([('id', 'in', cli)])

        clienti = self.env['res.partner'].search([('id', 'in', amministratore.customer_ids.ids)])
        fatture = self.env['account.invoice'].search(['&', ('partner_id', 'in', clienti.ids), ('state', 'in', ['open'])])
        pagamenti = self.env['account.payment'].search(['&', '&', ('partner_id', 'in', clienti.ids), ('partner_type', '=', 'customer'), ('payment_type', '=', 'inbound')])

        # _logger.info('******************************** acconti: {0}'.format(acconti))
        # _logger.info('******************************** zone: {0}'.format(zone.ids))

        # _logger.info('******************************** clienti: {0}'.format(clienti.ids))

        tot_amm = 0
        clienti_ids_list = []

        for c in clienti:
            tot_doc = 0
            tot_scad = 0
            tot_pag = 0
            fatt_cliente = False
            for f in fatture:
                if f.commercial_partner_id.id == c.id:
                    if not fatt_cliente:
                        fatt_cliente = True
                    tot_doc = tot_doc+f.amount_total_company_signed
                    for p in pagamenti:
                        if p.id in f.payment_ids.ids:
                            tot_pag = tot_pag+p.amount
                    tot_scad = tot_scad+f.residual_company_signed
                    tot_amm = tot_amm+f.residual_company_signed
            if fatt_cliente:
                clienti_ids_list.append(c.id)
        clienti_filtered = self.env['res.partner'].search([('id', 'in', clienti_ids_list)])
        fatture_filtered = self.env['account.invoice'].search(['&', ('partner_id', 'in', clienti_filtered.ids), ('state', 'in', ['open'])])
        pagamenti_filtered = self.env['account.payment'].search(['&', '&', ('partner_id', 'in', clienti_filtered.ids), ('partner_type', '=', 'customer'), ('payment_type', '=', 'inbound')])

        oggi = datetime.now().strftime('%d/%m/%Y')

        docargs = {
            'doc_ids': self.ids,
            'doc_model': 'gevi_contatti.referente',
            'docs': amministratore,
            'fatture': fatture_filtered,
            'pagamenti': pagamenti_filtered,
            'clienti': clienti_filtered,
            'DataStampa': fields.date.today(),
            'oggi': oggi,
            'tot_amministratore': tot_amm
        }
        return report_obj.render('gevi_estrattocontoscoperto.report_scoperto', values=docargs)


