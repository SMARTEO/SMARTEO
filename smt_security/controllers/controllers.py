# -*- coding: utf-8 -*-
# from odoo import http


# class SmtSecurity(http.Controller):
#     @http.route('/smt_security/smt_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smt_security/smt_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smt_security.listing', {
#             'root': '/smt_security/smt_security',
#             'objects': http.request.env['smt_security.smt_security'].search([]),
#         })

#     @http.route('/smt_security/smt_security/objects/<model("smt_security.smt_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smt_security.object', {
#             'object': obj
#         })
