import operator as py_operator

from odoo import api, fields, models
from odoo.exceptions import UserError

_OPERATORS = {
    "=": py_operator.eq,
    "!=": py_operator.ne,
    ">": py_operator.gt,
    ">=": py_operator.ge,
    "<": py_operator.lt,
    "<=": py_operator.le,
}


class StockQuant(models.Model):
    _inherit = "stock.quant"
    _description = "Quant"

    standard_price = fields.Float(
        company_dependent=True,
        groups="base.group_user",
        related="product_id.standard_price",
        string="Unit Price",
        readonly=True,
        store=False,
        aggregator="avg",
    )
    category_id = fields.Many2one(
        "product.category",
        related="product_id.categ_id",
        string="Product Category",
        readonly=True,
        store=False,
    )
    values = fields.Float(
        string="Total Value",
        compute="_compute_values",
        search="_search_values",
        store=False,
    )

    @api.depends("inventory_quantity_auto_apply", "standard_price")
    def _compute_values(self):
        for record in self:
            record.values = record.inventory_quantity_auto_apply * record.standard_price

    def _search_values(self, operator, value):
        if operator not in _OPERATORS:
            raise UserError(
                self.env._(
                    "Unsupported operator %s on the 'Total Value' field.", operator
                )
            )
        op = _OPERATORS[operator]
        matching_ids = [
            quant.id for quant in self.search([]) if op(quant.values, value)
        ]
        return [("id", "in", matching_ids)]
