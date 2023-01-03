from odoo import models, fields, api,_


class rierba_bl(models.Model):
    _name = 'rierba_bl.rierba_bl'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'rierba_bl.rierba_bl'

    name = fields.Char(string='BL name')
    supplier_invoice = fields.Boolean(string='supplier invoice')
    packing_list = fields.Boolean(string='packing list')
    certificate_origin = fields.Boolean(string='certificate of origin')
    bill_lading = fields.Boolean(string='bill of lading')
    insurance_Policy = fields.Boolean(string='Insurance Policy')
    supplier_form = fields.Boolean(string='supplier form')
    invoice_expenses = fields.Boolean(string='invoice of local expenses')
    transportation_invoice = fields.Boolean(string='transportation invoice')
    freight_bill = fields.Boolean(string='freight bill')
    customs_invoice = fields.Boolean(string='customs management invoice')
    phytosanitary_certificate = fields.Boolean(string='phytosanitary certificate')
    supplier_doc = fields.Binary(string='Documents supplier invoice')
    packing_doc = fields.Binary(string='Documents packing list')
    certificate_doc = fields.Binary(string='Documents certificate of origin')
    bill_doc = fields.Binary(string='Documents bill of lading')
    insurance_doc = fields.Binary(string='Documents Insurance Policy')
    supplier_form_doc = fields.Binary(string='Documents supplier form')
    invoice_doc = fields.Binary(string='Documents invoice of local expenses')
    transportation_doc = fields.Binary(string='Documents transportation invoice')
    freight_doc = fields.Binary(string='Documents freight bill')
    customs_doc = fields.Binary(string='Documents customs management invoice')
    phytosanitary_doc = fields.Binary(string='Documents phytosanitary certificate')
    purchase_ids = fields.One2many("purchase.order",'rierba_bl_id')
    invoice_ids = fields.One2many("account.move",'rierba_bl')

    def write(self,vals):
        res = super().write(vals)
        trasn_fields = {'supplier invoice':'factura del proveedor',
                        'packing list':'lista de empaque',
                        'certificate of origin':'certificado de origen',
                        'bill of lading':'guía de carga',
                        'Insurance Policy':'Póliza de seguros',
                        'supplier form':'formulario de proveedor',
                        'invoice of local expenses':'factura de gastos locales',
                        'transportation invoice':'factura de transporte',
                        'freight bill':'factura de flete',
                        'customs management invoice':'factura de gestión de aduanas',
                        'phytosanitary certificate':'certificado fitosanitario',
                        'Documents supplier invoice':'Documentos factura del proveedor',
                        'Documents packing list':'Documentos lista de empaque',
                        'Documents certificate of origin':'Documentos certificado de origen',
                        'Documents bill of lading':'Documentos guía de carga',
                        'Documents Insurance Policy':'Documentos Póliza de seguros',
                        'Documents supplier form':'Documentos formulario de proveedor',
                        'Documents invoice of local expenses':'Documentos factura de gastos locales',
                        'Documents transportation invoice':'Documentos factura de transporte',
                        'Documents freight bill':'Documentos factura de flete',
                        'Documents customs management invoice':'Documentos factura de gestión de aduanas',
                        'Documents phytosanitary certificate':'Documentos certificado fitosanitario'                        
                        }
        check = {True:"hecho",False:"desecho"}

        # for field in vals:
        #     if field not in ['name','purchase_ids']:
        #         self.message_post(body=(f"{trasn_fields[self._fields[(field)].string]} fue {check[vals[field]]}"))

        # return res
    

    @api.onchange('supplier_doc')
    def _compute_change_value(self):
        if self.supplier_doc:
            self.supplier_invoice = True
        else:
            self.supplier_invoice = False

    @api.onchange('packing_doc')
    def _compute_change_value1(self):
        if self.packing_doc:
            self.packing_list = True
        else:
            self.packing_list = False            

    @api.onchange('certificate_doc')
    def _compute_change_value2(self):
        if self.certificate_doc:
            self.certificate_origin = True
        else:
            self.certificate_origin = False

    @api.onchange('bill_doc')
    def _compute_change_value3(self):
        if self.bill_doc:
            self.bill_lading = True
        else:
            self.bill_lading = False 

    @api.onchange('insurance_doc')
    def _compute_change_value4(self):
        if self.insurance_doc:
            self.insurance_Policy = True
        else:
            self.insurance_Policy = False

    @api.onchange('supplier_form_doc')
    def _compute_change_value5(self):
        if self.supplier_form_doc:
            self.supplier_form = True
        else:
            self.supplier_form = False 

    @api.onchange('invoice_doc')
    def _compute_change_value6(self):
        if self.invoice_doc:
            self.invoice_expenses = True
        else:
            self.invoice_expenses = False  


    @api.onchange('transportation_doc')
    def _compute_change_value7(self):
        if self.transportation_doc:
            self.transportation_invoice = True
        else:
            self.transportation_invoice = False              

    @api.onchange('freight_doc')
    def _compute_change_value8(self):
        if self.freight_doc:
            self.freight_bill = True
        else:
            self.freight_bill = False  

    @api.onchange('phytosanitary_doc')
    def _compute_change_value9(self):
        if self.phytosanitary_doc:
            self.phytosanitary_certificate = True
        else:
            self.phytosanitary_certificate = False     


