from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"
    
    external_name = fields.Char()
    required_cost_confirmation = fields.Boolean()

    def _compute_display_name(self):
        super()._compute_display_name()
        for record in self:
            if not record.external_name:
                continue
            record.display_name = record.external_name
