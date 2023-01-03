from odoo import models, fields

class CheckReportConfig(models.Model):
    _inherit = "check.report.config"

    check_date_top = fields.Float("Margen superior de fecha en pie", default=50)
    check_date_left = fields.Float("Margen izquierdo de fecha en pie", default=50)

    show_description = fields.Boolean(
        'Show Description',
        help='If checked the description section is displayed on the check report'
    )

    description_top = fields.Float(
        string='Description Top Margin',
        help='Margin top of description section in mm',
        default=20
    )

    description_left = fields.Float(
        string='Description left Margin',
        help='Margin left of description section in mm',
        default=20
    )    
