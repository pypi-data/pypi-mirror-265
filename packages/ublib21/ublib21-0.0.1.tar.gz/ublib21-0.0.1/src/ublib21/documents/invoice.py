from typing import List
from ublib21.base import ComplexXMLParseableObject
from ublib21.common import cac, cbc, ext
from ublib21.exceptions import ListMustNotBeEmptyException
from ublib21.documents.base import Document


class Invoice(Document, ComplexXMLParseableObject):
    # Required Attrs
    id = None
    issue_date = None
    accounting_supplier_party = None
    accounting_customer_party = None
    legal_monetary_total = None
    invoice_line = None  # List (at least 1)

    # Optional Attrs
    ubl_extensions = None
    ubl_version_id = None
    customization_id = None
    profile_id = None
    profile_execution_id = None
    copy_indicator = None
    uuid = None
    issue_time = None
    due_date = None
    invoice_type_code = None
    note = None  # List
    tax_point_date = None
    document_currency_code = None
    pricing_currency_code = None
    payment_currency_code = None
    payment_alternative_currency_code = None
    accounting_cost_code = None
    accounting_cost = None
    line_count_numeric = None
    buyer_reference = None
    invoice_period = None  # List
    order_reference = None
    billing_reference = None  # List
    despatch_document_reference = None  # List
    receipt_document_reference = None  # List
    statement_document_reference = None  # List
    originator_document_reference = None  # List
    contract_document_reference = None  # List
    additional_document_reference = None  # List
    project_reference = None  # List
    signature = None  # List
    payee_party = None
    buyer_customer_party = None
    seller_supplier_party = None
    tax_representative_party = None
    delivery = None  # List
    delivery_terms = None
    payment_means = None  # List
    payment_terms = None  # List
    prepaid_payment = None  # List
    allowance_charge = None  # List
    tax_exchange_rate = None
    pricing_exchange_rate = None
    payment_exchange_rate = None
    payment_alternative_exchange_rate = None
    tax_total = None  # List
    withholding_tax_total = None  # List

    order_list = [
        'ubl_extensions',
        'ubl_version_id',
        'customization_id',
        'profile_id',
        'profile_execution_id',
        'id',
        'copy_indicator',
        'uuid',
        'issue_date',
        'issue_time',
        'due_date',
        'invoice_type_code',
        'note',
        'tax_point_date',
        'document_currency_code',
        'pricing_currency_code',
        'payment_currency_code',
        'payment_alternative_currency_code',
        'accounting_cost_code',
        'accounting_cost',
        'line_count_numeric',
        'buyer_reference',
        'invoice_period',
        'order_reference',
        'billing_reference',
        'despatch_document_reference',
        'receipt_document_reference',
        'statement_document_reference',
        'originator_document_reference',
        'contract_document_reference',
        'additional_document_reference',
        'project_reference',
        'signature',
        'accounting_supplier_party',
        'accounting_customer_party',
        'payee_party',
        'buyer_customer_party',
        'seller_supplier_party',
        'tax_representative_party',
        'delivery',
        'delivery_terms',
        'payment_means',
        'payment_terms',
        'prepaid_payment',
        'allowance_charge',
        'tax_exchange_rate',
        'pricing_exchange_rate',
        'payment_exchange_rate',
        'payment_alternative_exchange_rate',
        'tax_total',
        'withholding_tax_total',
        'legal_monetary_total',
        'invoice_line',
    ]

    xml_namespaces = [
        'xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"',
        'xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"',
        'xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"',
        'xmlns:ds="http://www.w3.org/2000/09/xmldsig#"',
        'xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"',
        'xmlns:sts="dian:gov:co:facturaelectronica:Structures-2-1"',
        'xmlns:xades="http://uri.etsi.org/01903/v1.3.2#"',
        'xmlns:xades141="http://uri.etsi.org/01903/v1.4.1#"',
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        'xsi:schemaLocation="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2 http://docs.oasis-open.org/ubl/os-UBL-2.1/xsd/maindoc/UBL-Invoice-2.1.xsd"',
    ]

    def __init__(self, id_: cbc.ID,
                 issue_date: cbc.IssueDate,
                 accounting_supplier_party: cac.AccountingSupplierParty,
                 accounting_customer_party: cac.AccountingCustomerParty,
                 legal_monetary_total: cac.LegalMonetaryTotal,
                 invoice_line: List[cac.InvoiceLine],
                 ubl_extensions: ext.UBLExtensions = None,
                 ubl_version_id: cbc.VersionID = None,
                 customization_id: cbc.CustomizationID = None,
                 profile_id: cbc.ProfileID = None,
                 profile_execution_id: cbc.ProfileExecutionID = None,
                 copy_indicator: cbc.CopyIndicator = None,
                 uuid: cbc.UUID = None,
                 issue_time: cbc.IssueDate = None,
                 due_date: cbc.DueDate = None,
                 invoice_type_code: cbc.InvoiceTypeCode = None,
                 note: List[cbc.Note] = None,
                 tax_point_date: cbc.TaxPointDate = None,
                 document_currency_code: cbc.DocumentCurrencyCode = None,
                 pricing_currency_code: cbc.PricingCurrencyCode = None,
                 payment_currency_code: cbc.PaymentCurrencyCode = None,
                 payment_alternative_currency_code: cbc.PaymentAlternativeCurrencyCode = None,
                 accounting_cost_code: cbc.AccountingCostCode = None,
                 accounting_cost: cbc.AccountingCost = None,
                 line_count_numeric: cbc.LineCountNumeric = None,
                 buyer_reference: cbc.BuyerReference = None,
                 invoice_period: List[cac.InvoicePeriod] = None,
                 order_reference: cac.OrderReference = None,
                 billing_reference: List[cac.BillingReference] = None,
                 despatch_document_reference: List[cac.DespatchDocumentReference] = None,
                 receipt_document_reference: List[cac.ReceiptDocumentReference] = None,
                 statement_document_reference: List[cac.StatementDocumentReference] = None,
                 originator_document_reference: List[cac.OriginatorDocumentReference] = None,
                 contract_document_reference: List[cac.ContractDocumentReference] = None,
                 additional_document_reference: List[cac.AdditionalDocumentReference] = None,
                 project_reference: List[cac.ProjectReference] = None,
                 signature: List[cac.Signature] = None,
                 payee_party: cac.PayeeParty = None,
                 buyer_customer_party: cac.BuyerCustomerParty = None,
                 seller_supplier_party: cac.SellerSupplierParty = None,
                 tax_representative_party: cac.TaxRepresentativeParty = None,
                 delivery: List[cac.Delivery] = None,
                 delivery_terms: cac.DeliveryTerms = None,
                 payment_means: List[cac.PaymentMeans] = None,
                 payment_terms: List[cac.PaymentTerms] = None,
                 prepaid_payment: List[cac.PrepaidPayment] = None,
                 allowance_charge: List[cac.AllowanceCharge] = None,
                 tax_exchange_rate: cac.TaxExchangeRate = None,
                 pricing_exchange_rate: cac.PricingExchangeRate = None,
                 payment_exchange_rate: cac.PaymentExchangeRate = None,
                 payment_alternative_exchange_rate: cac.PaymentAlternativeExchangeRate = None,
                 tax_total: List[cac.TaxTotal] = None,
                 withholding_tax_total: List[cac.WithholdingTaxTotal] = None) -> None:
        self.id = id_
        self.issue_date = issue_date
        self.accounting_supplier_party = accounting_supplier_party
        self.accounting_customer_party = accounting_customer_party
        self.legal_monetary_total = legal_monetary_total
        if not invoice_line:
            raise ListMustNotBeEmptyException('invoice_line')
        self.invoice_line = invoice_line  # List (at least 1)
        self.ubl_extensions = ubl_extensions
        self.ubl_version_id = ubl_version_id
        self.customization_id = customization_id
        self.profile_id = profile_id
        self.profile_execution_id = profile_execution_id
        self.copy_indicator = copy_indicator
        self.uuid = uuid
        self.issue_time = issue_time
        self.due_date = due_date
        self.invoice_type_code = invoice_type_code
        self.note = note  # List
        self.tax_point_date = tax_point_date
        self.document_currency_code = document_currency_code
        self.pricing_currency_code = pricing_currency_code
        self.payment_currency_code = payment_currency_code
        self.payment_alternative_currency_code = payment_alternative_currency_code
        self.accounting_cost_code = accounting_cost_code
        self.accounting_cost = accounting_cost
        self.line_count_numeric = line_count_numeric
        self.buyer_reference = buyer_reference
        self.invoice_period = invoice_period  # List
        self.order_reference = order_reference
        self.billing_reference = billing_reference  # List
        self.despatch_document_reference = despatch_document_reference  # List
        self.receipt_document_reference = receipt_document_reference  # List
        self.statement_document_reference = statement_document_reference  # List
        self.originator_document_reference = originator_document_reference  # List
        self.contract_document_reference = contract_document_reference  # List
        self.additional_document_reference = additional_document_reference  # List
        self.project_reference = project_reference  # List
        self.signature = signature  # List
        self.payee_party = payee_party
        self.buyer_customer_party = buyer_customer_party
        self.seller_supplier_party = seller_supplier_party
        self.tax_representative_party = tax_representative_party
        self.delivery = delivery  # List
        self.delivery_terms = delivery_terms
        self.payment_means = payment_means  # List
        self.payment_terms = payment_terms  # List
        self.prepaid_payment = prepaid_payment  # List
        self.allowance_charge = allowance_charge  # List
        self.tax_exchange_rate = tax_exchange_rate
        self.pricing_exchange_rate = pricing_exchange_rate
        self.payment_exchange_rate = payment_exchange_rate
        self.payment_alternative_exchange_rate = payment_alternative_exchange_rate
        self.tax_total = tax_total  # List
        self.withholding_tax_total = withholding_tax_total  # List

    def __str__(self):
        tag = self.get_tag()
        namespaces = ''
        if self.xml_namespaces is not None:
            for ns in self.xml_namespaces:
                namespaces += f' {ns}'

        return f'<{tag}{namespaces}>{self.get_value()}</{tag}>'

    def to_file(self):
        full_file = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>{self}'
        return full_file
        
