from odoo import models, fields, api, _

class RepairOrder(models.Model):
    _inherit="repair.order"

    product_ids = fields.Many2many('product.product')
    lot_ids = fields.Many2many('stock.production.lot')
    product_id = fields.Many2one('product.product', domain="[('id', 'in', product_ids)]")
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial',
        domain="[('id', 'in', lot_ids), ('product_id','=', product_id), ('company_id', '=', company_id)]", check_company=True,
        help="Products repaired are all belonging to this lot")
    state = fields.Selection(readonly=False, selection_add=[('reception', 'Reception'), ('draft',)], default="reception")
    external_product = fields.Boolean()
    lot = fields.Char()
    repair_count = fields.Integer(default=0)
    field_service_count = fields.Integer(default=0)
    roduct_qty = fields.Float(
        'Product Quantity',
        default=1.0, digits='Product Unit of Measure',
        readonly=True, required=True, states={'draft': [('readonly', False)], 'reception':[('readonly', False)]})
    product_uom = fields.Many2one(
        'uom.uom', 'Product Unit of Measure',
        readonly=True, required=True, states={'draft': [('readonly', False)], 'reception':[('readonly', False)]}, domain="[('category_id', '=', product_uom_category_id)]")
    location_id = fields.Many2one(
        'stock.location', 'Location',
        index=True, readonly=True, required=True, check_company=True,
        help="This is the location where the product to repair is located.",
        states={'draft': [('readonly', False)], 'reception':[('readonly', False)], 'confirmed': [('readonly', True)]})

    @api.onchange('partner_id', 'external_product')
    def _compute_product_ids(self):
        SaleOrder = self.env['sale.order'].sudo()
        ProductProduct = self.env['product.product'].sudo()

        for record in self:
            if record.external_product:
                record.product_ids = ProductProduct.search([])
                continue

            if not record.partner_id:
                record.product_id = False
                record.product_ids = ProductProduct
                continue

            sale_id = SaleOrder.search([('partner_id', '=', record.partner_id.id)])

            if not sale_id:
                record.product_ids = ProductProduct
                continue

            product_ids = ProductProduct
            for line in sale_id.order_line:
                if not line.qty_delivered:
                    continue
                product_ids += line.product_id

            record.product_ids = product_ids
        return

    @api.onchange('partner_id', 'product_id')
    def _compute_lot_ids(self):
        StockMoveLine = self.env['stock.move.line']
        StockProductLot = self.env['stock.production.lot']

        for record in self:
            record.lot_ids = False

            if not record.partner_id:
                record.lot_ids = False
                continue

            if not record.product_id:
                record.lot_ids = False
                continue

            ans = StockProductLot

            domain = record._get_stock_move_line_domain()
            stock_move_line_ids = StockMoveLine.search(domain)

            for line in stock_move_line_ids:
                if line.picking_id.sale_id.partner_id != record.partner_id:
                    continue
                if line.picking_id.state != 'done':
                    continue
                ans += line.lot_id

            if ans:
                record.lot_ids = ans

    @api.onchange('lot_id')
    def _onchange_lot_id(self):
        for record in self:
            if not record.lot_id:
                record.lot = False
                continue
            record.lot = record.lot_id.name
        return
    
    @api.onchange('operations', 'fees_lines')
    def _oncahnge_operations_fees_lines(self):
        for record in self:
            if record.operations or record.fees_lines:
                record.write({'state':'draft'})

    def _get_stock_move_line_domain(self):
        return [('product_id', '=', self.product_id.id)]

    def action_validate(self):
        super().action_validate()
        self.create_field_service()
        self.get_related_repair_order()
        self.get_related_field_service()
    
    def create_field_service(self):
        self.ensure_one()

        ProjectTask = self.env['project.task'].with_context(fsm_mode=True)
        task_vals = self.get_field_service_vals()
        ProjectTask.create(task_vals)

        return

    def get_field_service_vals(self):
        return {
            'name': self.name,
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'planned_date_begin': False,
            'planned_date_end':False,
            'repair_id': self.id
        }

    def get_related_repair_order(self):
        for record in self:
            if record.state in ('draft', 'reception'):
                record.repair_count = 0
                continue
            record.repair_count = len(record.related_order())
        return
    
    def related_order(self):
        self.ensure_one()
        return self.search([('product_id', '=', self.product_id.id), ('partner_id', '=', self.partner_id.id), ('lot', '=', self.lot)])

    def get_related_field_service(self):
        for record in self:
            if record.state in ('draft', 'reception'):
                record.field_service_count = 0
                continue
            record.field_service_count = len(record.related_field_service())

    def related_field_service(self):
        self.ensure_one()

        ProjectTask = self.env['project.task']
        order_list = self.related_order().mapped('id')

        return ProjectTask.search([('repair_id', 'in', order_list)])

    def action_view_task(self):
        ctx = self.get_task_ctx()
        domain = self.get_task_domain()

        action = self.env.ref('industry_fsm.project_task_action_fsm').read()[0]
        action['context'] = dict(ctx)
        action['domain'] = domain
        return action

    def action_view_related_repair(self):
        action = self.env.ref('repair.action_repair_order_tree').read()[0]
        action['domain'] = self.get_repair_domain()
        return action

    def get_task_ctx(self):
        return {
            'fsm_mode': True, 
            'show_address': True,
            'fsm_task_kanban_whole_date': False,        
        }
    
    def get_task_domain(self):
        return [('is_fsm', '=', True), ('id', 'in', self.related_field_service().mapped('id'))]

    def get_repair_domain(self):
        return [('id', 'in', (self.related_order() - self).mapped('id'))]

    def action_repair_cancel(self):
        super().action_repair_cancel()
        ProjectTask = self.env['project.task']

        project_id = ProjectTask.search([('repair_id', '=', self.id)])

        if not project_id:
            return
        
        project_id.unlink()

