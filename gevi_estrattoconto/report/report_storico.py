# -*- coding: utf-8 -*-

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ReportStorico(models.AbstractModel):
    _name = 'report.gevi_estrattoconto.report_storico'
    _description = 'Estratto Conto Storico'

    def render_html(self, data=None):
        amministratore = self.env['gevi_contatti.referente'].search([('id', '=', self.id)], limit=1)
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('gevi_estrattoconto.report_storico')
        # ordini = self.env['sale.order'].search(['&', '&', ('user_id', '=', pian.collaboratore_id.id), ('contratto_id', '!=', False), ('state', 'in', ['draft'])])
        # cli = []
        # for ordine in ordini:
        #     cli.append(ordine.partner_id.id)
        # clienti = self.env['res.partner'].search([('id', 'in', cli)])
        clienti = self.env['res.partner'].search([('id', 'in', amministratore.customer_ids.ids)])
        fatture = self.env['account.invoice'].search([('partner_id', 'in', clienti.ids)])
        pagamenti = self.env['account.payment'].search(
            ['&', '&', ('partner_id', 'in', clienti.ids), ('partner_type', '=', 'customer'),
             ('payment_type', '=', 'inbound')])

        # _logger.info('******************************** acconti: {0}'.format(acconti))
        # _logger.info('******************************** zone: {0}'.format(zone.ids))

        docargs = {
            'doc_ids': self.ids,
            'doc_model': 'gevi_contatti.referente',
            'docs': amministratore,
            'fatture': fatture,
            'pagamenti': pagamenti,
            'clienti': clienti,
            'DataStampa': fields.date.today(),
        }
        return report_obj.render('gevi_estrattoconto.report_storico', values=docargs)
