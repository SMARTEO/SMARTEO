# -*- coding: utf-8 -*-
# from odoo import http


# class SmtSale(http.Controller):
#     @http.route('/smt_sale/smt_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smt_sale/smt_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('smt_sale.listing', {
#             'root': '/smt_sale/smt_sale',
#             'objects': http.request.env['smt_sale.smt_sale'].search([]),
#         })

#     @http.route('/smt_sale/smt_sale/objects/<model("smt_sale.smt_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smt_sale.object', {
#             'object': obj
#         })
