# -*- coding: utf-8 -*-
# from odoo import http


# class SmtHr(http.Controller):
#     @http.route('/smt_hr/smt_hr', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smt_hr/smt_hr/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('smt_hr.listing', {
#             'root': '/smt_hr/smt_hr',
#             'objects': http.request.env['smt_hr.smt_hr'].search([]),
#         })

#     @http.route('/smt_hr/smt_hr/objects/<model("smt_hr.smt_hr"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smt_hr.object', {
#             'object': obj
#         })
