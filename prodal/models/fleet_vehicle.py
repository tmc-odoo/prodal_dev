
from odoo import models, fields


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    driver_id = fields.Many2one(
        'hr.employee',
        string='Driver',
        help='Driver of the vehicle'
    )
    future_driver_id = fields.Many2one(
        'hr.employee',
        string='Future Driver',
        help='Next Driver of the vehicle'
    )
    assistant_ids = fields.Many2many(
        'hr.employee',
        string='Assistants'
    )
    quintal_limit = fields.Float(
        string='Quintal Limit',
    )
    plate = fields.Char(
        string='Plate',
        help='License plate number of the vehicle'
    )
    license_plate = fields.Char(
        string='Ficha',
        help='Numero de ficha del vehiculo'
    )

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    plan_to_change_car = fields.Boolean('Plan To Change Car', default=False)

    code = fields.Char(
        string='Code',
        help='Code of the employee'
    )

class HREmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    plan_to_change_car = fields.Boolean('Plan To Change Car', default=False)

class FleetVehicleAssignationLog(models.Model):
    _inherit = 'fleet.vehicle.assignation.log'

    driver_id = fields.Many2one('hr.employee', string="Driver", required=True)

class FleetVehicleOdometer(models.Model):
    _inherit = 'fleet.vehicle.odometer'

    driver_id = fields.Many2one('hr.employee', related="vehicle_id.driver_id", string="Driver", readonly=False)

class FleetVehicleLogFuel(models.Model):
    _inherit = "fleet.vehicle.log.fuel"

    purchaser_id = fields.Many2one('hr.employee', 'Purchaser')

class FleetVehicleLogServices(models.Model):
    _inherit = "fleet.vehicle.log.services"

    purchaser_id = fields.Many2one('hr.employee', 'Purchaser')
