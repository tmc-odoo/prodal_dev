from odoo import models, fields

class UoM(models.Model):
    _inherit = 'uom.uom'

    is_unload_unit = fields.Boolean(
        'Is unload unit',
        help="If checked, moves with products that have this uom are factored in when computing the unload price of a stock picking."
    )
