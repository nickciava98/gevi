# -*- coding: utf-8 -*-
{
    'name': "Gevi Impianti",
    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. """,
    'description': """
        Versione Impianti
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE

        Funzioni disponibili:
            - Crea il menù Impianti
            - Gestione Impianti

        Configurazione:
            - Categoria Impianto
            - Attributo Descrittivo
            - Attributo Riscontro
            - Attributo Rilievo
            - Valore Attributo
            - Unità di misura

        Da fare:
            - name_get così formato: nomecliente+etichetta+codiceimpianto

    """,
    'author': "Niccolò Ciavarella",
    'website': "http://www.nciavarella.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '0.9',

    # any module necessary for this one to work correctly
    'depends': ['base', 'comuni_italiani', 'mail', 'gevi_contatti'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'data/gevi.impianti.unita_di_misura.csv',
        # 'data/gevi.impianti.impianto_categoria.csv',
        # 'data/gevi.impianti.valore_attributo.csv',
        # 'data/gevi.impianti.impianto_attributo_descrittivo.csv',
        # 'data/gevi.impianti.impianto_attributo_riscontro.csv',
        # 'data/gevi.impianti.impianto_attributo_rilievo.csv',
        # 'templates.xml',
        'data/impianto_sequence.xml',
        'views/impianto.xml',
        'views/partner.xml',
        'views/impianto_categoria.xml',
        'views/impianto_riga_descrizione.xml',
        'views/impianto_attributo_descrittivo.xml',
        'views/impianto_attributo_riscontro.xml',
        'views/impianto_attributo_rilievo.xml',
        'views/impianto_attributo_rilievo_mat.xml',
        'views/valore_attributo.xml',
        'views/unita_di_misura.xml',
        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.

        'views/gevi_menu_impianti.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'application': True,
    'license': 'LGPL-3',

}
