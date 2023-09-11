# -*- coding: utf-8 -*-
{
    'name': "Gevi Verbali",

    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. """,

    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE

        Funzioni disponibili:
            - Crea il menù Verbali
            - Gestione Verbale

        wizard:
            - Assegnazione massiva Responsabile Tecnico
            - Assengazione massiva Ispettore

        Automatismi:
            - Creazione OdV a verbale Convalidato

        Da fare:
            - Filtro Periodico / straordinario


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
        'base',
        'hr',
        'gevi_contatti',
        'gevi_contratti',
        'gevi_impianti',
        'comuni_italiani',
        'gevi_zone'
        ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'data/gevi_verbali.osservazione_categoria.csv',
        # 'data/gevi_verbali.osservazione.csv',
        'templates.xml',
        'data/verbale_sequence.xml',
        'views/osservazione.xml',
        'views/osservazione_categoria.xml',
        'views/contratto.xml',
        'views/raccomandazione.xml',
        'views/osservazione_mat.xml',
        'views/normeascensori.xml',
        'views/wizard_assegna_rt.xml',
        'views/wizard_assegna_isp.xml',
        'views/wizard_conferma.xml',
        # 'views/verbale_workflow.xml',
        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.
        'views/gevi_menu_verbali.xml',
        'views/verbale.xml',
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
