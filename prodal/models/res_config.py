from odoo import models, fields

class ResCompany(models.Model):
    _inherit='res.company'

    check_report_payment_method_ids = fields.Many2many('account.payment.method')


class ResConfig(models.TransientModel):
    _inherit='res.config.settings'

    check_report_payment_method_ids = fields.Many2many(
        'account.payment.method',
        help='Only print moves with these payment methods in the journal report when the payment check option is selected.',
        related='company_id.check_report_payment_method_ids',
        readonly=False
    )
