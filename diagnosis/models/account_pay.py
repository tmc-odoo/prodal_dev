from odoo import models, fields, api, _
from odoo.tools.misc import  formatLang, format_date

class account_payment(models.Model):
    _inherit = "account.payment"
    
    new_amount_in_words = fields.Char(compute='conver_amount_words')

    def _check_build_page_info(self, i, p):
        multi_stub = self.company_id.account_check_printing_multi_stub
        check_layout = self.company_id.account_check_printing_layout
        if check_layout == 'l10n_do_check_printing.action_print_custom_report':
            return {
                'sequence_number': self.check_number,
                'manual_sequencing': self.journal_id.check_manual_sequencing,
                'date': format_date(self.env, self.date),
                'partner_id': self.partner_id,
                'partner_name': self.check_name,
                'currency': self.currency_id,
                'state': self.state,
                'amount': formatLang(self.env, self.amount, currency_obj=self.currency_id) if i == 0 else 'VOID',
                'amount_in_word': self.new_amount_in_words,
                'memo': self.ref,
                'stub_cropped': not multi_stub and len(self.move_id._get_reconciled_invoices()) > 9,
                # If the payment does not reference an invoice, there is no stub line to display
                'stub_lines': p,
            
            }
        return super(account_payment, self)._check_build_page_info(i, p)

    @api.depends('payment_method_id', 'currency_id', 'amount', 'new_amount_in_words')
    def conver_amount_words(self):

        self.ensure_one()
        currency_type = ''

        amount_i, amount_d = divmod(self.amount, 1)
        amount_d = round(amount_d, 2)
        amount_d = int(round(amount_d * 100, 2))

        words = self.currency_id.with_context(lang='es_ES').amount_to_text(amount_i)
        self.new_amount_in_words = '%(words)s con %(amount_d)02d/100 %(currency_type)s' % {
            'words': words,
            'amount_d': amount_d,
            'currency_type': currency_type,
        }                    
        

class AccountJournal(models.Model):
    _inherit = "account.journal"
    _name = "account.journal"

    check_layout = fields.Many2one(
        "check.report.config", string="Plantilla de cheque", required=False,
        help="Seleccione el formato que corresponde al papel "
        "de verificación va a imprimir sus cheques en.\n"
        "Para desactivar la función de impresión, seleccione 'Ninguno'.")

