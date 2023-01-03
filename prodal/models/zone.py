
from odoo import models, fields

class Zone(models.Model):
    _name = 'prodal.zone'

    name = fields.Char(
        string='Name',
        help='Name of the zone'
    )
