from odoo import fields, models


class ProdalInvoiceListWizard(models.TransientModel):
    _name = "prodal.invoice.list.wizard"
    _description = "Invoice List Wizard"

    user_ids = fields.Many2many(
        'res.users',
        string='Sales Rep')

    date_from = fields.Date(
        required=True,
        string='Start Date')

    date_to = fields.Date(
        required=True,
        string='End Date')

    def print_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'user_ids'])[0]
        return self.env.ref(
            'prodal.action_report_prodal_invoice_list').report_action(
            self, data=data)
