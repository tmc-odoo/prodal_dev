from odoo import models


class ReportProdalLoadSquaring(models.AbstractModel):
    _name = 'prodal.report_prodal_load_squaring'
    _description = 'Stock Picking Batch Prodal report'

    def get_lines(self, batch):
        lines = []
        invoices = batch.invoice_ids
        for inv in invoices:
            rev_inv = inv.reversal_move_id
            rev_amount = sum(rev_inv.mapped('amount_total')) if rev_inv else 0
            data = {
                'number': inv.name,
                'amount': inv.amount_total,
                'total_amount': inv.amount_total - rev_amount,
                'payment_term': inv.invoice_payment_term_id.name,
                'client_name': inv.partner_id.name,
                'rev_number': rev_inv[0].name if rev_inv else '',
                'rev_amount': rev_amount,
            }
            lines.append(data)
        deliver_cash = sum(invoices.filtered('invoice_payment_term_id.is_cash').mapped('amount_total'))
        return lines, deliver_cash
