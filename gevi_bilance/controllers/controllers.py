# -*- coding: utf-8 -*-
from openerp import http

# class GeviBilance(http.Controller):
#     @http.route('/gevi_bilance/gevi_bilance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gevi_bilance/gevi_bilance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gevi_bilance.listing', {
#             'root': '/gevi_bilance/gevi_bilance',
#             'objects': http.request.env['gevi_bilance.gevi_bilance'].search([]),
#         })

#     @http.route('/gevi_bilance/gevi_bilance/objects/<model("gevi_bilance.gevi_bilance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gevi_bilance.object', {
#             'object': obj
#         })