# -*- coding: utf-8 -*-
from odoo import http

# class MethodApiDeuda(http.Controller):
#     @http.route('/method_api_deuda/method_api_deuda/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/method_api_deuda/method_api_deuda/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('method_api_deuda.listing', {
#             'root': '/method_api_deuda/method_api_deuda',
#             'objects': http.request.env['method_api_deuda.method_api_deuda'].search([]),
#         })

#     @http.route('/method_api_deuda/method_api_deuda/objects/<model("method_api_deuda.method_api_deuda"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('method_api_deuda.object', {
#             'object': obj
#         })