from odoo import models, fields


class PickingChangeOperation(models.TransientModel):
    _name = "picking.change.operation"
    _description = "Picking change operation"

    picking_type_id = fields.Many2one('stock.picking.type', required='True')

    def change_picking_type(self):
        active_id = self._context.get("active_id")
        picking_id = self.env["stock.picking"].browse(active_id)
        picking_id.action_cancel()
        picking_id.action_back_to_draft()
        picking_id.write({'picking_type_id': self.picking_type_id.id})
        picking_id.onchange_picking_type()
        picking_id.action_confirm()
