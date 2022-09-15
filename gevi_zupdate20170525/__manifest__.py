# -*- coding: utf-8 -*-
{
    'name': "Gevi z-Update20170525",

    'summary': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. """,

    'description': """
        Gestione delle Verifiche Ispettive per ICOVER S.R.L. - ISTITUTO COLLAUDI VERIFICHE E RICERCHE

        Update del 25-05-2017
        Verbali:
            - Introduzione del flag “Prioritario” per segnalare le verifiche che hanno priorità
            - Introduzione della dicitura “esercente attività di”, per le sole verifiche di Messa a terra e scariche atmosferiche
            - Introduzione della periodicità nell’elenco delle verifiche
            - Per i verbali di terra e scariche atmosferiche è stata introdotto un controllo che, se è vero che il proprietario è diverso dal cliente, stampa il contenuto del campo proprietario_id
        Impianti:
            - Introduzione del proprietario dell’impianto perché potrebbe differire dal cliente di fatturazione, per tutti i tipi di impianto
        Contabilità:
            - Introduzione del raggruppamento per amministratore e per zona commerciale
            - Stampa dell’estratto conto dello scaduto per amministratore
        Commerciale:
            - Accesso alla schermata dei verbali riferiti agli amministratori associati così da permetterne anche la stampa

        Sono stati aggiornati i seguenti modelli:
        - partner: Inserimento campo tipo_attivita = fields.Char
        - verbale: Inserimento campi prioritario = fields.Boolean, tipo_attivita = fields.Char, periodicita = fields.Selection, utente_assegnato_referente_id = fields.Many2one
        - impianto: Inserimento campi proprietario_diverso = fields.Boolean, proprietario_id = fields.Many2one
        - account_invoice: Inserimento campi referente_id = fields.Many2one, zona_commerciale_referente_id = fields.Many2one
        

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
        'base', 'gevi_verbali', 'gevi_contatti', 'account', 'gevi_impianti', 'gevi_zone',
        ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/partner.xml',
        'views/verbale.xml',
        'views/impianto.xml',
        'views/account_invoice.xml',
        # il caricamento della vista dei menu deve essere l'ultima cosa specificata nel contesto data.
        'views/menu_verbali.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
	'application': False,
}