# -*- coding: utf-8 -*-

### Appunti per il nuovo file python ###

# -*- coding: utf-8 -*-
# from odoo import models, fields, api, exceptions

# class nomeclasse(models.Model):
#     _name = 'nomemodulo.nomeclasse'

#     name = fields.Char()


### FINE Appunti per il nuovo file python ###




### Contesto __init__.py ###

# Inserire i nome dei modelli da importare del modulo nella forma nomefile senza estensione

# from . import nomeclasse


from . import impianto
from . import impianto_categoria
from . import impianto_attributo_descrittivo
from . import impianto_attributo_riscontro
from . import impianto_attributo_rilievo
from . import valore_attributo
from . import unita_di_misura
from . import partner
from . import impianto_riga_descrizione
from . import impianto_attributo_rilievo_mat
