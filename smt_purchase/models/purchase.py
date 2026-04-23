# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    dateorder_dateapprove = fields.Char(compute='_compute_combined_date')

    def _compute_combined_date(self):
        for purchase in self:
            if not purchase.date_order:
                purchase.dateorder_dateapprove = ""
            elif purchase.date_approve:
                purchase.dateorder_dateapprove = purchase.date_approve.strftime('%d-%m-%Y')
            else:
                purchase.dateorder_dateapprove = purchase.date_order.strftime('%d-%m-%Y')
