# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"
    _description = 'Quant'

    standard_price = fields.Float(
        company_dependent=True,
        groups="base.group_user",
        related="product_id.standard_price",
        string="Unit Price",
        readonly=True,
        store=False,
        group_operator="avg",
    )
    category_id = fields.Many2one(
        "product.category",
        related="product_id.categ_id",
        string="Product Category",
        readonly=True,
        store=False,
    )
    values = fields.Float(string="Total Value", compute="_compute_values", store=False)

    @api.depends("inventory_quantity_auto_apply", "standard_price")
    def _compute_values(self):
        for record in self:
            record.values = record.inventory_quantity_auto_apply * record.standard_price
