# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    categ_id = fields.Many2one(
        "product.category", related="product_id.categ_id", store=True
    )
    defaul_code = fields.Char(
        related="product_id.default_code", store=True, string="Internal Reference"
    )
    standard_price = fields.Float(
        related="product_id.standard_price",
        store=True,
        string="Unit Price",
        group_operator="avg",
    )
    values = fields.Float(
        string="Total Value", store=True, readonly=True, compute="_compute_value"
    )

    @api.depends("quantity", "standard_price")
    def _compute_value(self):
        for record in self:
            record.values = record.quantity * record.standard_price
