# -*- coding: utf-8 -*-
{
    'name': "Comuni Italiani",

    'summary': """
        Anagrafica dei Comuni Italiani """,

    'description': """
        Anagrafica di Comuni Italiani con CAP, Provincia e Regione ordinati per priorità di visualizzazione
        Configurazione delle priorità

    """,

    'author': "Niccolò Ciavarella",
    'website': "http://www.nciavarella.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.9',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/comuni_italiani.comune.csv',
        'templates.xml',
        'views/comuni_italiani.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
