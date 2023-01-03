from odoo import models, fields

class PaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    is_cash = fields.Boolean(
        'Is Cash',
        help='If checked, invoices with this payment term will be taken into account for the "cash to deliver" field in the squaring load report',
    )
