from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    parent_id = fields.Many2one(
        string='Categoria padre' , 
        related= 'categ_id.parent_id' , 
        store = True)
