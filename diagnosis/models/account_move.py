from odoo.addons.web.controllers.main import ExcelExport
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, format_amount
from werkzeug.wrappers import Request, Response
from datetime import datetime
import base64
import json


class AccountMove(models.Model):
    _inherit = "account.move"

    insurance_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Insurance carrier',
        domain=[('partner_type', '=', 'insurence')],
        help="Insurace type partner related to this invoice"
    )
    institution_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Institution',
        domain=[('partner_type', '=', 'institution')],
        help="Institution type partner related to this invoice"
    )
    insurance_authorization = fields.Char(
        string='Insurance authorization',
        help="Field to describe the authorization from the insurance"
    )
    affiliate_number = fields.Char(
        string='Affiliate number',
        related='partner_id.affiliate_number',
        readonly=True,
        help="Partner's insurance affiliation number"
    )
    insurance_policy = fields.Char(
        string='Insurance policy',
        related='partner_id.insurance_policy',
        readonly=True,
        help="Partner's insurance affiliation number"
    )
    insurance_coverage_amount = fields.Monetary(
        string='Total insurance coverage',
        currency_field="currency_id",
        compute="_compute_insurance_institution",
        store=True,
        help="Total amount covered by the insurance"
    )
    institution_coverage_amount = fields.Monetary(
        string='Total institution coverage',
        currency_field="currency_id",
        compute="_compute_insurance_institution",
        inverse="_inverse_institution_coverage_amount",
        store=True,
        help="Total amount covered by the institution"
    )
    insurance_amount_paid = fields.Monetary(
        string='Amount paid insurance',
        currency_field="currency_id",
        store=True,
        help="Total amount paid insurance"
    )
    is_closed_safe = fields.Boolean("Closed safe")
    close_reason_id = fields.Many2one("insurance.close.reason")
    referrer_id = fields.Many2one(
        'diagnosis.referrer',
        string='Referrer',
    )
    db_external_id = fields.Integer(
        help="Technical field. Save external ID other Databases")
    db_external_state = fields.Integer(
        help="Technical field. Save external state", string="External state")
    insurance_related_move_ids = fields.Many2many(
        "account.move", 'account_move_insurance_related_move',
        'insurance_id', 'move_id', readonly=False)
    is_insurance_move = fields.Boolean("Has invoce insurance", readonly=True)
    move_insurance_id = fields.Many2one("account.move", readonly=True)
    code_pss = fields.Char(
        related="insurance_partner_id.code_pss", string="Code PSS")
    affiliate_number = fields.Char(
        related="partner_id.affiliate_number", string="No. affiliate")
    product_name = fields.Char(
        compute="_compute_product_name", string="Product name")
    partner_name = fields.Char(
        related="partner_id.name", string="Partner name")
    partner_vat = fields.Char(
        related="partner_id.vat", string="Partner vat")
    pending_balance_amount = fields.Monetary(
        compute="_compute_pending_balance",
        string="Pending balance", store=True)
    product_categ_id = fields.Many2one("product.category")

    @api.depends(
        'invoice_line_ids.insurance_coverage',
        'invoice_line_ids.institution_coverage'
    )
    def _compute_insurance_institution(self):
        for move in self:
            move.update({
                'insurance_coverage_amount': sum(move.mapped(
                    'invoice_line_ids.insurance_coverage'
                )),
                'institution_coverage_amount': sum(move.mapped(
                    'invoice_line_ids.institution_coverage'
                )),
            })

    @api.depends("insurance_coverage_amount", "insurance_amount_paid")
    def _compute_pending_balance(self):
        for rec in self:
            rec.pending_balance_amount = (
                rec.insurance_coverage_amount - rec.insurance_amount_paid)

    @api.depends("invoice_line_ids.name")
    def _compute_product_name(self):
        for rec in self:
            rec.product_name = rec.invoice_line_ids[0].name

    def _inverse_institution_coverage_amount(self):
        for rec in self.filtered(lambda x: x.move_type == 'out_invoice'):
            rec.is_closed_safe = float_compare(
                rec.insurance_amount_paid, rec.institution_coverage_amount,
                precision_rounding=rec.currency_id.rounding) == 0

    def _assert_not_closed_safe(self):
        """Validate duplicate flight in task
        """
        validate = any((
            not self.is_closed_safe,
            not self.currency_id.is_zero(self.insurance_amount_paid)))
        if validate:
            return
        msg = _(
            "You can not next because you do not set a amount in field Amount paid insurance")
        raise UserError(msg)

    @api.constrains("is_closed_safe", "insurance_amount_paid")
    def constraint_not_closed_safe(self):
        for rec in self.filtered(lambda x: x.move_type == 'out_invoice'):
            rec._assert_not_closed_safe()

    def _prepare_move_insurance_lines(self):
        lines = []
        group_lines = self.env["account.move.line"].read_group([
            ('id', 'in', self.invoice_line_ids.ids)],
            ["analytic_account_id", "insurance_coverage"], ["analytic_account_id"])
        product = self[0].company_id.product_invoice_insurance_id
        if not product:
            msg = _('The product for the insurance invoice could not be found please go to the accounting settingsn.')
            raise UserError(msg)
        account = product.product_tmpl_id.get_product_accounts()
        for line in group_lines:
            lines += [(0, 0, {
                'sequence': 1,
                'name': product.name,
                'product_id': product.id,
                'product_uom_id': product.uom_id.id,
                'quantity': 1,
                'discount': 0,
                'account_id': (account.get(
                    'income') or self.env["account.account"]).id,
                'tax_ids': [(6, 0, product.taxes_id.ids)],
                'price_unit': line["insurance_coverage"],
                'analytic_account_id': (line.get("analytic_account_id") or [False])[0]
            })]
        return lines

    def _prepare_move_insurance(self):
        rec = self[0]
        journal = self.with_context(
            default_move_type='out_invoice')._get_default_journal()
        if len(self.mapped("insurance_partner_id")) > 1:
            raise UserError(_("Only can create invoice for same the insurance partner"))
        if not journal:
            raise UserError(
                _('Please define an accounting sales journal for the company %s (%s).') % (
                    self.company_id.name, self.company_id.id))
        invoice_vals = {
            'move_type': 'out_invoice',
            'currency_id': rec.currency_id.id,
            'partner_id': rec.insurance_partner_id.id,
            'fiscal_position_id': (
                rec.fiscal_position_id or rec.fiscal_position_id.get_fiscal_position(
                    rec.partner_id.id)).id,
            'journal_id': journal.id,
            'invoice_origin': rec.name,
            'company_id': rec.company_id.id,
            'is_insurance_move': True,
        }
        return invoice_vals

    def action_convert_invoice_insurance(self):
        move_vals = self._prepare_move_insurance()
        move_vals["insurance_related_move_ids"] = [(6, 0, self.ids)]
        move_vals["invoice_line_ids"] = self._prepare_move_insurance_lines()
        move = self.create(move_vals)
        self.write({'move_insurance_id': move.id})
        view_id = self.env.ref('diagnosis.diagnosis_view_move_form_inherit').id
        return {
            'name': _("Invoice Insurance"),
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': move.id,
            'type': 'ir.actions.act_window',
            'context': self._context,
            'views': [[view_id, 'form']],
            'target': 'current',
        }

    def get_insurance_invoice_relationship(self):
        lines = []
        columns = [
            'insurance_authorization',
            'insurance_coverage_amount',
            'insurance_amount_paid',
            'pending_balance_amount',
            'name',
            'code_pss',
            'product_name',
            'partner_name',
            'invoice_date',
            'affiliate_number',
        ]
        return self.insurance_related_move_ids.read(columns)
        
    def get_insurance_invoice_concilation(self):
        lines = []
        sum_fields = [
            'insurance_authorization',
            'insurance_coverage_amount',
            'insurance_amount_paid',
            'pending_balance_amount']
        one_fields = [
            'name',
            'code_pss',
            'product_name',
            'partner_name',
            'partner_vat',
            'invoice_date',
            'affiliate_number',
        ]
        groups = self.read_group(
            [('id', 'in', self.insurance_related_move_ids.ids)],
            sum_fields, ['insurance_authorization'])
        for line in groups:
            records = self.search(line.get("__domain"))
            res = {f: records.mapped(f)[0] or "" for f in one_fields}
            res.update({f: line[f] or 0 for f in sum_fields})
            res.update(records.get_calculation_report_line())
            lines += [res]
        return lines

    def get_calculation_report_line(self):
        res = {
            "affiliate_difference": 0,
            "amount_service": 0,
        }
        for rec in self:
            line = rec.invoice_line_ids
            if not line:
                continue
            res["affiliate_difference"] += line[0].price_unit
            res["amount_service"] = +line[0].price_unit + line[0].insurance_coverage
        return res

    def _recompute_dynamic_lines(self, recompute_all_taxes=False, recompute_tax_base_amount=False):
        super()._recompute_dynamic_lines(
            recompute_all_taxes=recompute_all_taxes,
            recompute_tax_base_amount=recompute_tax_base_amount)
        records = self.filtered(
            lambda x: x.product_categ_id or x.insurance_partner_id).line_ids.filtered(
                lambda x: x.exclude_from_invoice_tab and x.account_id.internal_type == 'receivable')
        for rec in records:
            default_account = rec.account_id
            account_id = (
                rec.move_id.product_categ_id.insurance_account_receivable_id or
                rec.move_id.insurance_partner_id.insurance_account_receivable_id)
            rec.account_id = (account_id or default_account).id

    def format_date(self, dt):
        dt = fields.Date.from_string(dt) or datetime.now()
        return dt.strftime('%d/%m/%Y')

    def format_monetary(self, number, currency=False):
        currency = currency or self.currency_id
        return format_amount(self.env, number, currency)

    def calculate_total(self, datas, ftotal):
        return self.format_monetary(sum([i[ftotal] for i in datas]))

    def btn_download_xls(self):
        datas = self.get_insurance_invoice_concilation()
        rows = [
            "name", "code_pss", "product_name", "partner_name", "partner_vat",
            "invoice_date", "affiliate_number", "insurance_authorization",
            "insurance_coverage_amount", "insurance_amount_paid", "affiliate_difference",
            "amount_service", "pending_balance_amount"
        ]
        headers = [
            _("No."),
            _("Code PSS"),
            _("Product"),
            _("Nombre"),
            _("Cedula"),
            _("Attention date"),
            _("No. Afilliate"),
            _("No. Authorization"),
            _("Total authorization"),
            _("Total paid"),
            _("Affiliate difference"),
            _("Amount"),
            _("Pending balance")
        ]
        filename = _("Insurance conciliation")
        row_data = []
        for d in datas:
            row_data.append([d[r] for r in rows])
        xlsx_data = ExcelExport().from_data(headers, row_data)
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'datas': base64.encodebytes(xlsx_data),
            'res_id': self.id,
            'res_model': 'account.move',
        })
        return {
            'type': 'ir.actions.act_url',
            'url': self.get_compose_download_report_url(attachment, filename+".xls"),
            'target': 'new',
        }

    def get_compose_download_report_url(self, record, filename, download=True):
        base_url = ("/web/content/{res_id}/{filename}?download={download}")
        return base_url.format(
            res_id=record.id, filename=filename,
            download=json.dumps(download))

 
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    insurance_coverage = fields.Monetary(
        string='Insurance coverage',
        currency_field="currency_id",
        help="Amount covered by the insurance",
    )
    institution_coverage = fields.Monetary(
        string='Institution coverage',
        currency_field="currency_id",
        help="Amount covered by the institution",
    )
    db_external_id = fields.Integer(
        help="Technical field. Save external ID other Databases")

    @api.depends('product_id', 'account_id', 'partner_id', 'date')
    def _compute_analytic_account(self):
        super()._compute_analytic_account()
        records = self.filtered(
            lambda x: x.move_id.move_type == 'out_invoice'
            and x.product_id.categ_id.analytic_account_id)
        for rec in records:
            rec.analytic_account_id = rec.product_id.categ_id.analytic_account_id

    def _get_computed_account(self):
        res = super()._get_computed_account()
        move = self.move_id
        if move.move_type == 'out_invoice':
            account_id = (
                (self.product_id.categ_id.is_force_account and
                self.product_id.categ_id.property_account_income_categ_id) or
                move.insurance_partner_id.insurance_account_id)
            res = account_id or res
        return res
