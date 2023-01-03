from odoo import models, fields


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    sale_discount = fields.Float(
        string='Sale Discount (%)',
        help="Discount to be applied in sale order lines discount field.",
        digits='Sale Discount',
    )
