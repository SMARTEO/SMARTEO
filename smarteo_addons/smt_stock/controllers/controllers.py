#-*- coding: utf-8 -*-
import io

from odoo import http, _
from odoo.http import content_disposition, request
from openpyxl import Workbook
from openpyxl.styles import Font
from werkzeug.wrappers import Response


class SmtStock(http.Controller):

    @http.route('/stock_picking/export/xlsx', type='http', auth='user')
    def export_xlsx_handler(self, ids):
        ids = [int(id) for id in ids.strip('][').split(', ')]
        records = request.env['stock.picking'].browse(ids)

        workbook = Workbook()

        sheet = workbook.active

        headers = ['Nom du partenaire', 'Document d origine', 'Date de la commande', 'Description du mouvement de stock', 'Quantité', 'Date prévue']
        sheet.append(headers)
        header_row = sheet[1]
        for cell in header_row:
            cell.font = Font(bold=True)
        for record in records:
            for st_move in record.move_ids:
                st_name = st_move.name
                st_product_qty = st_move.product_qty
            data = [record.partner_id.name, record.origin, record.date.strftime("%d-%m-%Y"), st_name, st_product_qty, record.scheduled_date.strftime("%d-%m-%Y")]
            sheet.append(data)
        file_stream = io.BytesIO()
        workbook.save(file_stream)
        file_stream.seek(0)

        file_content = file_stream.read()

        filename = 'probleme_planning_data.xlsx'

        response = Response(
            file_content,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename=%s' % filename),
            ]
        )
        return response
