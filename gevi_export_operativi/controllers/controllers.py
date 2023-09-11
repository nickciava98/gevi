# -*- coding: utf-8 -*-

# class Gevi(http.Controller):
#     @http.route('/gevi/gevi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gevi/gevi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gevi.listing', {
#             'root': '/gevi/gevi',
#             'objects': http.request.env['gevi.gevi'].search([]),
#         })

#     @http.route('/gevi/gevi/objects/<model("gevi.gevi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gevi.object', {
#             'object': obj
#         })
