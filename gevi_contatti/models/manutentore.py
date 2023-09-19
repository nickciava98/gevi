# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Manutentore(models.Model):
    _name = 'gevi_contatti.manutentore'
    _description = "Manutentore"

    # richiesto per openchatter
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char('Nome', required=True)
    codice_manutentore = fields.Char('Codice Manutentore', default="/")

    tipo_manutentore_id = fields.Many2one(
        'gevi_contatti.contatto_categoria',
        string='Tipo Manutentore',
        domain=[('tipo', 'ilike', 'manutentore')])

    indirizzo = fields.Char('Via')
    indirizzo2 = fields.Char('Estensione via')
    citta = fields.Char('Citta')
    localita = fields.Char('Località')
    regione = fields.Char('Regione')
    cap = fields.Char('CAP', size=5)
    provincia = fields.Char('Provincia', size=2, required=True)
    tel = fields.Char('Telefono')
    cell = fields.Char('Cellulare')
    fax = fields.Char('Fax')
    email = fields.Char('E-mail')
    sitoweb = fields.Char('Sito Web')
    cf = fields.Char('Codice Fiscale', size=16)
    piva = fields.Char('Partita IVA', size=13)
    comuni_italiani_id = fields.Many2one('comuni_italiani.comune')
    note_interne = fields.Text('Note Interne')
    interlocutore = fields.Char('Interlocutore')

    # metodo per controllare l'eventuale variazione di un campo specifico
    # def log_campo(self):
    #     if self.campo != '0':
    #         self.message_post(body="Variazione del campo", type='comment')

    def name_get(self):
        result = super(Manutentore, self).name_get()
        res = []
        for record in self:
            name = record.name
            provincia = record.provincia
            res.append((record.id, name + " (" + provincia + ")"))
        return res

    @api.onchange('comuni_italiani_id')
    def comuni_italiani_change(self):
        self.citta = self.comuni_italiani_id.name
        self.cap = self.comuni_italiani_id.cap
        self.provincia = self.comuni_italiani_id.provincia
        self.regione = self.comuni_italiani_id.regione

    @api.model_create_multi
    def create(self, values):
        result = super(Manutentore, self).create(values)
        result.codice_manutentore = self.env['ir.sequence'].next_by_code('gevi_contatti.manutentore')

        return result
