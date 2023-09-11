# -*- coding: utf-8 -*-
{
    'name': "Gevi z-Update20171219",

    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. """,

    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE

        Update del 19-12-2017 operativo il giorno 11-01-2018
        
        Fatture:
            - Introduzione campi related "Tipo Amministratore" e "Tipo Cliente" per Filtri e Raggruppamenti
            - Introduzione campi related "Utente Amministratore" e "Agente Amministratore" per Filtri e Raggruppamenti
        
        Pagamenti:
            - Introduzione campi related "Amministratore", "Zona Amministratore" e "Tipo Cliente" per Filtri e Raggruppamenti
            - Introduzione campi related "Utente Amministratore" e "Agente Amministratore" per Filtri e Raggruppamenti

        Contratti:
            - Introduzione campi related "Zona Amministratore", "Tipo Amministratore" e "Tipo Cliente" per Filtri e Raggruppamenti
            - Introduzione dello stato "disdetta_uv", ovvero Disdetta in attesa di ultima verifica
                Note: Attenzione al metodo "aggiorna_stato(self)" di contratto perché deve contemplare la logica della disdetta_uv

        Impianti:
            - Introduzione del campo One2many "verbali_ids", per permettere la navigazione delle verifiche precedenti attraverso l'impianto
            - Introduzione del metodo "apri_verbale" richiamabile dalla vista per aprire il verbale non in modalità popup/modale

        Vendite:
            - Introduzione del campo "verbale_id" per avere relazione tra vendite e verbali. 
            
                Note: Attenzione al metodo "_crea_ordine_vendita(self)" di verbale perché deve includere tra i campi 
                        ...
                        'origin': self.name,
                        'verbale_id': self.id,
                        ...

        Verbali:
            - Introduzione del campo related "stato_contratto" per avere informazioni sullo stato del contratto nella vista del verbale

    """,

    'author': "Niccolò Ciavarella",
    'website': "http://www.nciavarella.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 'account', 'gevi_contratti', 'gevi_impianti', 'sale', 'gevi_verbali', 'gevi_contatti', 'gevi_zone',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_invoice.xml',
        'views/account_payment.xml',
        'views/contratto.xml',
        'views/impianto.xml',
        'views/verbale.xml',
        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'application': False,
}
