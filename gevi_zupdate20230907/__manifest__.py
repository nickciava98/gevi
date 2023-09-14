# -*- coding: utf-8 -*-
{
    'name': "Gevi z-Update20230907",

    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. """,

    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE
        Aggiornamento verbali Messa a Terra
    """,

    'author': "Niccolò Ciavarella",
    'website': "http://www.icoversrl.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'gevi_verbali'
    ],

    # always loaded
    'data': [
        'views/verbale_form.xml',
        'views/report_verbale_mat.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'application': False,
    'license': 'LGPL-3',
}
