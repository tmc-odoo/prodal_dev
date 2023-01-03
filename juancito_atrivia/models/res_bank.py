from odoo import _, models, fields, api
from odoo.exceptions import ValidationError


class Bank(models.Model):

    _inherit = 'res.bank'
    _order = "sequence asc"


    sequence = fields.Integer()


class ResPartnerBank(models.Model):

    _inherit = 'res.partner.bank'

    bank_account_type = fields.Selection([
        ('1', 'Current account'),
        ('2', 'Savings account'),
        ('3', 'Credit Card'),
        ('4', 'Loans'),
        ('5', 'Check'),
        ('7', 'Debit Card'),
    ], default='2',
        help="The type is used for txt payroll.")
