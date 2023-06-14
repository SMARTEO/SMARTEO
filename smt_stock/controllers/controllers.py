#-*- coding: utf-8 -*-
from collections import deque
import io
import json

from odoo import http, _
from odoo.http import content_disposition, request
from odoo.tools import ustr, osutil
from odoo.tools.misc import xlsxwriter

class SmtStock(http.Controller):

    # @http.route('/export', type='http', auth='user')
    # def export_handler(self, **kw):
    #     model = request.env['stock.picking']
    #     response = model.export_data_planning_issu()
    #     return response(environ=request.httprequest.environ)
    def _get_display_name(self, record, field_name):
        return getattr(record, field_name).display_name if field_name.endswith("_id") else str(getattr(record, field_name))
    @http.route('/stock_picking/export/xlsx', type='http', auth='user')
    def export_xlsx_handler(self, ids):
        output = io.BytesIO()
        ids = [int(id) for id in ids.strip('][').split(', ')]
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet(_('Stock Picking'))
        header_bold = workbook.add_format({'bold': True, 'pattern': 1, 'bg_color': '#AAAAAA'})
        header_plain = workbook.add_format({'pattern': 1, 'bg_color': '#AAAAAA'})
        bold = workbook.add_format({'bold': True})
        headers = request.env['stock.picking']._fields.keys()
        for c, header in enumerate(headers):
            worksheet.write(0, c, header, header_bold)
        records = request.env['stock.picking'].browse(ids)
        l = 1
        for record in records:
            for c, field_name in enumerate(headers):
                worksheet.write(l, c, self._get_display_name(record, field_name), header_plain)
            l += 1
        workbook.close()
        xlsx_data = output.getvalue()
        filename = osutil.clean_filename(_("Raport %(title)s (%(model_name)s)", title=_('Problèmes de planning'), model_name="stock_picking"))
        response = request.make_response(xlsx_data,
                                         headers=[('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                                  ('Content-Disposition', content_disposition(filename + '.xlsx'))],
                                         )

        return response
    #@http.route('/smt_stock/smt_stock', auth='public')
    # def index(self, **kw):
    #     return "Hello, world"
    #
    # @http.route('/smt_stock/smt_stock/objects', auth='public')
    # def list(self, **kw):
    #     return http.request.render('smt_stock.listing', {
    #         'root': '/smt_stock/smt_stock',
    #         'objects': http.request.env['smt_stock.smt_stock'].search([]),
    #     })
    #
    # @http.route('/smt_stock/smt_stock/objects/<model("smt_stock.smt_stock"):obj>', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('smt_stock.object', {
    #         'object': obj
    #     })

