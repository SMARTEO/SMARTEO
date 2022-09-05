# -*- coding: utf-8 -*-
# from odoo import http


# class SmtAccount(http.Controller):
#     @http.route('/smt_account/smt_account', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smt_account/smt_account/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('smt_account.listing', {
#             'root': '/smt_account/smt_account',
#             'objects': http.request.env['smt_account.smt_account'].search([]),
#         })

#     @http.route('/smt_account/smt_account/objects/<model("smt_account.smt_account"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smt_account.object', {
#             'object': obj
#         })
