from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_weight = fields.Float('Weight')

    price_per_weight = fields.Float('Price per Weight')

    sold_by_weight = fields.Boolean(related='product_id.sold_by_weight')

    @api.onchange('product_weight', 'price_per_weight', 'quantity')
    def _onchange_weight_fields(self):
        for line in self.filtered(lambda l: l.sold_by_weight):
            line.price_unit = (line.price_per_weight * line.product_weight) / line.quantity
