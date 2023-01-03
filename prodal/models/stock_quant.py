from odoo import fields, models, api


class StockQuant(models.Model):
    _inherit = "stock.quant"

    available_difference = fields.Float(string="Difference", readonly=True,
            compute='_compute_available_difference')
    committed_qty = fields.Float("Committed", compute="_compute_committed_qty")
    stock_max = fields.Float(string="Stock Max", compute="_compute_stock_max")
    stock_min = fields.Float(string="Stock Min", compute="_compute_stock_min")
    qty_to_produce = fields.Float(string="Qty. to Produce", compute="_compute_qty_to_produce")
    categ_id = fields.Many2one('product.category', string='Product Category',
            readonly=True, compute="_compute_categ_id", store=True)


    @api.depends("quantity", "committed_qty")
    def _compute_available_difference(self):
        for product in self:
            product.available_difference = product.quantity - product.committed_qty

    @api.depends("product_id")
    def _compute_committed_qty(self):
        for rec in self:
            rec.committed_qty = rec.get_committed_qty()

    def get_committed_qty(self):
        domain = [
            ('product_id', '=', self.product_id.id),
            ('picking_id.state', 'in', ['assigned', 'confirmed']),
            ('picking_code', '=', 'outgoing'),
            ('location_id','=', self.location_id.id)
        ]
        moves = self.env["stock.move"].search(domain)
        return sum(moves.mapped("product_uom_qty"))

    @api.depends('product_id')
    def _compute_categ_id(self):
        for product in self:
            product.categ_id = product.product_id.categ_id

    @api.depends('product_id')
    def _compute_stock_max(self):
        for product in self:
            product.stock_max = max(product.mapped('product_id.orderpoint_ids.product_max_qty') or [0])

    @api.depends('product_id')
    def _compute_stock_min(self):
        for product in self:
            product.stock_min = min(product.mapped('product_id.orderpoint_ids.product_min_qty') or [0])

    @api.depends('available_difference','stock_max')
    def _compute_qty_to_produce(self):
        for prdt in self:
            prdt.qty_to_produce = 0
            if  prdt.available_difference < prdt.stock_max:
                prdt.qty_to_produce = prdt.stock_max - prdt.available_difference
