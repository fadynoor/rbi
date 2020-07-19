# -*- coding: utf-8 -*-
# from odoo import http


# class StockRbi(http.Controller):
#     @http.route('/stock_rbi/stock_rbi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_rbi/stock_rbi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_rbi.listing', {
#             'root': '/stock_rbi/stock_rbi',
#             'objects': http.request.env['stock_rbi.stock_rbi'].search([]),
#         })

#     @http.route('/stock_rbi/stock_rbi/objects/<model("stock_rbi.stock_rbi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_rbi.object', {
#             'object': obj
#         })
