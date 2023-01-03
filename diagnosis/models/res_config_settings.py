from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    product_invoice_insurance_id = fields.Many2one(
        "product.product", "Product insurance")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_invoice_insurance_id = fields.Many2one("product.product",
        "Product insurance",
        related="company_id.product_invoice_insurance_id",
        readonly=False)
