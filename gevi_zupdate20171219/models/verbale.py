# -*- coding: utf-8 -*-
import logging
import xml.etree.ElementTree as etree

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class Verbale(models.Model):
    _inherit = 'gevi_verbali.verbale'

    stato_contratto = fields.Selection(
        string='Stato Contratto',
        readonly=True,
        related='contratto_id.state',
        store=True
    )

    def apri_verbale(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Verbale',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'target': 'current',
        }

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(Verbale, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            # Check if user is in group that allow creation
            # can_edit = True if self.env.uid == 1 or self.env.uid == self.ispettore_id.user_id or self.env.uid == self.responsabile_tecnico_id.user_id else False
            # _logger.info('******************************** res.ispettore_id.user_id: {0}'.format(res.ispettore_id.user_id))
            # _logger.info('******************************** res.ispettore_id.user_id.id: {0}'.format(res.ispettore_id.user_id.id))
            # _logger.info('******************************** res.is_ispettore: {0}'.format(res.is_ispettore))
            # _logger.info('******************************** res.responsabile_tecnico_id.user_id: {0}'.format(res.responsabile_tecnico_id.user_id))
            # _logger.info('******************************** res.responsabile_tecnico_id.user_id.id: {0}'.format(res.responsabile_tecnico_id.user_id.id))
            # _logger.info('******************************** res.is_responsabile_tecnico: {0}'.format(res.is_responsabile_tecnico))
            can_edit = True
            if not can_edit:
                root = etree.fromstring(res['arch'])
                root.set('edit', 'false')
                res['arch'] = etree.tostring(root)
        return res
