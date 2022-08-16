# -*- coding: utf-8 -*-
# from odoo import http


# class SmtStock(http.Controller):
#     @http.route('/smt_stock/smt_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smt_stock/smt_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('smt_stock.listing', {
#             'root': '/smt_stock/smt_stock',
#             'objects': http.request.env['smt_stock.smt_stock'].search([]),
#         })

#     @http.route('/smt_stock/smt_stock/objects/<model("smt_stock.smt_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smt_stock.object', {
#             'object': obj
#         })
