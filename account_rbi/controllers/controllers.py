# -*- coding: utf-8 -*-
# from odoo import http


# class AccountRbi(http.Controller):
#     @http.route('/account_rbi/account_rbi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_rbi/account_rbi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_rbi.listing', {
#             'root': '/account_rbi/account_rbi',
#             'objects': http.request.env['account_rbi.account_rbi'].search([]),
#         })

#     @http.route('/account_rbi/account_rbi/objects/<model("account_rbi.account_rbi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_rbi.object', {
#             'object': obj
#         })
