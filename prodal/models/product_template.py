from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    quintales_per_ud = fields.Float(
        string='Quintales x UD',
    )

    weight_factor = fields.Float(
        string='Weight Factor',
        help='Represents the weight factor of the product used in the calculation of the unload price.'
    )

    is_unload_product = fields.Boolean(
        'Is unload product',
        related='uom_id.is_unload_unit',
        help='If checked, moves with this product are factored in when computing the unload price of a stock picking.',
        readonly=True
    )
    quantity_pound = fields.Float(
        "Quantity Pounds", compute="_compute_quantity_pound")

    def _compute_quantity_pound(self):
        for rec in self:
            rec.quantity_pound = rec.quintales_per_ud * 100

class ProductCategory(models.Model):
    _inherit = 'product.category'

    shown_name = fields.Char('Shown name')
