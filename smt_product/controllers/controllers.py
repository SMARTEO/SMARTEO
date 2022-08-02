# -*- coding: utf-8 -*-
# from odoo import http


# class SmtProduct(http.Controller):
#     @http.route('/smt_product/smt_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smt_product/smt_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smt_product.listing', {
#             'root': '/smt_product/smt_product',
#             'objects': http.request.env['smt_product.smt_product'].search([]),
#         })

#     @http.route('/smt_product/smt_product/objects/<model("smt_product.smt_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smt_product.object', {
#             'object': obj
#         })
