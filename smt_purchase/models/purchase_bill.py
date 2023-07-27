# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class PurchaseBillUnion(models.Model):
    _inherit = 'purchase.bill.union'

    def name_get(self):
        result = []
        for doc in self:
            name = doc.name or ''
            if doc.reference:
                name += ' - ' + doc.reference
            amount = doc.amount
            if doc.purchase_order_id and doc.purchase_order_id.invoice_status == 'no':
                amount = 0.0
            name += ': ' + formatLang(self.env, amount, monetary=True, currency_obj=doc.currency_id)
            result.append((doc.id, name))
        return result