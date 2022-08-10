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
    name = fields.Char('Nome', default="/") #compute='_onchange_name', store=True

    numscale = fields.Selection(
        [
            ('singola_scala', 'Singola Scala'),
            ('doppia_scala', 'Doppia Scala'),
            ('tripla_scala', 'Tripla Scala'),
        ],
        default='singola_scala')
        
    tipo_bilancia_id = fields.Many2one('gevi_bilance.tipobilanciatable', ondelete='cascade', string="Tipo Bilancia", required=False) 

    classe_bilancia_id = fields.Many2one('gevi_bilance.classe', ondelete='cascade', string="Classe Bilancia", required=False)    

    punti_di_supporto = fields.Integer(string="Punti di supporto")   
      
        
    #classe_id = fields.Many2one('gevi_bilance.classe', ondelete='set null', string="Classe", required=False)
    
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, u"%s-%s-%s" % (record.costruttore, record.modello, record.matricola)))
            #self.name = ' '.join(result)
        #result.append((self.id, u"%s %s %s" % (self.costruttore, self.modello, self.matricola)))
        return result
        #result.append((self.id, u"%s" %(self.costruttore + "-" + self.modello + "-" + self.matricola)))
        #self.name = ' '.join(result)
        
    #@api.one
    #@api.onchange('name')
    #def _onchange_name(self):
    #    #record = self
    #    self.name = self.costruttore + " " + self.modello + " " + self.matricola
    #    return self.name
        
        
        