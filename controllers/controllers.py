# -*- coding: utf-8 -*-
# from odoo import http


# class FormulirCuti(http.Controller):
#     @http.route('/formulir_cuti/formulir_cuti', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/formulir_cuti/formulir_cuti/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('formulir_cuti.listing', {
#             'root': '/formulir_cuti/formulir_cuti',
#             'objects': http.request.env['formulir_cuti.formulir_cuti'].search([]),
#         })

#     @http.route('/formulir_cuti/formulir_cuti/objects/<model("formulir_cuti.formulir_cuti"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('formulir_cuti.object', {
#             'object': obj
#         })
