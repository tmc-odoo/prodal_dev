from odoo import api
from . import report_prodal_packing_list as report


class ReportLoadTruck(report.ReportProdalPackingList):
    _name = 'prodal.report_load_truck'
    _description = 'Report transfer truck route'

    @api.model
    def get_picking_total(self, picking):
        total_lines = picking.move_lines.mapped(
            lambda l: l.product_id.list_price
            * l.quantity_done
        )
        return sum(total_lines)

    def get_summary_line(self, line, qty, total):
        sum_line = super().get_summary_line(line, qty, total)
        sum_line['quintals'] = line.product_id.quintales_per_ud * qty
        sum_line['warehouse'] = line.warehouse_id.code
        return sum_line
