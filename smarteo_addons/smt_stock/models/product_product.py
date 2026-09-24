import operator as py_operator

from odoo import fields, models
from odoo.exceptions import UserError

_OPERATORS = {
    "=": py_operator.eq,
    "!=": py_operator.ne,
    ">": py_operator.gt,
    ">=": py_operator.ge,
    "<": py_operator.lt,
    "<=": py_operator.le,
}


class ProductProduct(models.Model):
    _inherit = "product.product"
    _description = "Product Variant"

    values = fields.Float(
        string="Total Value",
        compute="_compute_values",
        search="_search_values",
        store=False,
    )

    def _compute_values(self):
        for record in self:
            record.values = record.qty_available * record.standard_price

    def _search_values(self, operator, value):
        if operator not in _OPERATORS:
            raise UserError(
                self.env._(
                    "Unsupported operator %s on the 'Total Value' field.", operator
                )
            )
        op = _OPERATORS[operator]
        matching_ids = [
            product.id for product in self.search([]) if op(product.values, value)
        ]
        return [("id", "in", matching_ids)]
