from __future__ import division
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_discount = fields.Float(
        related="pricelist_id.sale_discount"
    )

    zone_id = fields.Many2one(
        'prodal.zone',
        string='Zone',
    )

    notes = fields.Char(
        string='Notes',
        help='Sale order notes'
    )

    blocked = fields.Boolean(
        string="Blocked",
        store=True,
        readonly=False,
        compute="_compute_blocked",
        help="This field is set to true if order line is changed"
    )

    total_discount = fields.Float(
        string ="Total discount",
        readonly=True,
        compute='_compute_total_discount'
    )

    total_no_discount = fields.Float(string="Total No discount",
        readonly=True,
        compute='_compute_sub_total')

    @api.depends('order_line.price_unit', 'order_line.discount')
    def _compute_blocked(self):
        for rec in self:
            lines_is_block = self.order_line.filtered(
                lambda x: (x.product_id.list_price != x.price_unit) or x.discount)
            if lines_is_block:
                rec.blocked = True

    def _compute_total_discount(self):
        disc = 0
        for line in self.order_line:
            disc += (line.discount/100) * line.price_unit * line.product_uom_qty
        self.total_discount = disc

    def _compute_sub_total(self):
        total = 0
        for line in self.order_line:
            total += line.product_uom_qty * line.price_unit
        self.total_no_discount = total

    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):
        for sale in self:
            sale.order_line.update({
                'discount': sale.pricelist_id and sale.pricelist_id.sale_discount or 0.0
            })


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount = fields.Float(
        digits="Sale Discount"
    )
