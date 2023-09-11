# -*- coding: utf-8 -*-
{
    'name': "Gevi Zone",
    'summary': """
        Gestione delle Zone per Verifiche Ispettive""",
    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE

    Rilasci futuri:
        - Menu

    """,
    'author': "Niccolò Ciavarella",
    'website': "http://www.nciavarella.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '0.9',

    # any module necessary for this one to work correctly
    'depends': ['base', 'comuni_italiani', 'gevi_contatti', 'gevi_impianti', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'data/gevi_zone.zona_agente.csv',
        'templates.xml',
        'views/referente.xml',
        'views/manutentore.xml',
        'views/partner.xml',
        'views/impianto.xml',
        'views/hr.xml',
        # 'views/zona_agente.xml',
        'views/zona_commerciale.xml',
        'views/zona_impianto.xml',

        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.
        'views/gevi_menu_zone.xml',

    ],
    # only loaded in demonstration mode
    'demo': ['demo.xml', ],

    'application': True,
}
