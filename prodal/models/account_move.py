from __future__ import division
from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    driver_id = fields.Many2one(
        'hr.employee',
        string='Driver',
        help="Related driver"
    )

    total_discount = fields.Float(
        string ="Total discount",
        readonly=True,
        compute='_compute_total_discount'
    )

    unload_discount = fields.Float(
        string='Unload discount',
        compute='_compute_unload_discount',
    )

    total_no_discount = fields.Float(
        string="Total No discount",
        readonly=True,
        compute='_compute_sub_total')

    def _compute_total_discount(self):
        disc = 0
        for line in self.invoice_line_ids:
            disc += (line.discount / 100) * line.price_unit * line.quantity
        self.total_discount = disc

    def _compute_unload_discount(self):
        for inv in self:
            pickings = self.env['stock.picking'].search([
                ('origin', '=', inv.invoice_origin),
                ('state', '=', 'done'),
                ('unload_price', '>', 0)])

            inv.unload_discount = sum(pickings.mapped('unload_price'))

    def _compute_sub_total(self):
        total = 0
        for line in self.invoice_line_ids:
            total += line.price_unit * line.quantity
        self.total_no_discount = total

    def post(self):
        if not self.env.user.has_group('prodal.group_invoice_menu_user'):
            return super().post()
        self.env.su = True
        res = super().post()
        self.env.su = False
        return res


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    move_driver_id = fields.Many2one(
        "hr.employee",
        string="Driver",
        help="Move related driver",
        related="move_id.driver_id",
        readonly=True
    )

    qq = fields.Float(
        string='QQ',
        digits="Product Unit of Measure",
        help="Quintal",
        compute="_compute_qq",
    )

    @api.depends('product_id', 'quantity')
    def _compute_qq(self):
        for line in self:
            line.qq = line.product_id.quintales_per_ud * line.quantity

    @api.model
    def _query_get(self, domain=None):
        ctx = dict(self._context)
        if ctx.get("from_audit_report"):
            account_ids = self.env["account.account"].browse(ctx.get("account_ids"))
            ctx.update({"account_ids": account_ids})
        return super(AccountMoveLine, self.with_context(ctx))._query_get(domain=domain)
