from itertools import groupby
from odoo import models, api


class ReportInvoiceList(models.AbstractModel):
    _name = 'report.prodal.report_prodal_invoice_document'
    _description = 'Report Invoice List'

    @api.model
    def _get_report_values(self, docids, data=None):
        invoices = self.env['account.move'].search([
            ('partner_id.user_id', 'in', data['form']['user_ids']),
            ('invoice_date', '>=', data['form']['date_from']),
            ('invoice_date', '<=', data['form']['date_to']),
            ('invoice_payment_state', '!=', 'paid'),
            ('invoice_payment_term_id.credit', '=', True),
            ('type', 'in', ('out_invoice', 'out_refund', 'out_receipt')),
            ('state', '=', 'posted'),
        ]).sorted(key=lambda i: i.date).sorted(key=lambda i: i.partner_id.name)

        return {
            'data': data,
            'inv_groups': self.get_invoice_groups(invoices, group_field=['partner_id', 'user_id']),
            'currency': self.env.user.company_id.currency_id
        }

    def get_invoice_groups(self, invoices, group_field):
        if not invoices:
            return []
        inv_groups = []
        group_func = lambda i: i[group_field[0]]
        group_obj = invoices[0][group_field[0]].browse()
        if group_field == ['partner_id', 'user_id']:
            group_func = lambda i: i[group_field[0]][group_field[1]].id
            group_obj = invoices[0][group_field[0]][group_field[1]].browse()
        move_obj = self.env['account.move']

        invoices = invoices.sorted(group_func)

        for key, grp in groupby(invoices, group_func):
            ids = [inv.id for inv in grp]
            inv_list = move_obj.browse(ids)
            if group_field == ['partner_id', 'user_id']:
                inv_list = self.get_invoice_groups(inv_list, group_field=['partner_id'])
            inv_groups.append(
                (group_obj.browse(key), inv_list)
            )
        return inv_groups
