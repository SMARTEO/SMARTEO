# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductValue(models.Model):
    _inherit = "product.value"

    categ_id = fields.Many2one("product.category", related="product_id.categ_id", store=True)
    default_code = fields.Char(
        related="product_id.default_code", store=True, string="Internal Reference"
    )
