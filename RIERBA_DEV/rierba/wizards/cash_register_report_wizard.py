# Copyright 2020, Cesar Barron
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from odoo import api, fields, models


class CashRegisterReportWizard(models.TransientModel):
    _name = "cash.register.report.wizard"
    _description = "Cash Register Report Wizard"

    journal_ids = fields.Many2many(
        'account.journal', string='Journals', required=True,
        domain=[('type', '=', 'cash')],
        help='Journals to filtered account payments')
    date_from = fields.Date(
        string='Start Date', required=True,
        help='Date from which the account payments will be consulted')
    date_to = fields.Date(
        string='End Date', required=True,
        help='Date to which the account payments will be consulted')
    number_from = fields.Integer(
        help='Number from which the account payments will be consulted.')
    number_to = fields.Integer(
        help='Number to which the account payments will be consulted')

    one = fields.Integer(
        string='One',
        help='Quantity of denomination One'
    )

    five = fields.Integer(
        string='Five',
        help='Quantity of denomination Five'
    )

    ten = fields.Integer(
        string='Ten',
        help='Quantity of denomination Ten'
    )

    twenty = fields.Integer(
        string='Twenty',
        help='Quantity of denomination Twenty'
    )

    twentyfive = fields.Integer(
        string='Twenty Five',
        help='Quantity of denomination Twenty five'
    )

    fifty = fields.Integer(
        string='Fifty',
        help='Quantity of denomination Fifty'
    )

    onehundred = fields.Integer(
        string='One Hundred',
        help='Quantity of denomination One Hundred'
    )

    twohundred = fields.Integer(
        string='Two Hundred',
        help='Quantity of denomination Two Hundred'
    )

    fivehundred = fields.Integer(
        string='Five Hundred',
        help='Quantity of denomination Five Hundred'
    )

    thousand = fields.Integer(
        string='Thousand',
        help='Quantity of denomination Thousand'
    )

    twothousand = fields.Integer(
        string='Two Thousand',
        help='Quantity of denomination Two Thousand'
    )

    @api.model
    def default_get(self, _fields):
        """Inherit function default_get to set the default values in wizard.
        Args:
            _fields: Fields in wizard
        Returns:
            Dict of wizard fields with values.
        """
        res = super().default_get(_fields)
        res['date_from'] = datetime.now()
        res['date_to'] = datetime.now()
        return res

    def _build_contexts(self, data):
        """Build context to use in wizard.
        Args:
            data: Dict of data wizard
        Returns:
            Dict of context wizard.
        """
        result = {}
        result['journal_ids'] = ('journal_ids' in data['form'] and
                                 data['form']['journal_ids'] or False)
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['number_from'] = data['form']['number_from'] or '-'
        result['number_to'] = data['form']['number_to'] or '-'
        return result

    def get_report(self):
        """Call when button 'Print' clicked.

        Returns:
            Action to construct the report parameters.
        """
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'journal_ids',
                                  'number_from', 'number_to', 'one', 'five',
                                  'ten', 'twenty', 'twentyfive', 'fifty',
                                  'onehundred', 'twohundred', 'fivehundred',
                                  'thousand', 'twothousand'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = (
            dict(used_context, lang=self.env.context.get('lang') or 'en_US'))

        return self.env.ref(
            'rierba.action_cash_register_report').report_action(
                self, data=data)
