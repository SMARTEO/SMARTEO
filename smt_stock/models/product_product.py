from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    values = fields.Float(compute="_compute_values", string="Valeur total", store=False)

    def _compute_values(self):
        for record in self:
            record.values = record.qty_available * record.standard_price
