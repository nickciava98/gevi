# -*- coding: utf-8 -*-
{
    'name': "Gevi Bilance",

    'summary': """
        Gestione delle Verifiche Ispettive  """,

    'description': """
        Gestione delle Verifiche Ispettive 

        Gestione delle Bilance

    """,

    'author': "Niccolò Ciavarella, Antonio Longo",
    'website': "http://www.nciavarella.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 'sale_crm', 'gevi_contratti', 'gevi_impianti', 'gevi_verbali'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/crm_sale_opp_contratto.xml',
        'views/classe_bilancia.xml',
        'views/classe_pesiera.xml',
        'views/classe_strumento.xml',
        'views/pesiera.xml',
        'views/contratto.xml',
        'views/impianto.xml',

        # wizard
        'views/wizard_assegna_rt.xml',
        'views/wizard_assegna_isp.xml',
        'views/wizard_conferma.xml',

        'views/verbale.xml',

        'data/bilancia_sequence.xml',
        'data/classe_pesiera.xml',
        'data/classe_strumento.xml',

        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.
        'views/gevi_menu_bilance.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'application': False,
    'license': 'LGPL-3',
}
