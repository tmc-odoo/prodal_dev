from odoo import models, fields, api,_
from odoo.exceptions import UserError


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    rierba_bl = fields.Many2one("rierba_bl.rierba_bl")