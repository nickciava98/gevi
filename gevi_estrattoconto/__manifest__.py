# -*- coding: utf-8 -*-
{
    'name': "Gevi Estratto Conto",
    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L.""",
    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L.

    Funzioni disponibili:
        - Report Stampa Estratto Conto Storico
        - Report Stampa Estratto Conto Scaduto

    """,
    'author': "Niccolò Ciavarella",
    'website': "http://www.nciavarella.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'gevi_contatti', 'account',
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/qweb_report_storico.xml',
        'views/report_storico.xml',
    ],
    # only loaded in demonstration mode
    'demo': ['demo.xml'],

    'application': True,
}
