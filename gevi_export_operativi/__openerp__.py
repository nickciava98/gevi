# -*- coding: utf-8 -*-
{
    'name': "Gevi Export Operativi",
    'summary': """
        Gestione dei Report Estesi per ICOVER S.R.L. """,
    'description': """
        Gestione dei Report Estesi per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE

    Funzioni disponibili:
        - Esportazione XLS per Ministero
        - Esportazione XLS per Manutentori
        - Esportazione XLS per Ispettori
        - Esportazione XLS per Monitoraggio

    """,
    'author': "Antonio Longo",
    'website': "https://www.icoversrl.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '0.5',

    # any module necessary for this one to work correctly
    'depends': ['base', 'gevi_verbali',
               ],


    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/wizard_export_operativo.xml',
        'views/elenco_export.xml',
        # menu ultima vista
        'views/menu_export_operativi.xml',
    ],
    # only loaded in demonstration mode
    'demo': ['demo.xml'],

    'application': True,
}
