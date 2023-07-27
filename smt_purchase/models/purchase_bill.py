# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseBillUnion(models.Model):
    _inherit = 'purchase.bill.union'

    @api.model
    def _name_search(self, name="", args=None, operator="ilike", limit=100, name_get_uid=None):
        args = list(args or [])
        if name:
            args += [
                "|",
                "|",
                ("name", operator, name),
                ("reference", operator, name),
                ("partner_id", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)


