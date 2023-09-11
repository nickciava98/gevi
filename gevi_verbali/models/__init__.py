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


from . import contratto
from . import normeascensori
from . import osservazione
from . import osservazione_categoria
from . import osservazione_mat
from . import raccomandazione
from . import utpcei
from . import verbale
from . import verbale_osservazione_mat_riga
from . import verbale_osservazione_riga
from . import verbale_raccomandazione_riga
from . import verbale_rilievo_mat_riga
from . import verbale_rilievo_riga
from . import verbale_riscontro_riga
