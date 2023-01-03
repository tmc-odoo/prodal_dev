import datetime
import string
import re
import stdnum
from stdnum.eu.vat import check_vies
from stdnum.exceptions import InvalidComponent
import logging

from odoo import api, models, tools, _, fields
from odoo.tools.misc import ustr
from odoo.exceptions import ValidationError

class ResPartnerTitle(models.Model):
    _inherit = 'res.partner.title'
    _order = "sequence asc"


    sequence = fields.Integer()



class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _split_vat(self, vat):
        vat_country, vat_number = vat[:2].lower(), vat[2:].replace(' ', '')
        return vat_country, vat_number

    @api.model
    def simple_vat_check(self, country_code, vat_number):
        '''
        Check the VAT number depending of the country.
        http://sima-pc.com/nif.php
        '''
        if not ustr(country_code).encode('utf-8').isalpha():
            return False
        check_func_name = 'check_vat_' + country_code
        check_func = getattr(self, check_func_name, None) or getattr(stdnum.util.get_cc_module(country_code, 'vat'), 'is_valid', None)
        if not check_func:
            # No VAT validation available, default to check that the country code exists
            if country_code.upper() == 'EU':
                # Foreign companies that trade with non-enterprises in the EU
                # may have a VATIN starting with "EU" instead of a country code.
                return True
            country_code = _eu_country_vat_inverse.get(country_code, country_code)
            return bool(self.env['res.country'].search([('code', '=ilike', country_code)]))
        return check_func(vat_number)

    @api.model
    @tools.ormcache('vat')
    def _check_vies(self, vat):
        # Store the VIES result in the cache. In case an exception is raised during the request
        # (e.g. service unavailable), the fallback on simple_vat_check is not kept in cache.
        return check_vies(vat)

    @api.model
    def vies_vat_check(self, country_code, vat_number):
        try:
            # Validate against  VAT Information Exchange System (VIES)
            # see also http://ec.europa.eu/taxation_customs/vies/
            vies_result = self._check_vies(country_code.upper() + vat_number)
            return vies_result['valid']
        except InvalidComponent:
            return False
        except Exception:
            # see http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl
            # Fault code may contain INVALID_INPUT, SERVICE_UNAVAILABLE, MS_UNAVAILABLE,
            # TIMEOUT or SERVER_BUSY. There is no way we can validate the input
            # with VIES if any of these arise, including the first one (it means invalid
            # country code or empty VAT number), so we fall back to the simple check.
            _logger.exception("Failed VIES VAT check.")
            return self.simple_vat_check(country_code, vat_number)

    @api.model
    def fix_eu_vat_number(self, country_id, vat):
        europe = self.env.ref('base.europe')
        country = self.env["res.country"].browse(country_id)
        if not europe:
            europe = self.env["res.country.group"].search([('name', '=', 'Europe')], limit=1)
        if europe and country and country.id in europe.country_ids.ids:
            vat = re.sub('[^A-Za-z0-9]', '', vat).upper()
            country_code = _eu_country_vat.get(country.code, country.code).upper()
            if vat[:2] != country_code:
                vat = country_code + vat
        return vat

    @api.constrains('vat', 'country_id')
    def check_vat(self):
        # The context key 'no_vat_validation' allows you to store/set a VAT number without doing validations.
        # This is for API pushes from external platforms where you have no control over VAT numbers.
        if self.env.context.get('no_vat_validation'):
            return
        partners_with_vat = self.filtered('vat')
        if not partners_with_vat:
            return
        if self.env.context.get('company_id'):
            company = self.env['res.company'].browse(self.env.context['company_id'])
        else:
            company = self.env.company
        eu_countries = self.env.ref('base.europe').country_ids
        for partner in partners_with_vat:
            is_eu_country = partner.commercial_partner_id.country_id in eu_countries
            if company.vat_check_vies and is_eu_country and partner.is_company:
                # force full VIES online check
                check_func = self.vies_vat_check
            else:
                # quick and partial off-line checksum validation
                check_func = self.simple_vat_check

            failed_check = False
            #check with country code as prefix of the TIN
            vat_country_code, vat_number = self._split_vat(partner.vat)
            vat_has_legit_country_code = self.env['res.country'].search([('code', '=', vat_country_code.upper())])
