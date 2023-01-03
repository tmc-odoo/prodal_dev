from odoo import models, fields


class DiagnosisReferrer(models.Model):
    _name = "diagnosis.referrer"
    _description = "Diagnosis Referrer"

    name = fields.Char(
        string='Referrer',
        required=True,
    )
    db_external_id = fields.Integer(
        help="Technical field. Save external ID other Databases")
