# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class PurchaseBillUnion(models.Model):
    _inherit = 'purchase.bill.union'

    def name_get(self):
        return [(rec.id, rec.name) for rec in self]