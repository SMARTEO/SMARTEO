# -*- coding: utf-8 -*-
# from odoo import http


# class SmtPurchase(http.Controller):
#     @http.route('/smt_purchase/smt_purchase', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smt_purchase/smt_purchase/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('smt_purchase.listing', {
#             'root': '/smt_purchase/smt_purchase',
#             'objects': http.request.env['smt_purchase.smt_purchase'].search([]),
#         })

#     @http.route('/smt_purchase/smt_purchase/objects/<model("smt_purchase.smt_purchase"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smt_purchase.object', {
#             'object': obj
#         })
