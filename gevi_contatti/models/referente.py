# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class Referente(models.Model):
    _name = 'gevi_contatti.referente'
    _description = "Amministratore"

    # richiesto per openchatter
    _inherit = ["mail.thread", "mail.activity.mixin"]

    tipo_referente_id = fields.Many2one('gevi_contatti.contatto_categoria',
                                        string='Tipo Referente', domain=[('tipo', 'ilike', 'referente')])

    agente_id = fields.Many2one('hr.employee', domain="[('job_id.name', 'ilike', 'Agente')]")

    utente_assegnato_id = fields.Many2one('res.users')

    codice_referente = fields.Char('Codice Amministratore', default="/")

    name = fields.Char('Nome', required=True)
    indirizzo = fields.Char('Via')
    indirizzo2 = fields.Char('Estensione via')
    citta = fields.Char('Citta')
    localita = fields.Char('Località')
    regione = fields.Char('Regione')
    cap = fields.Char('CAP', size=5)
    provincia = fields.Char('Provincia', size=2)
    tel = fields.Char('Telefono')
    cell = fields.Char('Cellulare')
    fax = fields.Char('Fax')
    email = fields.Char('E-mail')
    sitoweb = fields.Char('Sito Web')
    cf = fields.Char('Codice Fiscale', size=16)
    piva = fields.Char('Partita IVA', size=13)
    comuni_italiani_id = fields.Many2one('comuni_italiani.comune')
    customer_ids = fields.One2many(
        'res.partner', 'referente_id', string="Amministratore per", readonly=True)
    interlocutore = fields.Char('Interlocutore')
    note_interne = fields.Text('Note Interne')

    @api.onchange('comuni_italiani_id')
    def comuni_italiani_change(self):
        self.citta = self.comuni_italiani_id.name
        self.cap = self.comuni_italiani_id.cap
        self.provincia = self.comuni_italiani_id.provincia
        self.regione = self.comuni_italiani_id.regione

    @api.model_create_multi
    def create(self, values):
        result = super(Referente, self).create(values)
        result.codice_referente = self.env['ir.sequence'].next_by_code('gevi_contatti.referente')

        return result

    def invia_estratto_conto_scoperto(self):
        for line in self:
            clienti = self.env['res.partner'].search([('id', 'in', line.customer_ids.ids)])
            fatture = self.env['account.invoice'].search(
                ['&', ('partner_id', 'in', clienti.ids), ('state', 'in', ['open'])])

            tot_amm = 0

            for f in fatture:
                tot_amm = tot_amm + f.residual_company_signed

            if tot_amm == 0:
                raise exceptions.UserError('La situazione contabile è regolare e non verrà inviata nessuna email')
            else:
                # do export
                # id 12 = Invia estratto conto scoperto
                domain_template = [('id', '=', 12)]
                template_mail = self.env['mail.template'].search(domain_template)
                if line.email:
                    template_mail.email_to = line.email
                    template_mail.send_mail(line.id, force_send=True)
                    template_mail.email_to = None
                else:
                    raise exceptions.UserError("L'indirizzo email deve essere presente e valido")
