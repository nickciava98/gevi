# -*- co/ding: utf-8 -*-
{
    'name': "Gevi Bilance",

    'summary': """
        Gestione delle Verifiche Ispettive Bilance per ICOVER S.R.L. """,
    'description': """
        -- ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE --
        
        --- Gestione delle Verifiche Ispettive per Bilance ---
    """,
    'author': "Giovanni Bonaventuri",
    'website': "http://www.icoversrl.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'TEST',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded  rispettare lo ordine 
    'data': [
        # 'security/ir.model.access.csv',
        'data/gevi_bilance.classe.csv',
        'data/gevi_bilance.tipobilanciatable.csv',
        'views/anagrafica_view.xml',
        'views/classe_view.xml',
        'views/TipoBilancia_view.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}