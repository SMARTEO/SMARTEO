# -*- coding: utf-8 -*-

from datetime import datetime, time
from dateutil.relativedelta import relativedelta


from odoo import api, fields, models, _



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    dateorder_dateapprove = fields.Char(compute='_compute_combined_date')

    def _compute_combined_date(self):
        for purchase in self:
            # if purchase.date_order and purchase.date_approve:
            # date_order = purchase.date_order.strftime('%d-%b-%Y')
            # date_approve = purchase.date_approve.strftime('%d-%b-%Y')
            # purchase.dateorder_dateapprove = f"{date_order}  {date_approve}"
            if not purchase.date_order:
                purchase.dateorder_dateapprove = ""
            elif purchase.date_approve:
                purchase.dateorder_dateapprove = f"{purchase.date_approve.strftime('%d-%m-%Y')}"
            else:
                purchase.dateorder_dateapprove = f"{purchase.date_order.strftime('%d-%m-%Y')}"


