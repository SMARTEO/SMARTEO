# -*- coding: utf-8 -*-
# from odoo import http


# class SmtContact(http.Controller):
#     @http.route('/smt_contact/smt_contact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smt_contact/smt_contact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smt_contact.listing', {
#             'root': '/smt_contact/smt_contact',
#             'objects': http.request.env['smt_contact.smt_contact'].search([]),
#         })

#     @http.route('/smt_contact/smt_contact/objects/<model("smt_contact.smt_contact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smt_contact.object', {
#             'object': obj
#         })
