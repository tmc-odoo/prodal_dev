from odoo import fields, models, tools


class MRPStockMoveLine(models.Model):
    _name = "mrp.stock.move.line"
    _description = "MRP view move lines"
    _auto = False

    date = fields.Date(readonly=True)
    reference = fields.Char(readonly=True)
    product_id = fields.Many2one("product.product", readonly=True)
    product_ctg_id = fields.Many2one(
        "product.category", string="Product category", readonly=True)
    qty_done = fields.Float("Quantity done", readonly=True)
    qty_qq = fields.Float("Quantity QQ", readonly=True)
    date_planned_start = fields.Datetime(readonly=True)
    mrp_state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('progress', 'In Progress'),
        ('planned', 'Planned'),
        ('to_close', 'To Close'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='State')

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
            )
        """ %(self._table, self._select(), self._from()))

    def _select(self):
        return """
            SELECT id, date, reference, product_id, product_ctg_id, qty_done, qty_qq, date_planned_start, mrp_state
        """

    def _from(self):
        return """
        FROM (
             SELECT
                mvl.id AS id,
                move.date,
                move.reference,
                mvl.product_id,
                template.categ_id as product_ctg_id,
                mvl.qty_done as qty_done,
                mvl.qty_done * template.quintales_per_ud as qty_qq,
                production.date_planned_start,
                production.state as mrp_state
                FROM stock_move_line AS mvl
                JOIN stock_move move ON (move.id=mvl.move_id)
                JOIN mrp_production production
                    ON (production.id=move.production_id and production.product_id = move.product_id)
                JOIN product_product as product ON (product.id=mvl.product_id)
                JOIN product_template as template ON (template.id=product.product_tmpl_id)
                WHERE move.production_id is not null
                UNION (
                    SELECT
                        mvl.id AS id,
                        move.date,
                        move.reference,
                        mvl.product_id,
                        template.categ_id as product_ctg_id,
                        mvl.qty_done * -1 as qty_done,
                        mvl.qty_done * template.quintales_per_ud * -1 as qty_qq,
                        production.date_planned_start as date_planned_start,
                        unbuild.state as mrp_state
                    FROM stock_move_line AS mvl
                    JOIN stock_move move ON (move.id=mvl.move_id)
                    JOIN mrp_unbuild unbuild
                        ON (unbuild.id=move.unbuild_id and unbuild.product_id=move.product_id)
                    LEFT JOIN mrp_production as production
                        ON production.id = unbuild.mo_id
                    JOIN product_product as product ON (product.id=mvl.product_id)
                    JOIN product_template as template ON (template.id=product.product_tmpl_id)
                    WHERE move.unbuild_id is not null
                )
        ) as foo
        """

    def _where(self):
        return """
            WHERE 
                move.production_id is not null
                OR move.unbuild_id is not null
        """

    def _group_by(self):
        return """
            GROUP BY
                mvl.id,
                move.date,
                move.reference,
                mvl.product_id,
                template.categ_id,
                move.production_id,
                move.unbuild_id,
                template.quintales_per_ud
        """
