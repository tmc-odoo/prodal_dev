
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_zone_id = fields.Many2one(
        'prodal.zone',
        related='sale_id.zone_id',
        string='Sale Zone',
        store=True,
        readonly=True
    )

    sale_notes = fields.Char(
        string='Sale Notes',
        related='sale_id.notes',
        help='Sale order notes',
    )

    sale_note = fields.Text(
        string='Sale Note',
        related='sale_id.note',
        help='Sale order note',
        readonly=False
    )

    quintal_total = fields.Float(
        string='Total Quintals',
        compute='_compute_quintal_total',
        store=True,
        readonly=False,
    )

    truck_id = fields.Many2one(
        'fleet.vehicle',
        string='Truck'
    )

    driver = fields.Many2one(
        'hr.employee',
        string='Driver',
    )

    assistant_ids = fields.Many2many(
        'hr.employee',
        string='Assistants',
    )

    show_vehicle_fields = fields.Boolean(
        related='picking_type_id.show_vehicle_fields',
        readonly=True
    )

    show_freight_type = fields.Boolean(
        related='picking_type_id.show_freight_type',
        readonly=True
    )

    total_price = fields.Float(
        string='Total price',
        help='Total price of all the move lines',
        compute='_compute_price_total',
    )

    check_payment = fields.Boolean(
        string='Is Check Payment',
        compute='_compute_check_payment'
    )

    days_since_creation = fields.Integer(
        string='Days',
        help='Amount of days since stock picking creation',
        compute='_compute_days_since'
    )

    salesperson = fields.Many2one(
        string='Salesperson',
        related='sale_id.user_id',
        store=True
    )

    freight_type = fields.Selection(
        [('int', 'Internal'), ('ext', 'External')],
        'Freight Type',
        default='int',
        required=True
    )

    unload_factor = fields.Float(
        string='Unload Factor',
        related='partner_id.unload_factor'
    )

    unload_price = fields.Float(
        string='Unload Price'
    )

    driver_ext = fields.Char(
        string='External Driver'
    )

    driver_ext_plate = fields.Char(
        string='External Driver Plate'
    )

    driver_ext_id = fields.Char(
        string='External Driver ID'
    )

    partner_name = fields.Char(
        string='Contact',
        related='partner_id.name'
    )
    batch_created_uid = fields.Many2one('res.users', related='batch_id.create_uid', string="Batch created uid",
                                        store=True)
    batch_created_date = fields.Datetime(related='batch_id.create_date', string="Batch created date", store=True)
    batch_quintal_total = fields.Float(related='batch_id.quintal_total', string="Batch quintal total", store=True)
    dest_move_unprocessed = fields.Boolean()
    user_to_notify = fields.Many2one('res.users')

    def get_unload_price(self):
        for picking in self:
            moves = picking.move_ids_without_package.filtered(
                lambda m: m.product_uom.is_unload_unit
            )
            weighted_bags = moves.mapped(
                lambda m: m.quantity_done * m.product_id.weight_factor
            )
            picking.unload_price = picking.unload_factor * sum(weighted_bags)

    @api.depends('move_ids_without_package')
    def _compute_quintal_total(self):
        for picking in self:
            total = 0
            moves = picking.mapped('move_ids_without_package')
            for move in moves:
                total += move.product_id.quintales_per_ud * move.product_uom_qty
            picking.quintal_total = total


    @api.depends('date_done')
    def _compute_days_since(self):
        today = datetime.now()
        for picking in self:
            date_to = picking.date_done or today
            picking.days_since_creation = (date_to - picking.create_date).days

    @api.depends('move_lines')
    def _compute_price_total(self):
        prices = self.move_lines.mapped(
            lambda ml: ml.product_id.list_price *
            ml.quantity_done
        )
        self.total_price = sum(prices)

    @api.depends('sale_id.payment_term_id')
    def _compute_check_payment(self):
        term_names = self.mapped('sale_id.payment_term_id.name')
        self.check_payment = 'Contado cheque' in term_names

    def button_validate(self):
        res = super().button_validate()
        self.send_user_notification()
        return res

    def send_user_notification(self):
        if not self.user_to_notify:
            return
        notification_ids = [(0, 0, {
            'res_partner_id': self.user_to_notify.partner_id.id,
            'notification_type': 'inbox'
        })]
        view = self.env.ref('prodal.stock_picking_validation_message_template')
        vals = {'name': self.name, 'id': self.id}
        self.message_post(
            body=view.render(vals, engine='ir.qweb', minimal_qcontext=True),
            message_type="notification",
            subtype="mail.mt_comment",
            author_id=self.env.user.partner_id.id,
            notification_ids=notification_ids
        )


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    show_vehicle_fields = fields.Boolean(
        string="Show driver and truck"
    )

    show_freight_type = fields.Boolean(
        string="Show freight type"
    )


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    quintal_total = fields.Float(
        string='Total Quintals',
        compute='_compute_quintal_total',
        store=True,
        readonly=False,
    )
    user_id = fields.Many2one(
        'hr.employee',
        string='Responsible',
        help='Person responsible for this batch transfer'
    )
    truck_id = fields.Many2one(
        'fleet.vehicle',
        string='Truck'
    )
    driver = fields.Many2one(
        'hr.employee',
        string='Driver',
    )
    assistant_ids = fields.Many2many(
        'hr.employee',
        string='Assistants',
    )
    quintal_limit = fields.Float(
        string='Quintal Limit',
        related='truck_id.quintal_limit'
    )
    move_join_ids = fields.One2many(
        'stock.move',
        string='move joined',
        compute='_compute_join_moves'
    )
    unload_price = fields.Float(
        string='Unload Price'
    )

    def get_unload_price(self):
        for batch in self:
            pickings = batch.picking_ids
            pickings.get_unload_price()
            batch.unload_price = sum(
                pickings.mapped('unload_price')
            )

    @api.onchange('truck_id')
    def default_driver(self):
        if len(self) != 1:
            return
        if not self.driver:
            self.driver = self.truck_id.driver_id
        if not self.assistant_ids:
            self.assistant_ids = self.truck_id.assistant_ids

    @api.depends('picking_ids', 'picking_ids.move_ids_without_package')
    def _compute_quintal_total(self):
        quintal_total = 0
        for batch in self:
            moves = batch.picking_ids.mapped('move_ids_without_package')
            quintal_total = sum(
                moves.mapped(lambda m: m.product_id.quintales_per_ud * m.product_uom_qty)
            )
            batch.quintal_total = quintal_total


    def done(self):
        if self.env.user.has_group('prodal.group_ignore_qq_validation'):
            return super().done()

        if self.quintal_total > self.quintal_limit:
            raise ValidationError(_('Total quintals above the limit.'))

        return super().done()

    @api.depends('picking_ids')
    def _compute_join_moves(self):
        for batch in self:
            batch.move_join_ids = batch.get_filtered_moves()

    def get_filtered_moves(self):
        id_ = int(self._origin.id)
        self.env.cr.execute(
            'SELECT DISTINCT ON (sm.product_id) sm.id '
            'FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id '
            'WHERE batch_id = %s;', (id_,)
        )
        move_ids = [m_id[0] for m_id in self.env.cr.fetchall()]
        return self.env['stock.move'].browse(move_ids)

    def get_zone_to_picking_date_map(self, zone_ids):
        """Returns dictionary with the earliest creation dates (value) of stock pickings
           with a given sale zone id (key)
        """
        self._cr.execute(
            'SELECT MIN(sp.create_date), so.zone_id '
            'FROM stock_picking as sp INNER JOIN sale_order as so ON sp.sale_id = so.id '
            'WHERE so.zone_id in %s AND sp.state = \'assigned\''
            'GROUP BY so.zone_id;',
            (tuple(zone_ids),))
        return {record[1]:record[0] for record in self.env.cr.fetchall()}
