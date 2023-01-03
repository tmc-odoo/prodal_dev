from odoo import models, fields, api,_
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"


    factory_ready = fields.Date(string='factory ready')
    etd = fields.Date(string='ETD')
    date_planned = fields.Datetime(string='ETA',
                                   index=True,
                                   copy=False,
                                   compute='_compute_date_planned',
                                   store=True,
                                   readonly=False,
        help="Delivery date promised by vendor. This date is used to determine expected arrival of products.")
    rierba_bl_id = fields.Many2one("rierba_bl.rierba_bl")

    state = fields.Selection(selection_add=[('produ','Factory Production'),
                                             ('petai','Retained by Credit hold'),
                                             ('ready','factory ready'),
                                             ('coordinating','coordinating Booking'),
                                             ('transitmiami','Transit MIAMI'),
                                             ('warehouse','warehouse MIAMI'),
                                             ('transitdr','transit to DR'),
                                             ('customs','in Dominican customs'),
                                             ('france','France warehouse'),
                                             ('duarte','duarte warehouse'),
                                             ('account','sent to accounting')], string='Status',
                                                                                index=True,
                                                                                copy=False,
                                                                                default='draft',
                                                                                tracking=True)

    shipment = fields.Selection([
        ('aeri', 'aerial'),
        ('mari', 'maritime')],
        string='shipment')


    def action_read_purchase(self):
        self.ensure_one()
        return {
            'name': self.display_name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'res_id': self.id,
        }

    def create_bl_group(self):

        context = []
        bl_comparin = self[0].BL
        for line in self:
            if bl_comparin == line.BL:
                context.append((4,line.id))
                bl_comparin = line.BL
            else:
                raise UserError(_('all the orders should have the same BL'))
        return {
            'name': _('BL group'),
            'view_mode': 'form',
            'view_id': self.env.ref('rierba_bl.rierba_bl_form').id,
            'res_model': 'rierba_bl.rierba_bl',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {
                'default_name': 'test',
                'default_purchase_ids': context
            }}
        

    def add_bl_group(self):

        context = []
        context += [(4, line.id) for line in self]
        return {
            'name': _('add BL group'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rierba_bl.addbl',
            'target': 'new',
            'context': {
            'default_purchase_ids': context
            }
        }
        