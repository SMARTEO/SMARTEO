# -*- coding: utf-8 -*-

from ast import Store
from odoo import models, fields, api


class StockValuationLayerInherit(models.Model):
    _inherit = "stock.valuation.layer"
    categ_id = fields.Many2one(
        "product.category", related="product_id.categ_id", store=True
    )
    defaul_code = fields.Char(
        related="product_id.default_code", store=True, string="Reference article"
    )

    standard_price = fields.Float(
        related="product_id.standard_price",
        store=True,
        string="Prix unitaire",
        group_operator="avg",
    )

    values = fields.Float(
        string="Valeur", store=True, readonly=True, compute="_compute_value"
    )

    @api.depends("quantity", "standard_price")
    def _compute_value(self):
        for record in self:
            record.values = record.quantity * record.standard_price
