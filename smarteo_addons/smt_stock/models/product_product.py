from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"
    _description = "Product Variant"

    values = fields.Float(string="Total Value", compute="_compute_values", store=False)

    def _compute_values(self):
        for record in self:
            record.values = record.qty_available * record.standard_price
