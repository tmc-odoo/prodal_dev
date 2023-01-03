from odoo import models, fields

class ProjectTask(models.Model):
    _inherit="project.task"

    repair_id = fields.Many2one('repair.order')
    lot = fields.Char(related="repair_id.lot", readonly=True)
    product_id = fields.Many2one('product.product', related="repair_id.product_id", readonly=True)