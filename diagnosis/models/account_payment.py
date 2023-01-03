from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    affected_box = fields.Char()
    move_reconcile_line = fields.Many2one("account.move")
    product_categ_id = fields.Many2one("product.category")
    insurance_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Insurance carrier',
        domain=[('partner_type', '=', 'insurence')],
        help="Insurace type partner related to this invoice"
    )
    db_external_state = fields.Integer(
        help="Technical field. Save external state", string="External state")

    @api.depends(
        'journal_id', 'partner_id', 'partner_type',
        'is_internal_transfer', 'insurance_partner_id',
        'product_categ_id')
    def _compute_destination_account_id(self):
        super()._compute_destination_account_id()
        to_change = self.filtered(
            lambda x: x.insurance_partner_id or x.product_categ_id)
        for rec in to_change:
            destination_account_id = rec.destination_account_id
            categ = rec.product_categ_id
            account_id = (
                (categ.is_force_account and categ.insurance_account_receivable_id) or
                rec.insurance_partner_id.insurance_account_receivable_id)
            rec.destination_account_id = (account_id or destination_account_id).id
