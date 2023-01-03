from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_type = fields.Selection(
        string='Partner Type',
        selection=[
            ('institution', 'Institution'),
            ('insurence', 'Insurance carrier'),
            ('pacient', 'Pacient'),
            ('contact', 'Contact')
        ],
        default="pacient",
        help="Diagnosis partner clasification"
    )
    affiliate_number = fields.Char(
        string='Affiliate number',
        help="Insurance affiliation number"
    )
    insurance_policy = fields.Char(
        string='Insurance policy',
        help="partner insurance policy"
    )
    db_external_id = fields.Integer(
        help="Technical field. Save external ID other Databases")
    code_pss = fields.Char("Code PSS")
    insurance_account_id = fields.Many2one("account.account")
    insurance_account_receivable_id = fields.Many2one(
        "account.account",
        domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]")
