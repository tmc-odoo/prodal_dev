from odoo import models, fields


class InsuranceCloseReason(models.Model):
    _name = "insurance.close.reason"
    _description = "Close reason"

    name = fields.Char(required=True)
