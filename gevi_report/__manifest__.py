# -*- coding: utf-8 -*-
{
    'name': "Gevi Report",
    'summary': """
        Gestione dei Report per Verifiche Ispettive""",
    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE

    Funzioni disponibili:
        - Gestione Report (stampa) Contratti
        - Gestione Report (stampa) Verbali
        - Gestione Report (stampa) Fattura (riepilogo conti in last-page)

    """,
    'author': "Niccolò Ciavarella",
    'website': "http://www.nciavarella.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'gevi_contratti',
                'gevi_verbali',
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/layouts.xml',
        'views/report_contratto.xml',
        'views/qweb_report_contratto.xml',
        'views/report_verbale.xml',
        'views/qweb_report_verbale.xml',
        'views/report_no_stampa.xml',
        'views/report_verbale_ascensore_periodica.xml',
        'views/report_verbale_ascensore_straordinaria.xml',
        'views/report_verbale_mat.xml',
        'views/report_verbale_satm.xml',
        'views/report_verbale_pem_periodica.xml',
        'views/report_verbale_pem_straordinaria.xml',
        'views/report_fattura.xml',
        'views/qweb_report_fattura.xml',
    ],
    # only loaded in demonstration mode
    'demo': ['demo.xml', ],

    'application': True,
    'license': 'LGPL-3',
}
