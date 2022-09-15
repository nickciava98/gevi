# -*- coding: utf-8 -*-
{
    'name': "Gevi FatturaPA",

    'summary': """
        Generazione della fattura elettronica 1.2.1
        """,

    'description': """
        Generazione della fattura elettronica - Versione 1.2.1
        
        Link di riferimento: https://www.fatturapa.gov.it/export/fatturazione/it/normativa/f-2.htm
        
        Aggiornato alla versione 1.2.1 il 16/10/2018
        
        Dopo l'installazione è necessario:
        In Contabilità -> configurazione -> configurazione -> Fattura Elettronica
        -   configurare il telefono da impostare nell'xml
        -   configurare il fax da impostare nell'xml
        -   configurare l'e-mail da impostare nell'xml
        -   configurare l'ID trasmittente (che dovrebbe essere aruba) da impostare nell'xml
        -   configurare la posizione fiscale (regime ordinario)
        -   configurare i Dati REA
        
        Inoltre: 
        -   impostare la provincia nel partner collegato all'azienda
        -   impostare i dati fiscali per i termini di pagamento
        -   impostare l'esigibilità per i codici iva
         
        Verificare la generazione per la pubblica amministrazione!!
    """,

    'author': "Niccolò Ciavarella",
    'website': "http://www.nciavarella.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'account',
                'gevi_contatti',
                'l10n_it_account_tax_kind',
                'l10n_it_fiscal_payment_term',
                'l10n_it_split_payment',
                'l10n_it_esigibilita_iva',
                'l10n_it_rea',
                'partner_firstname',
                ],

    # always loaded
    'data': [
        'data/fatturapa_data.xml',
        'data/fatturapa_sequence.xml',
        'data/welfare.fund.type.csv',
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/account_view.xml',
        'views/attachment_view.xml',
        'views/partner.xml',
        'views/company_view.xml',
        'wizard/wizard_export_fatturapa_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'external_dependencies': {
        'python': [
            'pyxb',  # pyxb 1.2.5
            'unidecode',
        ],
    }
}
