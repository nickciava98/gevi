# -*- coding: utf-8 -*-
{
    'name': "Gevi Pannelli Operativi",

    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. """,

    'description': """
        Processi operativi di supporto per l'aggiornamento massivo dei dati

        Viene implementato un pannello per ogni entità del sistema

        Implementati:
        -   gevi_contatti.referente: Cambio zona commerciale per Amministratore

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
        'base', 'gevi_contatti', 'gevi_zone',
        ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/pannello_operativo_referente.xml',
        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
	'application': True,
}
