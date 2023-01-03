from odoo import models, fields

class AccountMove(models.Model):
    _inherit='account.move'

    is_transit = fields.Boolean('Is Transit')


class AccountMoveLine(models.Model):
    _inherit="account.move.line"

    external_name = fields.Char(related="product_id.external_name")


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    method = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('check', 'Check'),
        ('deposit', 'Deposit'),
    ],
        string='Type method',
        default='cash',
        help="The 'Internal Type' is used for features available on "
        "Payments")
