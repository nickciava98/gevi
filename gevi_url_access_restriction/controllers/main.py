# -*- coding: utf-8 -*-
import logging
from openerp import http, exceptions
from openerp.http import request
from openerp.addons.web.controllers import main
import logging
_logger = logging.getLogger(__name__)


class UrlAction(main.Action):

	@http.route()
	def load(self, action_id, do_not_eval=False, additional_context=None):

		try:
			action_id = int(action_id)
		except ValueError:
			# non è un id action di BE ma di WebClient
			return super(UrlAction, self).load(action_id, do_not_eval=do_not_eval, additional_context=additional_context)

		menu = False
		menu_ids = request.env['ir.ui.menu'].sudo().search([])
		for menu_id in menu_ids:
			if menu_id.action:
				if menu_id.action.id == action_id:
					menu = menu_id
		user = request.env['res.users'].sudo().browse(request.session.uid)
		# On vérifie s'il y a un menu associé à l'action
		if not self._user_has_acces_right(action_id, menu, user):
			# Si l'utilisateur n'a pas le droit d'accès au menu
			raise exceptions.AccessError("Accesso negato. Contattare l'amministratore di sistema.")
			# return {
			# 	'name': 'WARNING',
			# 	'type': 'ir.actions.client',
			# 	'tag': 'warning_message',
			# }

		return super(UrlAction, self).load(action_id, do_not_eval=do_not_eval, additional_context=additional_context)

	def _user_has_acces_right(self, action_id, menu, user):
		# S'il n'y a pas de menu associé à l'action, on vérifie si c'est une action window
		action = request.env['ir.actions.act_window'].sudo().search([('id','=',action_id)], limit=1)
		# Si c'est une action window et qu'il y a un group associé à l'action
		if action and len(action.groups_id) > 0:
			# On vérifie si l'utilisateur a droit à l'action
			if any(elem in user.groups_id.ids  for elem in action.groups_id.ids):
				# L'utilisateur a droit à l'action
				return True
			return False
		if menu and len(menu.groups_id.ids) > 0:
			if any(elem in user.groups_id.ids  for elem in menu.groups_id.ids):
				return True
			return False
		if menu and menu.parent_id:
			return self._user_has_acces_right(action_id, menu.parent_id, user)

		return True
