from odoo import _, models, fields, api
from odoo.exceptions import ValidationError


class Employee(models.Model):
    """
    Fields adds in Employee
    """
    _inherit = "hr.employee"


    @api.onchange('passport_id')
    def onchange_passport_id(self):
        for record in self:
            address_home_id = self.env['res.partner'].search([('vat', '=', record.passport_id)], limit=1)
            record.address_home_id = address_home_id
