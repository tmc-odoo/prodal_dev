from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    unload_factor = fields.Float(
        string='Unload Factor',
        help='Value multiplied by number of bags to get unload price'
    )

    is_unload_client = fields.Boolean(
        string='Unload client',
    )

    visit_weekday = fields.Selection(
        string='Visit weekday',
        selection=[
            ('mon', 'Monday'),
            ('tue', 'Tuesday'),
            ('wed', 'Wednesday'),
            ('thu', 'Thursday'),
            ('fri', 'Friday'),
            ('sat', 'Saturday'),
            ('sun', 'Sunday')
        ],
        help="Days to visit this partner."
    )

    last_sale_date = fields.Datetime(
        'Last sale date',
        related='last_sale.date_order',
        help="Last confirmed sale date",
        store=True
    )
    last_sale = fields.Many2one(
        'sale.order',
        string='Last sale',
        help="Last confirmed sale of this partner.",
        compute='_compute_last_sale'
    )
    code_reference = fields.Selection(
        selection=[
            ('ZZ', 'ZZ'),
            ('EE', 'EE'),
            ('A', 'A'),
            ('CP', 'CP'),
            ('VM', 'VM'),
        ], help="This code is use to generate the partner reference.")

    @api.model_create_multi
    def create(self, vals):
        for res in vals:
            if not res.get('ref', False) and res.get('code_reference', False):
                code = self.env['ir.sequence'].next_by_code('ref.res.partner')
                res['ref'] = res.get('code_reference') + code
        return super().create(vals)

    def write(self, vals):
        if vals.get('code_reference', False) and (
                ('ref' not in vals and not self.ref) or ('ref' in vals and not vals['ref'])):
            code = self.env['ir.sequence'].next_by_code('ref.res.partner')
            vals['ref'] = vals.get('code_reference') + code
        return super().write(vals)

    def _compute_last_sale(self):
        for partner in self:
            lastest_sale = partner.sale_order_ids.filtered(
                lambda s: s.state in ['sale', 'done']
            ).sorted('date_order', reverse=True)

            partner.last_sale = lastest_sale.ids and lastest_sale.ids[0] or False

    # Overrides the method from account module
    @api.depends_context('company')
    def _credit_debit_get(self):
        tables, where_clause, where_params = self.env['account.move.line'].with_context(state='posted', company_id=self.env.company.id)._query_get()
        where_params = [tuple(self.ids)] + where_params

        ## The table account_move_line has to be at the end ##
        try:
            tables_list = tables.split(',')
            aml_idx = tables_list.index('"account_move_line"')
            if aml_idx + 1 != len(tables_list):
                aml_table_name = tables_list.pop(aml_idx)
                tables = ','.join(tables_list + [aml_table_name])
        except ValueError:
            pass

        if where_clause:
            where_clause = 'AND ' + where_clause
        self._cr.execute("""SELECT account_move_line.partner_id, act.type, SUM(account_move_line.amount_residual)
                      FROM """ + tables + """
                      LEFT JOIN account_account a ON (account_move_line.account_id=a.id)
                      LEFT JOIN account_account_type act ON (a.user_type_id=act.id)
                      WHERE act.type IN ('receivable','payable')
                      AND account_move_line.partner_id IN %s
                      AND account_move_line.reconciled IS NOT TRUE
                      """ + where_clause + """
                      GROUP BY account_move_line.partner_id, act.type
                      """, where_params)
        treated = self.browse()
        for pid, acct_type, val in self._cr.fetchall():
            partner = self.browse(pid)
            if acct_type == 'receivable':
                partner.credit = val
                if partner not in treated:
                    partner.debit = False
                    treated |= partner
            elif acct_type == 'payable':
                partner.debit = -val
                if partner not in treated:
                    partner.credit = False
                    treated |= partner
        remaining = (self - treated)
        remaining.debit = False
        remaining.credit = False
