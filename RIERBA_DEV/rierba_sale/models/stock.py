from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_weight = fields.Float('Weight')

    sold_by_weight = fields.Boolean(
        related='product_id.sold_by_weight'
    )


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        move_fields = super()._get_custom_move_fields()
        move_fields.append('product_weight')
        return move_fields
