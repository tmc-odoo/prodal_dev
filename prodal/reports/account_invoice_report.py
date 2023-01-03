from odoo import models, fields, api


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    quintales_per_ud = fields.Float(
        string='QQ',
        readonly=True
    )

    @api.model
    def _select(self):
        _field = (
            ", sum(template.quintales_per_ud * line.quantity * "
            "(CASE WHEN move.type IN ('in_invoice','out_refund','in_receipt') "
            "THEN -1 ELSE 1 END)) as quintales_per_ud"
        )
        return "%s %s" % (
            super()._select(), _field
        )
