# -*- coding: utf-8 -*-
{
    'name': "Gevi Wizard Operativi",

    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. """,

    'description': """
        Processi operativi di supporto per la correzione di anomalie

        Per nascondere i Processi di supporto dai modelli interessati, entrare in "Azioni" -> "Vincoli Azione"
        Cercare il wizard interessato e cambiare il campo Qualifier da "client_action_multi" a "client_action_multi_removeme".
        Per riabilitare il processo operativo, cambiare il Qualifier  da "client_action_multi_removeme" a "client_action_multi".

        Implementati:

        -   gevi_impianti: Carica Attributi Descrittivi, Carica Attributi descrittivi per pem caricate come pem e non come Ascensore Generico
        -   gevi_impianti: Cambio categoria impianto
        -   gevi_verbali: Cambio categoria impianto senza operatività

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
        'base', 'gevi_impianti', 'gevi_verbali',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_operativi_impianto.xml',
        'views/wizard_operativi_verbale.xml',
        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'application': False,
    'license': 'LGPL-3',
}
