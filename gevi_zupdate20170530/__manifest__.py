# -*- coding: utf-8 -*-
{
    'name': "Gevi z-Update20170530",

    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. """,

    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE

        Update del 30-05-2017
        Zone:
            Introduzione dei figli per le zone commerciali
            Introduzione dei figli per le zone impianto
            Computazione della zona commerciale nel referente (computazione _compute_propria_zona_commerciale in implementazione)
            Computazione della zona commerciale nel partner (computazione _compute_propria_zona_commerciale in implementazione)
            Computazione della zona impianto in impianto (computazione _compute_propria_zona_impianto in implementazione)
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
        'base', 'gevi_verbali', 'gevi_contatti', 'gevi_zone',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_assegna_agente.xml',
        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'application': False,
    'license': 'LGPL-3',
}
