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

from . import hr
from . import impianto
from . import manutentore
from . import partner
from . import referente
# from . import zona_agente
from . import zona_commerciale
from . import zona_impianto
