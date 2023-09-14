# -*- coding: utf-8 -*-
{
    'name': "Gevi Contatti",
    'summary': """
        Gestione dei contatti per Verifiche Ispettive""",
    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE


    """,
    'author': "Niccolò Ciavarella",
    'website': "http://www.nciavarella.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'comuni_italiani', 'hr', 'mail', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/gevi_contatti.contatto_categoria.csv',
        'data/contatti_sequence.xml',
        'templates.xml',
        'views/referente.xml',
        'views/manutentore.xml',
        'views/partner.xml',
        'views/contatto_categoria.xml',

        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.
        'views/gevi_menu_contatti.xml',

    ],
    # only loaded in demonstration mode
    'demo': ['demo.xml', ],

    'application': True,
    'license': 'LGPL-3',
}
