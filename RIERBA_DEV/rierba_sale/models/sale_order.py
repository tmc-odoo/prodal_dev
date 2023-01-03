import json
from odoo import models, fields, api,_
from odoo.exceptions import UserError
from odoo.osv import expression

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Weight Fields

    product_weight_uom = fields.Many2one(
        'uom.uom',
        string='Sale Unit',
        related='product_id.sale_uom'
    )

    product_weight = fields.Float(
        string='Weight'
    )

    sold_by_weight = fields.Boolean(
        related='product_id.sold_by_weight'
    )

    price_per_weight = fields.Float('Price per Weight')

    @api.onchange('product_weight', 'price_per_weight', 'product_uom_qty')
    def _onchange_weight_fields(self):
        for line in self.filtered(lambda l: l.sold_by_weight):
            line.price_unit = (line.price_per_weight * line.product_weight) / line.product_uom_qty

    def _prepare_procurement_values(self, group_id=False):
        values = super()._prepare_procurement_values(group_id)
        values['product_weight'] = self.product_weight
        return values

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res['product_weight'] = self.product_weight
        res['price_per_weight'] = self.price_per_weight
        return res

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if self.sold_by_weight:
            return
        super().product_uom_change()

    product_id_domain_relate = fields.Char(related="order_id.product_id_domain")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    product_id_domain = fields.Char(
        compute="_compute_product_id_domain",
        readonly=True,
        store=False,
    )
    pricelist_valide = fields.Many2many('product.pricelist')

    def action_confirm(self):

        if (
            self.pricelist_id.id != self.env.ref('product.list0').id and
            self.pricelist_id.id not in self.pricelist_valide.ids
        ):
            raise UserError(_(f"Esta lista de precios ({self.pricelist_id.name}) no ha sido autorizada"))
        return super(SaleOrder, self).action_confirm()

    def action_validate(self):
        self.pricelist_valide += self.pricelist_id
        self.order_line = False
        self.show_update_pricelist = True

    @api.onchange('pricelist_id', 'order_line')
    def _onchange_pricelist_id(self):
        if self.pricelist_id.id in self.pricelist_valide.ids:
            super()._onchange_pricelist_id()
        else:
            self.show_update_pricelist = False

    @api.depends('pricelist_id')
    def _compute_product_id_domain(self):
        for rec in self:
            domain = [('sale_ok', '=', True), '|', ('company_id', '=', False),
                     ('company_id', '=', 'parent.company_id')]
            if rec.pricelist_id.id and rec.pricelist_id.item_ids:
                pricelist = self.env['product.pricelist'].browse(rec.pricelist_id.id)
                pricelist_applied = pricelist.item_ids.mapped('applied_on')
                if '3_global' not in pricelist_applied:
                    products = []
                    for item in pricelist.item_ids:
                        if item.applied_on == "2_product_category":
                            cate = item.categ_id.id
                            expression.OR([domain,('categ_id','=',cate)])
                        elif item.applied_on == "1_product":
                            prod_templ = item.product_tmpl_id.product_variant_ids
                            products.extend(prod_templ.ids)
                        elif item.applied_on == "0_product_variant":
                            products.append(item.product_id.id)
                    if products:
                        domain.append(('id', 'in', products))
            rec.product_id_domain = json.dumps(domain)

    def write(self, values):
        result = super().write(values)
        pricelist = values.get('pricelist_id', False)
        if pricelist and pricelist != self.env.ref('product.list0').id:
            group_sale_manager = self.env.ref('sales_team.group_sale_manager')
            for user in group_sale_manager.users.ids:
                self.env['mail.activity'].create({
                    'summary': _("validacion de Tarifa pendiente"),
                    'res_model_id': self.env['ir.model'].search([("model",'=',self._name)]).id,
                    'res_id': self.id,
                    'user_id':user,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_email').id,
                    'date_deadline': fields.Datetime.now(),
                })
        return result
