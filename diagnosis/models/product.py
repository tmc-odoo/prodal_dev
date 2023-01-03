from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    db_external_id = fields.Integer(
        help="Technical field. Save external ID other Databases")
    analytic_account_id = fields.Many2one(
        'account.analytic.account', string='Analytic account')
    insurance_account_receivable_id = fields.Many2one(
        "account.account",
        domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]")
    is_force_account = fields.Boolean("Force account")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    article_type = fields.Selection(
        [
            ('simple', 'Simple'),
            ('comp', 'Compound'),
            ('macro', 'Macro'),
        ],
        string='Article type',
        default="simple",
        help="""
            Types of article:
                simple: just a product,
                Compound: is made of 2 or more simple products,
                Macro: is made of 2 or more compound products
        """
    )
    db_external_id = fields.Integer(
        help="Technical field. Save external ID other Databases")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    article_type = fields.Selection(
        [
            ('simple', 'Simple'),
            ('comp', 'Compound'),
            ('macro', 'Macro'),
        ],
        string='Article type',
        default="simple",
        related="product_tmpl_id.article_type",
        help="""
            Types of article:
                simple: just a product,
                Compound: is made of 2 or more simple products,
        """
    )
    db_external_id = fields.Integer(
        help="Technical field. Save external ID other Databases")
