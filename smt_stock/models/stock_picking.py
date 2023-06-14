# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models, http

from odoo.exceptions import AccessError
import csv
import os
# from odoo.tools.misc import xlsxwriter
import base64
import re
import io
# from openpyxl import Workbook
from odoo.http import request
from werkzeug.wrappers import Response
from odoo.http import Controller
import json

class PickingType(models.Model):
    _inherit = "stock.picking.type"

    # def get_stock_picking_action_picking_type(self):
    #     if self.env.user.has_group('smt_stock.group_show_stock_picking_planing'):
    #         return self._get_action('smt_stock.stock_picking_action_picking_type_planing')
    #     else:
    #         return self._get_action('stock.stock_picking_action_picking_type')


class StockPicking(models.Model):
    _inherit = "stock.picking"

    # def export_data(self, fields_to_export):
    #     if not self.env.is_admin():
    #         raise AccessError(_("Only administrators are allowed to export mail message"))
    #
    #     return super(StockPicking, self).export_data(fields_to_export)


    # def export_data_planning_issu(self):
    #
    #     records = self.search([])
    #     fieldnames = ['name', 'location_id', 'location_dest_id', 'partner_id']
    #
    #     folder_path = '/home/michael/Downloads'
    #     filename = 'export_data.csv'
    #
    #     if not os.path.exists(folder_path):
    #         os.makedirs(folder_path)
    #
    #     file_path = os.path.join(folder_path, filename)
    #
    #     with open(file_path, 'w', newline='') as csvfile:
    #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #
    #         writer.writeheader()
    #         for record in records:
    #             writer.writerow({
    #                 'name': record.name,
    #                 'location_id': record.location_id,
    #                 'location_dest_id': record.location_dest_id,
    #                 'partner_id': record.partner_id
    #             })
    #
    #     return True

    # def export_data_planning_issu(self):
    #     # Récupérer les enregistrements à exporter
    #     records = self.search([])
    #
    #     # Créer un nouveau classeur Excel
    #     workbook = Workbook()
    #
    #     # Créer une feuille de calcul
    #     sheet = workbook.active
    #
    #     # Écrire les en-têtes de colonnes
    #     sheet.append(['name', 'location_id', 'location_dest_id', 'partner_id'])
    #
    #     # Parcourir les enregistrements et écrire chaque ligne
    #     for record in records:
    #         sheet.append([record.name, record.location_id.name, record.location_dest_id.name, record.partner_id.name])
    #
    #     # Définir le chemin d'accès et le nom du fichier de sortie
    #     filename = 'export_data.xlsx'
    #
    #     # Enregistrer le classeur Excel dans le fichier XLSX
    #     workbook.save(filename)
    #
    #     # Faire quelque chose avec le fichier exporté, par exemple l'envoyer en tant que réponse HTTP
    #
    #     return True





    # def export_data_planning_issu(self):
    #
    #     records = self.search([])
    #
    #     workbook = Workbook()
    #
    #     sheet = workbook.active
    #
    #     headers = ['Champ 1', 'Champ 2', 'Champ 3']
    #     sheet.append(headers)
    #
    #     for record in records:
    #         data = [record.name, record.name, record.name]
    #         sheet.append(data)
    #     file_stream = io.BytesIO()
    #     workbook.save(file_stream)
    #     file_stream.seek(0)
    #
    #     file_content = base64.b64encode(file_stream.read()).decode('utf-8')
    #
    #
    #     filename = 'export_data.xlsx'
    #
    #     # Renvoyer le fichier Excel en tant que réponse HTTP pour le téléchargement automatique
    #     response = Response(
    #         file_content,
    #         headers=[
    #             ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
    #             ('Content-Disposition', 'attachment; filename=%s' % filename),
    #         ]
    #     )
    #     return response

    def exp_button(self):
        # data = self.export_data(self._fields.keys())
        return {
            "type": "ir.actions.act_url",
            "url": f"/stock_picking/export/xlsx?ids={self.ids}",
        }



    # @api.model
    # def default_get(self, fields):
    #     if self.env.user.has_group('smt_stock.group_show_stock_picking_planing'):
    #         defaults = super(StockPicking, self).default_get(fields)
    #         defaults['planning_issues'] = True
    #     return defaults



