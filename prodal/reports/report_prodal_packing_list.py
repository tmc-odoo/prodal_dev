
from itertools import groupby
from odoo import api, models


class ReportProdalPackingList(models.AbstractModel):
    _name = 'prodal.report_prodal_packing_list'
    _description = 'Stock Picking Prodal report'

    def total_line_func(self, move_line):
        return move_line.sale_line_id.price_unit * move_line.quantity_done

    def get_picking_groups(self, batch, group):
        picking_groups = []
        picking_obj = self.env['stock.picking']
        group_objects = {
            'user': (lambda sp: sp.user_id.id, self.env['res.users']),
            'partner': (lambda sp: sp.partner_id.id, self.env['res.partner'])
        }
        group_func, group_obj = group_objects[group]
        pickings = batch.mapped('picking_ids').sorted(key=group_func)
        for key, grp in groupby(pickings, group_func):
            ids = [pick.id for pick in grp]
            picking_groups.append(
                (group_obj.browse(key), picking_obj.browse(ids))
            )
        return picking_groups

    def get_summary_line(self, line, qty, total):
        return {
            'code': line.product_id.default_code,
            'product': line.product_id.name,
            'qty': qty,
            'uom': line.product_uom.name,
            'total': total
        }

    @api.model
    def get_picking_summary(self, stock_pickings=None, batch=None):
        summary_lines = []
        func_product_id = lambda l: l.product_id.id
        stock_pickings = batch.mapped('picking_ids') if batch else stock_pickings
        if not stock_pickings:
            return summary_lines

        data = stock_pickings.mapped('move_lines').sorted(key=func_product_id)
        for dummy, group in groupby(data, func_product_id):
            group_list = list(group)
            line = group_list[0]
            qty = sum(map(lambda ml: ml.quantity_done, group_list))
            total = sum(map(self.total_line_func, group_list))
            summary_lines.append(
                self.get_summary_line(line, qty, total)
            )
        return summary_lines

    def get_general_load_data(self, batch):
        pickings = batch.mapped('picking_ids')
        lines = pickings.mapped('move_lines')
        clients = pickings.mapped('partner_id')
        total_quintals = sum(
            lines.mapped(lambda l: l.product_id.quintales_per_ud * l.quantity_done)
        )
        return {
            'quintals': total_quintals,
            'items_qty': sum(lines.mapped('quantity_done')),
            'clients': len(clients)
        }

    def get_total_price(self, pickings):
        prices = pickings.mapped('move_lines').mapped(self.total_line_func)
        return sum(prices)
