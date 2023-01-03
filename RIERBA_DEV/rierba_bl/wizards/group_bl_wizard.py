from odoo import api, fields, models,_
from odoo.exceptions import UserError


class Rierba_Bl_Addbl(models.TransientModel):
    _name = "rierba_bl.addbl"

    group_bl_id = fields.Many2one('rierba_bl.rierba_bl',string="BL group")
    purchase_ids = fields.Many2many("purchase.order")

    def action_add_fields(self):
        if not self.group_bl_id:
            raise UserError(_('you must select a BL group'))
        for purcha in self.purchase_ids:
            if self.group_bl_id.purchase_ids[0].BL == purcha.BL:
                self.group_bl_id.purchase_ids = [(4,purcha.id)]
            else:
                raise UserError(_('all the orders should have the same BL'))

        return {
            'name': 'BL gruop',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rierba_bl.rierba_bl',
            'res_id': self.group_bl_id.id,
        }
