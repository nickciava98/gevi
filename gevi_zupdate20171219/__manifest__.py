# -*- coding: utf-8 -*-
{
    'name': "Gevi z-Update20171219",

    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. """,

    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE
        Update del 19-12-2017 operativo il giorno 11-01-2018
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
    'license': 'LGPL-3',
}
