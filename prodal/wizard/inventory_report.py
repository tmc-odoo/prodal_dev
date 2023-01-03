from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class InventoryReportWizard(models.TransientModel):
    _name="inventory.report.wizard"
    _description="Inventory report wizard"

    categ_ids = fields.Many2many('product.category', string='Product Category')
    location_ids = fields.Many2many('stock.location', string='Location')

    def _build_contexts(self, data):
        """Build context to use in wizard.
        Args:
            data: Dict of data wizard
        Returns:
            Dict of context wizard.
        """
        result = {}
        result['categ_ids'] = data['form'].get("categ_ids") or False
        result['location_ids'] = data['form'].get("location_ids") or False
        return result

    def get_report(self):
        """Call when button 'Print' clicked.
        Returns:
            Action to construct the report parameters.
        """
        self.ensure_one()
        data = {}
        data['form'] = self.read(['categ_ids', 'location_ids'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = (
            dict(used_context, lang=self.env.context.get('lang') or 'en_US'))
        return self.env.ref(
            'prodal.inventory_report').report_action(
                self, data=data)

class InventoryReport(models.AbstractModel):
    _name = 'report.prodal.inventory_report_view'

    def get_quant_committed_qty(self, product):
        domain = [
            ('product_id', '=', product.id),
            ('picking_id.state', 'in', ['assigned', 'confirmed']),
            ('picking_code', '=', 'outgoing'),
            ('location_id.usage', '=', 'internal')
        ]
        moves = self.env["stock.move"].search(domain)
        return sum(moves.mapped("product_uom_qty"))

    @api.model
    def _get_report_values(self, docids, data=None):
        """Function to consult the report values.
        """
        categories = self.env['product.category'].browse(data['form'].get('categ_ids', []))
        locations = self.env['stock.location'].browse(data['form'].get('location_ids', []))
        stock = self.env['stock.quant'].search([]).filtered(lambda x: x.location_id in locations and x.product_id.categ_id in categories)
        products = self.env['product.product'].search([]).filtered(lambda x: x.categ_id in categories)
        total = []
        product_ids = []
        categ_ids = categories.mapped('shown_name')
        quintals_total = 0
        for item in stock:
            if item.product_id in product_ids:
                continue
            product_ids.append(item.product_id)
            filtered_stock = stock.filtered(lambda x: x.product_id == item.product_id)
            committed = self.get_quant_committed_qty(item.product_id)
            doc_data = {'available' : 0, 'reserved': 0,
                        'difference':0,'committed': committed,
                        'stock_max':0, 'stock_min':0,
                        'qty_to_produce':0, 'entry':0}
            for product in filtered_stock:
                doc_data['name'] = "[{}]".format(product.product_id.default_code) + product.product_id.name
                doc_data['available'] = doc_data['available'] + product.quantity
                doc_data['reserved'] = doc_data['reserved'] + product.reserved_quantity
                doc_data['difference'] = doc_data['difference'] + product.available_difference
                doc_data['committed'] = doc_data['committed']
                doc_data['stock_max'] = product.stock_max
                doc_data['stock_min'] = product.stock_min
                doc_data['qty_to_produce'] = doc_data['stock_max'] - doc_data['difference'] if doc_data['difference'] < doc_data['stock_max'] else 0
                doc_data['categ_id'] = product.product_id.categ_id.shown_name
                doc_data['quintals'] =  product.product_id.quintales_per_ud * doc_data['available']
                doc_data['entry'] = doc_data['entry'] + product.picking_entry
                quintals_total += doc_data['quintals']
            total.append(doc_data)

        for product in products:
            if product in product_ids:
                continue
            doc_data = {}
            doc_data['name'] = "[{}]".format(product.default_code) + product.name
            doc_data['available'] = 0
            doc_data['entry'] = 0
            doc_data['reserved'] =  'n/a'
            doc_data['committed'] = self.get_committed_qty(product.id, locations)
            doc_data['difference'] = 0 - doc_data['committed']
            doc_data['stock_max'] = max(product.mapped('orderpoint_ids.product_max_qty') or [0])
            doc_data['stock_min'] = min(product.mapped('orderpoint_ids.product_min_qty') or [0])
            doc_data['qty_to_produce'] =  doc_data['stock_max'] - doc_data['difference'] if doc_data['difference'] < doc_data['stock_max'] else 0
            doc_data['quintals'] =  0
            doc_data['categ_id'] = product.categ_id.shown_name
            total.append(doc_data)

        if not total:
            raise ValidationError(_("There is no registers between categories and locations selected"))

        total.sort(key=lambda x:x['name'])
        return {
            'locations': locations,
            'categories': categ_ids,
            'total': total,
            'quintals_total': quintals_total
        }

    def get_committed_qty(self, prdct_id, locations):
        domain = [
            ('product_id', '=', prdct_id),
            ('picking_id.state', 'in', ['assigned', 'confirmed']),
            ('location_id.usage', '=', 'internal'),
            ('picking_code', '=', 'outgoing'),
        ]
        moves = self.env["stock.move"].search(domain)
        return sum(moves.mapped("product_uom_qty"))
