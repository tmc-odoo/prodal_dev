from odoo import models


class InventoryQuintalsReportWizard(models.TransientModel):
    _name='inventory.quintals.report.wizard'
    _inherit='inventory.report.wizard'
    _description='Inventory Quintals Report Wizard'

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
        return self.env.ref('prodal.inventory_quintals_report').report_action(self, data=data)


class InventoryQuintalsReport(models.AbstractModel):
    _name = 'report.prodal.inventory_report_quintals'
    _inherit = 'report.prodal.inventory_report_view'
