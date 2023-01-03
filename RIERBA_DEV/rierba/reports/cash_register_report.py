# Copyright 2020, Cesar Barron
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from email.policy import default
from locale import currency
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class CashRegisterReport(models.AbstractModel):
    _name = 'report.rierba.cash_register_report'
    _description = 'Cash register report'

    def _convert_currency(self, amount, curr_id, rate_date):
        company_curr = self.env.company.currency_id
        amt = curr_id.with_context(
            date=rate_date
        ).compute(amount, company_curr)
        return amt

    # def _get_chks_summary(self, payments):
    #     ''' returns the summary of payments made by checks
    #     '''

    #     summchks = []
    #     paysbycheck = payments.filtered(
    #         lambda pay: pay.method == 'check')
    #     totchk = 0
    #     for check in paysbycheck:
    #         totchk += self._convert_currency(check.amount, check.currency_id, check.payment_date)
    #         summchks.append({
    #             'id': check.id,
    #             'bank': check.bank_id.name,
    #             'number': check.internal_number,
    #             'payer': check.payer,
    #             'amount': check.amount,
    #             'notes': check.communication,
    #             'currency': check.currency_id,
    #         })
    #     return totchk, summchks

    # def _get_deposit_summary(self, journals, date_from, date_to):
    #     ''' returns the summary of payments made by deposits
    #     '''

    #     summdepo = []
    #     deposits = self.env['account.deposit'].search([
    #         ('journal_origin_id', 'in', journals.ids),
    #         ('date', '>=', date_from),
    #         ('date', '<=', date_to),
    #     ])
    #     total_draft = 0
    #     total_confirmed = 0
    #     for dep_line in deposits.mapped('account_deposit_line_ids'):
    #         amount = self._convert_currency(dep_line.amount, dep_line.currency_id, dep_line.date)
    #         state = dep_line.account_deposit_id.state
    #         if state == 'confirmed':
    #             total_confirmed += amount
    #         else:
    #             total_draft += amount if state == 'draft' else 0
    #             continue
    #         summdepo.append({
    #             'id': dep_line.id,
    #             'journal': dep_line.journal_id,
    #             'amount': dep_line.amount,
    #             'description': dep_line.communication,
    #             'currency': dep_line.currency_id,
    #         })
    #     return total_confirmed, total_draft, summdepo

    # def _get_pay_deposit_summary(self, payments):
    #         '''
    #             returns the summary of payments made by deposit
    #         '''
    #         dep_payments = payments.filtered(
    #             lambda pay: pay.method == 'deposit'
    #         )
    #         total = 0
    #         payments = []
    #         for pay in dep_payments:
    #             total += self._convert_currency(pay.amount, pay.currency_id, pay.payment_date)
    #             payments.append({
    #                 'id': pay.id,
    #                 'journal': pay.journal_id,
    #                 'amount': pay.amount,
    #                 'description': pay.communication,
    #                 'currency': pay.currency_id,
    #             })
    #         return payments, total

    # def _get_card_summary(self, payments):
    #     ''' returns the summary of payments made by card
    #     '''

    #     summcard = []
    #     paysbycard = payments.filtered(
    #         lambda pay: pay.method == 'card')
    #     totcard = 0
    #     for cardp in paysbycard:
    #         totcard += self._convert_currency(cardp.amount, cardp.currency_id, cardp.payment_date)
    #         summcard.append({
    #             'id': cardp.id,
    #             'refnum': cardp.refnum,
    #             'cash_type': cardp.cash_type,
    #             'tjhabiente': cardp.tjhabiente,
    #             'amount': cardp.amount,
    #             'notes': cardp.communication,
    #             'currency': cardp.currency_id,
    #         })
    #     return totcard, summcard

    def _get_cash_summary(self, payments):
        ''' returns the summary of payments made by cash
        '''

        totcash = 0
        paysbycash = payments.filtered(
            lambda pay: pay.method == 'cash'
        )
        for pay in paysbycash:
            totcash += self._convert_currency(pay.amount, pay.currency_id, pay.date)
        return abs(totcash)

    def _get_denominations_summary(self, payments):
        ''' returns the summary of denominations in payments
        '''

        denomina = payments.mapped('cashdenon_ids')
        deno = {}
        for denom in denomina:
            if denom.denomination_id.id not in deno:
                deno.update({denom.denomination_id.id: {
                    'name': denom.denomination_id.name,
                    'code': denom.denomination_id.amount,
                    'qty': denom.quantity,
                    'total': (denom.denomination_id.amount * denom.quantity),
                }})
            else:
                deno[denom.denomination_id.id].update({
                    'qty': deno[denom.denomination_id.id]['qty'] + denom.quantity,
                    'total': deno[denom.denomination_id.id]['total'] + (
                        denom.denomination_id.amount * denom.quantity),
                })

        return (de for de in deno.values())

    @api.model
    def _get_report_values(self, docids, data=None):
        """Function to consult the report values.
        """
        
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        if date_from == date_to:
            raise ValidationError(_('The date from and date to must be different.'))
        journals = self.env['account.journal'].browse(
            data['form']['journal_ids'])
        journals_name = ', '.join(journals.mapped('name'))
        date_fromstr = fields.Date.from_string(date_from)
        date_tostr = fields.Date.from_string(date_to)
        payments = self.env['account.payment'].search(
            [('payment_type', '=', 'inbound'),
             ('date', '>=', date_fromstr),
             ('date', '<=', date_tostr),
             ('state', '=', 'posted'),
             ('journal_id', 'in', journals.mapped('id'))],
            order='id asc')
        
        payment_list = []
        if data['form']['number_from'] or data['form']['number_to']:
            number_dict = {pay: int(pay.name.split('-')[-1])
                           for pay in payments}
            for pay in number_dict:
                if ((number_dict[pay] >= data['form']['number_from']) and
                    (data['form']['number_to'] and
                     number_dict[pay] <= data['form']['number_to'])):
                    payment_list.append(pay)
            payments = payment_list

        totbymethod = {
            'cash': 0,
            'check': 0,
            'deposit': 0,
            'card': 0,
            'pay_deposit': 0
        }

        # totchks, summchks = self._get_chks_summary(payments)
        # totbymethod['check'] = totchks

        # totconfirmed, totdraft, summdepo = self._get_deposit_summary(journals, date_from, date_to)
        # totbymethod['deposit_draft'] = totdraft
        # totbymethod['deposit_confirmed'] = totconfirmed

        # dep_payments, total_pay_dep = self._get_pay_deposit_summary(payments)
        # totbymethod['pay_deposit'] = total_pay_dep

        # totcard, summcard = self._get_card_summary(payments)
        # totbymethod['card'] = totcard

        totcash = self._get_cash_summary(payments)
        totbymethod['cash'] = totcash

        # totbymethod['total'] = totchks + total_pay_dep + totcard + totcash

        us_curr = self.env['res.currency'].search([('name', '=', 'USD')])
        amount_us = sum(payments.mapped(lambda p: p.amount if p.currency_id == us_curr else 0))
        totbymethod['total_us'] = amount_us

        records = []
        total = 0
        for pay in payments:
            total += self._convert_currency(pay.amount, pay.currency_id, pay.date)
            reconciledto = ', '.join(pay.reconciled_invoice_ids.mapped('name'))
            terms = ', '.join(pay.reconciled_invoice_ids.invoice_payment_term_id.mapped('name'))
            fecven = []
            for fecv in pay.reconciled_invoice_ids.mapped('invoice_date_due'):
                fecven.append(fecv.strftime('%d/%m/%Y'))

            records.append({
                'id': pay.id,
                'date': pay.date,
                'number': pay.name,
                'name': pay.partner_id.name,
                'amount': pay.amount,
                'salesrep': pay.partner_id.user_id.name,
                'fecven': fecven,
                'terms': terms,
                'applied': reconciledto,
                'currency': pay.currency_id,
                'method': dict(
                    self.env['account.payment']._fields['method'].selection).get(pay.method).upper(),
            })

        # denominaciones = self._get_denominations_summary(payments)

        totdenom = data['form']['one'] + (data['form']['five'] * 5) +\
            (data['form']['ten'] * 10) + (data['form']['twenty'] * 20) +\
            (data['form']['twentyfive'] * 25) + (data['form']['fifty'] * 50) +\
            (data['form']['onehundred'] * 100) + (data['form']['twohundred'] * 200) +\
            (data['form']['fivehundred'] * 500) + (data['form']['thousand'] * 1000) +\
            (data['form']['twothousand'] * 2000)

        if not records:
            raise ValidationError(_("There is no registers between dates and"
                                    " journals selected."))
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_from': datetime.strftime(date_fromstr, '%d-%m-%Y'),
            'date_to': datetime.strftime(date_tostr, '%d-%m-%Y'),
            'number_from': data['form']['number_from'] or '-',
            'number_to': data['form']['number_to'] or '-',
            'total': total,
            'journals_name': journals_name,
            'currbase': self.env.company.currency_id,
            'us_curr': us_curr,
            'len_docs': len(records),
            'records': records,
            # 'summchks': summchks,
            # 'summdepo': summdepo,
            # 'summcard': summcard,
            # 'dep_payments': dep_payments,
            'totbymethod': totbymethod,
            'totdenom': totdenom,
            # 'denom': denominaciones,
            'one': data['form']['one'],
            'five': data['form']['five'],
            'ten': data['form']['ten'],
            'twenty': data['form']['twenty'],
            'twentyfive': data['form']['twentyfive'],
            'fifty': data['form']['fifty'],
            'onehundred': data['form']['onehundred'],
            'twohundred': data['form']['twohundred'],
            'fivehundred': data['form']['fivehundred'],
            'thousand': data['form']['thousand'],
            'twothousand': data['form']['twothousand'],
            'docs': payments,
        }
