# -*- coding: utf-8 -*-
from openerp import fields, models, api, exceptions

class Anagrafica(models.Model):
    _name = 'gevi_bilance.anagrafica'
    _description = "Anagrafica Bilance"
    # richiesto per openchatter
    _inherit = ['mail.thread']
    
    costruttore = fields.Char('Costruttore', default="/")
    modello = fields.Char('Modello', default="/")
    matricola = fields.Char('Matricola', default="/")

    numscale = fields.Selection(
        [
            ('singola_scala', 'Singola Scala'),
            ('doppia_scala', 'Doppia Scala'),
            ('tripla_scala', 'Tripla Scala'),
        ],
        default='singola_scala')
        
    tipo_bilancia_id = fields.Many2one('gevi_bilance.tipobilanciatable', ondelete='cascade', string="Tipo Bilancia", required=False) 

    classe_bilancia_id = fields.Many2one('gevi_bilance.classe', ondelete='cascade', string="Classe Bilancia", required=False)     
      
        
    #classe_id = fields.Many2one('gevi_bilance.classe', ondelete='set null', string="Classe", required=False)