# -*- coding: utf-8 -*-
{
    'name': "Gevi Contratti",

    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. """,

    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE

    Funzioni disponibili:
        - Crea il menù Contratti
        - Gestione Contratti, vista revisionata. 

    Automatismi:
        - Creazione verifica periodica (bottone funzionante)
        - Creazione verifica straordinaria da terminare.


    """,

    'author': "Niccolò Ciavarella",
    'website': "http://www.nciavarella.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '0.7',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'gevi_contatti',
        'gevi_impianti',
        'comuni_italiani'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'data/gevi_impianti.impianto_categoria.csv',
        'templates.xml',
        'views/contratto.xml',
        'data/contratto_sequence.xml',
        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.
        'views/gevi_menu_contratti.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
        # 'security/ir.model.access.csv',
        # 'data/gevi_impianti.impianto_categoria.csv',
        # 'data/gevi_impianti.impianto_attributo_rilievo.csv',
        # 'data/gevi_impianti.impianto_attributo_riscontro.csv',
        # 'data/gevi_impianti.valore_attributo.csv',
    ],
    'application': True,
}
