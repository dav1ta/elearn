# -*- coding: utf-8 -*-
# from odoo import http


# class Elearn-system(http.Controller):
#     @http.route('/elearn-system/elearn-system', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/elearn-system/elearn-system/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('elearn-system.listing', {
#             'root': '/elearn-system/elearn-system',
#             'objects': http.request.env['elearn-system.elearn-system'].search([]),
#         })

#     @http.route('/elearn-system/elearn-system/objects/<model("elearn-system.elearn-system"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('elearn-system.object', {
#             'object': obj
#         })
