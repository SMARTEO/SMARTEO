# -*- coding: utf-8 -*-
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"
    _description = 'Transfer'

    def exp_button(self):
        return {
            "type": "ir.actions.act_url",
            "url": f"/stock_picking/export/xlsx?ids={self.ids}",
        }
