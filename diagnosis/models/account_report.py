from odoo import models, api


class GenericTaxReport(models.AbstractModel):
    _inherit = 'account.generic.tax.report'

    filter_payment_date = True

    @api.model
    def _get_options(self, previous_options=None):
        rslt = super()._get_options(previous_options)
        if rslt['payment_date']:
            rslt['date']['date_field'] = 'invoice_payment_date'
        return rslt
