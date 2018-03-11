# -*- coding: utf-8 -*-
from openerp import http

# class GestionMembres(http.Controller):
#     @http.route('/gestion_membres/gestion_membres/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_membres/gestion_membres/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_membres.listing', {
#             'root': '/gestion_membres/gestion_membres',
#             'objects': http.request.env['gestion_membres.gestion_membres'].search([]),
#         })

#     @http.route('/gestion_membres/gestion_membres/objects/<model("gestion_membres.gestion_membres"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_membres.object', {
#             'object': obj
#         })