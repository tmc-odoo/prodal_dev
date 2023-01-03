from odoo import models, api

class AccountInvoice(models.Model):
    _name = "prodal"
    _inherit = 'account.invoice.report'

    @api.model
    def _where(self):
        return '''
            WHERE move.type IN ('out_invoice', 'out_refund', 'out_receipt')
                AND line.account_id IS NOT NULL
                AND NOT line.exclude_from_invoice_tab'''
