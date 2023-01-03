from datetime import timedelta
from psycopg2 import sql
from odoo import models, api, fields, _
from odoo.osv import expression
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

def get_mock_object(vals):
    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)
        def __getattr__(self, attr):
            if attr not in self.__dict__:
                return False
            return super().__getattr__(attr)
    return Struct(**vals)


class ReportJournal(models.AbstractModel):
    _inherit = 'report.account.report_journal'

    @api.model
    def _get_report_values(self, docids, data=None):
        res = super()._get_report_values(docids, data=data)
        journals = data['form']['journal_ids']
        account_ids = data['form']['account_ids']
        date_from = fields.Date.from_string(data['form']['date_from']) - timedelta(days=1)
        res['balance'] = self.set_init_balance_journal(journals, date_from, data['form']['amount_currency'])
        if not journals and account_ids:
            res.update(self.set_only_account_lines(data))
        return res

    def set_init_balance_journal(self, journals, date_from, amount_currency=False):
        res = {}
        fiscalyear = self.env.company.compute_fiscalyear_dates(date_from)
        for journal in journals:
            res.setdefault(journal, 0.0)
            domain = [
                ('display_type', 'not in', ('line_section', 'line_note')),
                ('move_id.state', '=', 'posted'),
                ('journal_id', '=', journal),
                ('date', '<=', date_from),
            ]
            domain2 = [
                ('move_id.state', '=', 'posted'),
                ('move_id.journal_id', '=', journal),
                ('date', "<=", date_from),
            ]
            domain = expression.OR([domain, domain2])
            amls = self.env['account.move.line'].search(domain)
            if amount_currency:
                balance = sum(amls.mapped('amount_currency'))
            else:
                balance = sum(amls.mapped('balance'))
            res[journal] = balance
        return res

    def set_init_balance_accounts(self, accounts, date_from, amount_currency=False):
        domain = [
            ('display_type', 'not in', ('line_section', 'line_note')),
            ('move_id.state', '=', 'posted'),
            ('account_id', 'in', accounts),
            ('date', '<=', date_from),
        ]
        amls = self.env['account.move.line'].search(domain)
        if amount_currency:
            return sum(amls.mapped('amount_currency'))
        return sum(amls.mapped('balance'))

    def set_only_account_lines(self, data):
        target_move = data['form'].get('target_move', 'all')
        sort_selection = data['form'].get('sort_selection', 'date')
        account_ids = data['form']['account_ids']
        date_from = fields.Date.from_string(data['form']['date_from']) - timedelta(days=1)
        journals = self.env["account.journal"].search([])
        docs = get_mock_object({
            "name": _("General"),
            "type": "banck",
            "ids": journals.ids,
            "id": 1,
            "env": self.env,
            "context": self._context
        })
        lines = {
            1: self.lines(target_move, journals.ids, sort_selection, data)
        }
        return {
            "docs": [docs],
            "lines": lines,
            "balance": {1: self.set_init_balance_accounts(
                account_ids, date_from, data['form']['amount_currency'])}
        }

    def lines(self, target_move, journal_ids, sort_selection, data):
        if not data['form'].get('payment_check', False):
            return  super().lines(target_move, journal_ids, sort_selection, data)
        return self.get_payment_out_lines(data, journal_ids)

    def get_payment_out_lines(self, data, journal_ids):
        if isinstance(journal_ids, int):
            journal_ids = (journal_ids,)
        accounts = tuple(data['form']['account_ids'])
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        sort_selection = data['form'].get('sort_selection', 'date')
        pay_methods = tuple(self.env.company.check_report_payment_method_ids.ids)

        _where_condition = (
            f"""
                pay.payment_type = 'outbound'
                AND aml.journal_id IN %(journal_ids)s
                {'AND (aml.date <= %(date_to)s) ' if date_to else ''}
                {'AND (aml.date >= %(date_from)s) ' if date_from else ''}
                {'AND pay.payment_method_id IN %(pay_methods)s ' if pay_methods else ''}
                {'AND aml.account_id IN %(accounts)s ' if accounts else ''}
            """
        )
        query = sql.SQL(
            f"""
            SELECT aml.id id, aml.{{order_field}} as {{order_field}}
            FROM
                account_move_line aml
                INNER JOIN account_account acc ON aml.account_id = acc.id
                INNER JOIN account_payment pay ON aml.payment_id = pay.id
            WHERE {_where_condition}
            UNION
            SELECT
                aml.id id, aml.{{order_field}} as {{order_field}}
            FROM
                account_move_line aml
                INNER JOIN account_move move ON aml.move_id = move.id
                INNER JOIN account_payment pay ON pay.move_cancellation_id = move.id
            WHERE {_where_condition}
            ORDER BY {{order_field}};
            """
        ).format(order_field=sql.Identifier(sort_selection))
        params = {
            'date_to': date_to,
            'date_from': date_from,
            'pay_methods': pay_methods,
            'accounts': accounts,
            'journal_ids': journal_ids
        }
        self.env.cr.execute(query, params)
        ids = (x[0] for x in self.env.cr.fetchall())
        return self.env['account.move.line'].browse(ids)
