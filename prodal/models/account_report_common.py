from odoo import fields, models, api


class AccountCommonReport(models.TransientModel):
    _inherit = "account.print.journal"

    journal_ids = fields.Many2many('account.journal', required=False, default=False)
    account_ids = fields.Many2many("account.account", readonly=False)
    payment_check = fields.Boolean('Payment Check')

    @api.onchange('company_id')
    def _onchange_company_id(self):
        for rec in self:
            rec.journal_ids = False

    def _build_contexts(self, data):
        res = super()._build_contexts(data)
        res["account_ids"] = self.account_ids.ids
        res["from_audit_report"] = True
        return res

    def pre_print_report(self, data):
        super().pre_print_report(data)
        data['form'].update({
            'account_ids': self.account_ids.ids,
            'payment_check': self.payment_check
        })
        return data
