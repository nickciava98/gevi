# -*- coding: utf-8 -*-
{
    'name': "Gevi Commerciale",

    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. """,

    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE

        Commerciale
        -   Appuntamenti
        -   Miei Amministratori
        -   Comunicazioni


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
        'base', 'gevi_verbali', 'gevi_contatti'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/referente.xml',
        'views/appuntamento.xml',
        'views/comunicazione.xml',
        'views/wizard_assegna_isp.xml',
        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.
        'views/menu_contatti.xml',
        'views/gevi_menu_commerciale.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'application': True,
}
