# -*- coding: utf-8 -*-
# from odoo import http


# class JuancitoAtrivia(http.Controller):
#     @http.route('/juancito_atrivia/juancito_atrivia/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/juancito_atrivia/juancito_atrivia/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('juancito_atrivia.listing', {
#             'root': '/juancito_atrivia/juancito_atrivia',
#             'objects': http.request.env['juancito_atrivia.juancito_atrivia'].search([]),
#         })

#     @http.route('/juancito_atrivia/juancito_atrivia/objects/<model("juancito_atrivia.juancito_atrivia"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('juancito_atrivia.object', {
#             'object': obj
#         })
