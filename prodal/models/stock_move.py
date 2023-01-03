from odoo import models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_done_total_batch = fields.Float(
        string='Quantity Done',
        help='Total quantity done in batch',
        compute='_compute_qty_done_total_batch'
    )

    is_offer = fields.Boolean(
        'Is Offer',
        related='sale_line_id.is_offer',
        readonly=True
    )

    def _compute_qty_done_total_batch(self):
        picking_ids = self.picking_id.batch_id.picking_ids.ids
        for move in self:
            domain = [
                ('picking_id', 'in', picking_ids),
                ('product_id', '=', move.product_id.id)
            ]
            move.qty_done_total_batch = sum(move.search(domain).mapped('quantity_done'))
