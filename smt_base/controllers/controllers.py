# -*- coding: utf-8 -*-
# from odoo import http


# class SmtBase(http.Controller):
#     @http.route('/smt_base/smt_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smt_base/smt_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smt_base.listing', {
#             'root': '/smt_base/smt_base',
#             'objects': http.request.env['smt_base.smt_base'].search([]),
#         })

#     @http.route('/smt_base/smt_base/objects/<model("smt_base.smt_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smt_base.object', {
#             'object': obj
#         })
