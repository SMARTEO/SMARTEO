# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    standard_price = fields.Float(
        related="product_id.standard_price",
        string="Unit Price",
        readonly=True,
        store=True,
        group_operator="avg",
    )
    category_id = fields.Many2one(
        "product.category",
        related="product_id.categ_id",
        string="Product Category",
        readonly=True,
        store=True,
    )
    values = fields.Float(string="Total Value", compute="_compute_values", store=True)

    @api.depends("inventory_quantity_auto_apply", "standard_price")
    def _compute_values(self):
        for record in self:
            record.values = record.inventory_quantity_auto_apply * record.standard_price
