from odoo import fields, models


class HrEducationLevel(models.Model):
    _inherit = 'hr.education.level'
    _order = "sequence asc"


    sequence = fields.Integer()
