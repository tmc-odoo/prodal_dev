from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json

class PurchaseOrder(models.Model):
    _inherit = "stock.landed.cost"


    rierba_bl = fields.Many2one("rierba_bl.rierba_bl")


    vendor_bill_id_domain = fields.Char(compute="_compute_vendor_bill_id_domain", readonly=True, store=False,)

    # @api.multi
    @api.depends('rierba_bl')
    def _compute_vendor_bill_id_domain(self):
        for rec in self:
            rec.vendor_bill_id_domain = json.dumps([('rierba_bl', '=', rec.rierba_bl.id)])
