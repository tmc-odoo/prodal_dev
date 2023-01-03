from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    quintales_per_ud = fields.Float(
        string='QQ',
        readonly=True
    )

    def _query(
        self, with_clause='', fields_dict='', groupby='',
        from_clause=''
):
        fields_dict = {}
        fields_dict['quintales_per_ud'] = """
        , sum(t.quintales_per_ud * l.product_uom_qty) as quintales_per_ud
        """

        return super()._query(with_clause, fields_dict, groupby, from_clause)
