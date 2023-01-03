from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_uom = fields.Many2one(
        'uom.uom',
        string='Sale Unit'
    )

    sold_by_weight = fields.Boolean(
        string='Sold by Weight'
    )
