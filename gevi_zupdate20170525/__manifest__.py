# -*- coding: utf-8 -*-
{
    'name': "Gevi z-Update20170525",

    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. """,

    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE
        Update del 25-05-2017
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
        'base', 'gevi_verbali', 'gevi_contatti', 'account', 'gevi_impianti', 'gevi_zone',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/partner.xml',
        'views/verbale.xml',
        'views/impianto.xml',
        'views/account_invoice.xml',
        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.
        'views/menu_verbali.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'application': False,
    'license': 'LGPL-3',
}
