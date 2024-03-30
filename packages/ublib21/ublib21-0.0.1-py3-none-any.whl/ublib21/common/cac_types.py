from typing import List
from ublib21.common import cbc
from ublib21.common.cac import *
from ublib21.base import ComplexXMLParseableObject


class ListMustNotBeEmptyException(Exception):
    pass


class PrefixCAC:
    prefix = 'cac'


class __ActivityDataLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    supply_chain_activity_type_code = None
    activity_origin_location = None
    buyer_customer_party = None
    seller_supplier_party = None
    activity_period = None
    activity_final_location = None
    sales_item = None
    order_list = [
        'id_',
        'supply_chain_activity_type_code',
        'buyer_customer_party',
        'seller_supplier_party',
        'activity_period',
        'activity_origin_location',
        'activity_final_location',
        'sales_item',
    ]

    def __init__(self,		id_: cbc.ID,
                 supply_chain_activity_type_code: cbc.SupplyChainActivityTypeCode,
                 activity_origin_location: 'ActivityOriginLocation',
                 buyer_customer_party: 'BuyerCustomerParty' = None,
                 seller_supplier_party: 'SellerSupplierParty' = None,
                 activity_period: 'ActivityPeriod' = None,
                 activity_final_location: 'ActivityFinalLocation' = None,
                 sales_item: List['SalesItem'] = None, xml_namespaces=None):
        if not sales_item:
            raise ListMustNotBeEmptyException('sales_item')
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.supply_chain_activity_type_code = supply_chain_activity_type_code
        self.activity_origin_location = activity_origin_location
        self.buyer_customer_party = buyer_customer_party
        self.seller_supplier_party = seller_supplier_party
        self.activity_period = activity_period
        self.activity_final_location = activity_final_location
        self.sales_item = sales_item


class __ActivityPropertyType(PrefixCAC, ComplexXMLParseableObject):
    name = None
    value = None
    order_list = [
        'name',
        'value',
    ]
    def __init__(self,		name: cbc.Name,
                 value: cbc.Value, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.name = name
        self.value = value


class __AddressType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    address_type_code = None
    address_format_code = None
    postbox = None
    floor = None
    room = None
    street_name = None
    additional_street_name = None
    block_name = None
    building_name = None
    building_number = None
    inhouse_mail = None
    department = None
    mark_attention = None
    mark_care = None
    plot_identification = None
    city_subdivision_name = None
    city_name = None
    postal_zone = None
    country_subentity = None
    country_subentity_code = None
    region = None
    district = None
    timezone_offset = None
    address_line = None
    country = None
    location_coordinate = None
    order_list = [
        'id_',
        'address_type_code',
        'address_format_code',
        'postbox',
        'floor',
        'room',
        'street_name',
        'additional_street_name',
        'block_name',
        'building_name',
        'building_number',
        'inhouse_mail',
        'department',
        'mark_attention',
        'mark_care',
        'plot_identification',
        'city_subdivision_name',
        'city_name',
        'postal_zone',
        'country_subentity',
        'country_subentity_code',
        'region',
        'district',
        'timezone_offset',
        'address_line',
        'country',
        'location_coordinate',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 address_type_code: cbc.AddressTypeCode = None,
                 address_format_code: cbc.AddressFormatCode = None,
                 postbox: cbc.Postbox = None,
                 floor: cbc.Floor = None,
                 room: cbc.Room = None,
                 street_name: cbc.StreetName = None,
                 additional_street_name: cbc.AdditionalStreetName = None,
                 block_name: cbc.BlockName = None,
                 building_name: cbc.BuildingName = None,
                 building_number: cbc.BuildingNumber = None,
                 inhouse_mail: cbc.InhouseMail = None,
                 department: cbc.Department = None,
                 mark_attention: cbc.MarkAttention = None,
                 mark_care: cbc.MarkCare = None,
                 plot_identification: cbc.PlotIdentification = None,
                 city_subdivision_name: cbc.CitySubdivisionName = None,
                 city_name: cbc.CityName = None,
                 postal_zone: cbc.PostalZone = None,
                 country_subentity: cbc.CountrySubentity = None,
                 country_subentity_code: cbc.CountrySubentityCode = None,
                 region: cbc.Region = None,
                 district: cbc.District = None,
                 timezone_offset: cbc.TimezoneOffset = None,
                 address_line: List['AddressLine'] = None,
                 country: 'Country' = None,
                 location_coordinate: List['LocationCoordinate'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.address_type_code = address_type_code
        self.address_format_code = address_format_code
        self.postbox = postbox
        self.floor = floor
        self.room = room
        self.street_name = street_name
        self.additional_street_name = additional_street_name
        self.block_name = block_name
        self.building_name = building_name
        self.building_number = building_number
        self.inhouse_mail = inhouse_mail
        self.department = department
        self.mark_attention = mark_attention
        self.mark_care = mark_care
        self.plot_identification = plot_identification
        self.city_subdivision_name = city_subdivision_name
        self.city_name = city_name
        self.postal_zone = postal_zone
        self.country_subentity = country_subentity
        self.country_subentity_code = country_subentity_code
        self.region = region
        self.district = district
        self.timezone_offset = timezone_offset
        self.address_line = address_line
        self.country = country
        self.location_coordinate = location_coordinate


class __AddressLineType(PrefixCAC, ComplexXMLParseableObject):
    line = None
    order_list = [
        'line',
    ]

    def __init__(self,		line: cbc.Line, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.line = line


class __AirTransportType(PrefixCAC, ComplexXMLParseableObject):
    aircraft_id = None
    order_list = [
        'aircraft_id',
    ]

    def __init__(self,		aircraft_id: cbc.AircraftID, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.aircraft_id = aircraft_id


class __AllowanceChargeType(PrefixCAC, ComplexXMLParseableObject):
    charge_indicator = None
    amount = None
    id_ = None
    allowance_charge_reason_code = None
    allowance_charge_reason = None
    multiplier_factor_numeric = None
    prepaid_indicator = None
    sequence_numeric = None
    base_amount = None
    accounting_cost_code = None
    accounting_cost = None
    per_unit_amount = None
    tax_category = None
    tax_total = None
    payment_means = None
    order_list = [
        'id_',
        'charge_indicator',
        'allowance_charge_reason_code',
        'allowance_charge_reason',
        'multiplier_factor_numeric',
        'prepaid_indicator',
        'sequence_numeric',
        'amount',
        'base_amount',
        'accounting_cost_code',
        'accounting_cost',
        'per_unit_amount',
        'tax_category',
        'tax_total',
        'payment_means',
    ]

    def __init__(self,		charge_indicator: cbc.ChargeIndicator,
                 amount: cbc.Amount,
                 id_: cbc.ID = None,
                 allowance_charge_reason_code: cbc.AllowanceChargeReasonCode = None,
                 allowance_charge_reason: List[cbc.AllowanceChargeReason] = None,
                 multiplier_factor_numeric: cbc.MultiplierFactorNumeric = None,
                 prepaid_indicator: cbc.PrepaidIndicator = None,
                 sequence_numeric: cbc.SequenceNumeric = None,
                 base_amount: cbc.BaseAmount = None,
                 accounting_cost_code: cbc.AccountingCostCode = None,
                 accounting_cost: cbc.AccountingCost = None,
                 per_unit_amount: cbc.PerUnitAmount = None,
                 tax_category: List['TaxCategory'] = None,
                 tax_total: 'TaxTotal' = None,
                 payment_means: List['PaymentMeans'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.charge_indicator = charge_indicator
        self.amount = amount
        self.id_ = id_
        self.allowance_charge_reason_code = allowance_charge_reason_code
        self.allowance_charge_reason = allowance_charge_reason
        self.multiplier_factor_numeric = multiplier_factor_numeric
        self.prepaid_indicator = prepaid_indicator
        self.sequence_numeric = sequence_numeric
        self.base_amount = base_amount
        self.accounting_cost_code = accounting_cost_code
        self.accounting_cost = accounting_cost
        self.per_unit_amount = per_unit_amount
        self.tax_category = tax_category
        self.tax_total = tax_total
        self.payment_means = payment_means


class __AppealTermsType(PrefixCAC, ComplexXMLParseableObject):
    description = None
    presentation_period = None
    appeal_information_party = None
    appeal_receiver_party = None
    mediation_party = None
    order_list = [
        'description',
        'presentation_period',
        'appeal_information_party',
        'appeal_receiver_party',
        'mediation_party',
    ]

    def __init__(self,		description: List[cbc.Description] = None,
                 presentation_period: 'PresentationPeriod' = None,
                 appeal_information_party: 'AppealInformationParty' = None,
                 appeal_receiver_party: 'AppealReceiverParty' = None,
                 mediation_party: 'MediationParty' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.description = description
        self.presentation_period = presentation_period
        self.appeal_information_party = appeal_information_party
        self.appeal_receiver_party = appeal_receiver_party
        self.mediation_party = mediation_party


class __AttachmentType(PrefixCAC, ComplexXMLParseableObject):
    embedded_document_binary_object = None
    external_reference = None
    order_list = [
        'embedded_document_binary_object',
        'external_reference',
    ]
    def __init__(self,		embedded_document_binary_object: cbc.EmbeddedDocumentBinaryObject = None,
                 external_reference: 'ExternalReference' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.embedded_document_binary_object = embedded_document_binary_object
        self.external_reference = external_reference


class __AuctionTermsType(PrefixCAC, ComplexXMLParseableObject):
    auction_constraint_indicator = None
    justification_description = None
    description = None
    process_description = None
    conditions_description = None
    electronic_device_description = None
    auction_uri = None
    order_list = [
        'auction_constraint_indicator',
        'justification_description',
        'description',
        'process_description',
        'conditions_description',
        'electronic_device_description',
        'auction_uri',
    ]

    def __init__(self,		auction_constraint_indicator: cbc.AuctionConstraintIndicator = None,
                 justification_description: List[cbc.JustificationDescription] = None,
                 description: List[cbc.Description] = None,
                 process_description: List[cbc.ProcessDescription] = None,
                 conditions_description: List[cbc.ConditionsDescription] = None,
                 electronic_device_description: List[cbc.ElectronicDeviceDescription] = None,
                 auction_uri: cbc.AuctionURI = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.auction_constraint_indicator = auction_constraint_indicator
        self.justification_description = justification_description
        self.description = description
        self.process_description = process_description
        self.conditions_description = conditions_description
        self.electronic_device_description = electronic_device_description
        self.auction_uri = auction_uri


class __AwardingCriterionType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    awarding_criterion_type_code = None
    description = None
    weight_numeric = None
    weight = None
    calculation_expression = None
    calculation_expression_code = None
    minimum_quantity = None
    maximum_quantity = None
    minimum_amount = None
    maximum_amount = None
    minimum_improvement_bid = None
    subordinate_awarding_criterion = None
    order_list = [
        'id_',
        'awarding_criterion_type_code',
        'description',
        'weight_numeric',
        'weight',
        'calculation_expression',
        'calculation_expression_code',
        'minimum_quantity',
        'maximum_quantity',
        'minimum_amount',
        'maximum_amount',
        'minimum_improvement_bid',
        'subordinate_awarding_criterion',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 awarding_criterion_type_code: cbc.AwardingCriterionTypeCode = None,
                 description: List[cbc.Description] = None,
                 weight_numeric: cbc.WeightNumeric = None,
                 weight: List[cbc.Weight] = None,
                 calculation_expression: List[cbc.CalculationExpression] = None,
                 calculation_expression_code: cbc.CalculationExpressionCode = None,
                 minimum_quantity: cbc.MinimumQuantity = None,
                 maximum_quantity: cbc.MaximumQuantity = None,
                 minimum_amount: cbc.MinimumAmount = None,
                 maximum_amount: cbc.MaximumAmount = None,
                 minimum_improvement_bid: List[cbc.MinimumImprovementBid] = None,
                 subordinate_awarding_criterion: List['SubordinateAwardingCriterion'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.awarding_criterion_type_code = awarding_criterion_type_code
        self.description = description
        self.weight_numeric = weight_numeric
        self.weight = weight
        self.calculation_expression = calculation_expression
        self.calculation_expression_code = calculation_expression_code
        self.minimum_quantity = minimum_quantity
        self.maximum_quantity = maximum_quantity
        self.minimum_amount = minimum_amount
        self.maximum_amount = maximum_amount
        self.minimum_improvement_bid = minimum_improvement_bid
        self.subordinate_awarding_criterion = subordinate_awarding_criterion


class __AwardingCriterionResponseType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    awarding_criterion_id = None
    awarding_criterion_description = None
    description = None
    quantity = None
    amount = None
    subordinate_awarding_criterion_response = None
    order_list = [
        'id_',
        'awarding_criterion_id',
        'awarding_criterion_description',
        'description',
        'quantity',
        'amount',
        'subordinate_awarding_criterion_response',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 awarding_criterion_id: cbc.AwardingCriterionID = None,
                 awarding_criterion_description: List[cbc.AwardingCriterionDescription] = None,
                 description: List[cbc.Description] = None,
                 quantity: cbc.Quantity = None,
                 amount: cbc.Amount = None,
                 subordinate_awarding_criterion_response: List['SubordinateAwardingCriterionResponse'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.awarding_criterion_id = awarding_criterion_id
        self.awarding_criterion_description = awarding_criterion_description
        self.description = description
        self.quantity = quantity
        self.amount = amount
        self.subordinate_awarding_criterion_response = subordinate_awarding_criterion_response


class __AwardingTermsType(PrefixCAC, ComplexXMLParseableObject):
    weighting_algorithm_code = None
    description = None
    technical_committee_description = None
    low_tenders_description = None
    prize_indicator = None
    prize_description = None
    payment_description = None
    followup_contract_indicator = None
    binding_on_buyer_indicator = None
    awarding_criterion = None
    technical_committee_person = None
    order_list = [
        'weighting_algorithm_code',
        'description',
        'technical_committee_description',
        'low_tenders_description',
        'prize_indicator',
        'prize_description',
        'payment_description',
        'followup_contract_indicator',
        'binding_on_buyer_indicator',
        'awarding_criterion',
        'technical_committee_person',
    ]

    def __init__(self,		weighting_algorithm_code: cbc.WeightingAlgorithmCode = None,
                 description: List[cbc.Description] = None,
                 technical_committee_description: List[cbc.TechnicalCommitteeDescription] = None,
                 low_tenders_description: List[cbc.LowTendersDescription] = None,
                 prize_indicator: cbc.PrizeIndicator = None,
                 prize_description: List[cbc.PrizeDescription] = None,
                 payment_description: List[cbc.PaymentDescription] = None,
                 followup_contract_indicator: cbc.FollowupContractIndicator = None,
                 binding_on_buyer_indicator: cbc.BindingOnBuyerIndicator = None,
                 awarding_criterion: List['AwardingCriterion'] = None,
                 technical_committee_person: List['TechnicalCommitteePerson'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.weighting_algorithm_code = weighting_algorithm_code
        self.description = description
        self.technical_committee_description = technical_committee_description
        self.low_tenders_description = low_tenders_description
        self.prize_indicator = prize_indicator
        self.prize_description = prize_description
        self.payment_description = payment_description
        self.followup_contract_indicator = followup_contract_indicator
        self.binding_on_buyer_indicator = binding_on_buyer_indicator
        self.awarding_criterion = awarding_criterion
        self.technical_committee_person = technical_committee_person


class __BillingReferenceType(PrefixCAC, ComplexXMLParseableObject):
    invoice_document_reference = None
    self_billed_invoice_document_reference = None
    credit_note_document_reference = None
    self_billed_credit_note_document_reference = None
    debit_note_document_reference = None
    reminder_document_reference = None
    additional_document_reference = None
    billing_reference_line = None
    order_list = [
        'invoice_document_reference',
        'self_billed_invoice_document_reference',
        'credit_note_document_reference',
        'self_billed_credit_note_document_reference',
        'debit_note_document_reference',
        'reminder_document_reference',
        'additional_document_reference',
        'billing_reference_line',
    ]

    def __init__(self,		invoice_document_reference: 'InvoiceDocumentReference' = None,
                 self_billed_invoice_document_reference: 'SelfBilledInvoiceDocumentReference' = None,
                 credit_note_document_reference: 'CreditNoteDocumentReference' = None,
                 self_billed_credit_note_document_reference: 'SelfBilledCreditNoteDocumentReference' = None,
                 debit_note_document_reference: 'DebitNoteDocumentReference' = None,
                 reminder_document_reference: 'ReminderDocumentReference' = None,
                 additional_document_reference: 'AdditionalDocumentReference' = None,
                 billing_reference_line: List['BillingReferenceLine'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.invoice_document_reference = invoice_document_reference
        self.self_billed_invoice_document_reference = self_billed_invoice_document_reference
        self.credit_note_document_reference = credit_note_document_reference
        self.self_billed_credit_note_document_reference = self_billed_credit_note_document_reference
        self.debit_note_document_reference = debit_note_document_reference
        self.reminder_document_reference = reminder_document_reference
        self.additional_document_reference = additional_document_reference
        self.billing_reference_line = billing_reference_line


class __BillingReferenceLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    amount = None
    allowance_charge = None
    order_list = [
        'id_',
        'amount',
        'allowance_charge',
    ]

    def __init__(self,		id_: cbc.ID,
                 amount: cbc.Amount = None,
                 allowance_charge: List['AllowanceCharge'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.amount = amount
        self.allowance_charge = allowance_charge


class __BranchType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    name = None
    financial_institution = None
    address = None
    order_list = [
        'id_',
        'name',
        'financial_institution',
        'address',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 name: cbc.Name = None,
                 financial_institution: 'FinancialInstitution' = None,
                 address: 'Address' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.name = name
        self.financial_institution = financial_institution
        self.address = address


class __BudgetAccountType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    budget_year_numeric = None
    required_classification_scheme = None
    order_list = [
        'id_',
        'budget_year_numeric',
        'required_classification_scheme',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 budget_year_numeric: cbc.BudgetYearNumeric = None,
                 required_classification_scheme: 'RequiredClassificationScheme' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.budget_year_numeric = budget_year_numeric
        self.required_classification_scheme = required_classification_scheme


class __BudgetAccountLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    total_amount = None
    budget_account = None
    order_list = [
        'id_',
        'total_amount',
        'budget_account',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 total_amount: cbc.TotalAmount = None,
                 budget_account: List['BudgetAccount'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.total_amount = total_amount
        self.budget_account = budget_account


class __CapabilityType(PrefixCAC, ComplexXMLParseableObject):
    capability_type_code = None
    description = None
    value_amount = None
    value_quantity = None
    evidence_supplied = None
    validity_period = None
    order_list = [
        'capability_type_code',
        'description',
        'value_amount',
        'value_quantity',
        'evidence_supplied',
        'validity_period',
    ]

    def __init__(self,		capability_type_code: cbc.CapabilityTypeCode = None,
                 description: List[cbc.Description] = None,
                 value_amount: cbc.ValueAmount = None,
                 value_quantity: cbc.ValueQuantity = None,
                 evidence_supplied: List['EvidenceSupplied'] = None,
                 validity_period: 'ValidityPeriod' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.capability_type_code = capability_type_code
        self.description = description
        self.value_amount = value_amount
        self.value_quantity = value_quantity
        self.evidence_supplied = evidence_supplied
        self.validity_period = validity_period


class __CardAccountType(PrefixCAC, ComplexXMLParseableObject):
    primary_account_number_id = None
    network_id = None
    card_type_code = None
    validity_start_date = None
    expiry_date = None
    issuer_id = None
    issue_number_id = None
    cv2_id = None
    card_chip_code = None
    chip_application_id = None
    holder_name = None
    order_list = [
        'primary_account_number_id',
        'network_id',
        'card_type_code',
        'validity_start_date',
        'expiry_date',
        'issuer_id',
        'issue_number_id',
        'cv2_id',
        'card_chip_code',
        'chip_application_id',
        'holder_name',
    ]

    def __init__(self,		primary_account_number_id: cbc.PrimaryAccountNumberID,
                 network_id: cbc.NetworkID,
                 card_type_code: cbc.CardTypeCode = None,
                 validity_start_date: cbc.ValidityStartDate = None,
                 expiry_date: cbc.ExpiryDate = None,
                 issuer_id: cbc.IssuerID = None,
                 issue_number_id: cbc.IssueNumberID = None,
                 cv2_id: cbc.CV2ID = None,
                 card_chip_code: cbc.CardChipCode = None,
                 chip_application_id: cbc.ChipApplicationID = None,
                 holder_name: cbc.HolderName = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.primary_account_number_id = primary_account_number_id
        self.network_id = network_id
        self.card_type_code = card_type_code
        self.validity_start_date = validity_start_date
        self.expiry_date = expiry_date
        self.issuer_id = issuer_id
        self.issue_number_id = issue_number_id
        self.cv2_id = cv2_id
        self.card_chip_code = card_chip_code
        self.chip_application_id = chip_application_id
        self.holder_name = holder_name


class __CatalogueItemSpecificationUpdateLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    item = None
    contractor_customer_party = None
    seller_supplier_party = None
    order_list = [
        'id_',
        'contractor_customer_party',
        'seller_supplier_party',
        'item',
    ]

    def __init__(self,		id_: cbc.ID,
                 item: 'Item',
                 contractor_customer_party: 'ContractorCustomerParty' = None,
                 seller_supplier_party: 'SellerSupplierParty' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.item = item
        self.contractor_customer_party = contractor_customer_party
        self.seller_supplier_party = seller_supplier_party


class __CatalogueLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    item = None
    action_code = None
    life_cycle_status_code = None
    contract_subdivision = None
    note = None
    orderable_indicator = None
    orderable_unit = None
    content_unit_quantity = None
    order_quantity_increment_numeric = None
    minimum_order_quantity = None
    maximum_order_quantity = None
    warranty_information = None
    pack_level_code = None
    contractor_customer_party = None
    seller_supplier_party = None
    warranty_party = None
    warranty_validity_period = None
    line_validity_period = None
    item_comparison = None
    component_related_item = None
    accessory_related_item = None
    required_related_item = None
    replacement_related_item = None
    complementary_related_item = None
    replaced_related_item = None
    required_item_location_quantity = None
    document_reference = None
    keyword_item_property = None
    call_for_tenders_line_reference = None
    call_for_tenders_document_reference = None
    order_list = [
        'id_',
        'action_code',
        'life_cycle_status_code',
        'contract_subdivision',
        'note',
        'orderable_indicator',
        'orderable_unit',
        'content_unit_quantity',
        'order_quantity_increment_numeric',
        'minimum_order_quantity',
        'maximum_order_quantity',
        'warranty_information',
        'pack_level_code',
        'contractor_customer_party',
        'seller_supplier_party',
        'warranty_party',
        'warranty_validity_period',
        'line_validity_period',
        'item_comparison',
        'component_related_item',
        'accessory_related_item',
        'required_related_item',
        'replacement_related_item',
        'complementary_related_item',
        'replaced_related_item',
        'required_item_location_quantity',
        'document_reference',
        'item',
        'keyword_item_property',
        'call_for_tenders_line_reference',
        'call_for_tenders_document_reference',
    ]

    def __init__(self,		id_: cbc.ID,
                 item: 'Item',
                 action_code: cbc.ActionCode = None,
                 life_cycle_status_code: cbc.LifeCycleStatusCode = None,
                 contract_subdivision: cbc.ContractSubdivision = None,
                 note: List[cbc.Note] = None,
                 orderable_indicator: cbc.OrderableIndicator = None,
                 orderable_unit: cbc.OrderableUnit = None,
                 content_unit_quantity: cbc.ContentUnitQuantity = None,
                 order_quantity_increment_numeric: cbc.OrderQuantityIncrementNumeric = None,
                 minimum_order_quantity: cbc.MinimumOrderQuantity = None,
                 maximum_order_quantity: cbc.MaximumOrderQuantity = None,
                 warranty_information: List[cbc.WarrantyInformation] = None,
                 pack_level_code: cbc.PackLevelCode = None,
                 contractor_customer_party: 'ContractorCustomerParty' = None,
                 seller_supplier_party: 'SellerSupplierParty' = None,
                 warranty_party: 'WarrantyParty' = None,
                 warranty_validity_period: 'WarrantyValidityPeriod' = None,
                 line_validity_period: 'LineValidityPeriod' = None,
                 item_comparison: List['ItemComparison'] = None,
                 component_related_item: List['ComponentRelatedItem'] = None,
                 accessory_related_item: List['AccessoryRelatedItem'] = None,
                 required_related_item: List['RequiredRelatedItem'] = None,
                 replacement_related_item: List['ReplacementRelatedItem'] = None,
                 complementary_related_item: List['ComplementaryRelatedItem'] = None,
                 replaced_related_item: List['ReplacedRelatedItem'] = None,
                 required_item_location_quantity: List['RequiredItemLocationQuantity'] = None,
                 document_reference: List['DocumentReference'] = None,
                 keyword_item_property: List['KeywordItemProperty'] = None,
                 call_for_tenders_line_reference: 'CallForTendersLineReference' = None,
                 call_for_tenders_document_reference: 'CallForTendersDocumentReference' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.item = item
        self.action_code = action_code
        self.life_cycle_status_code = life_cycle_status_code
        self.contract_subdivision = contract_subdivision
        self.note = note
        self.orderable_indicator = orderable_indicator
        self.orderable_unit = orderable_unit
        self.content_unit_quantity = content_unit_quantity
        self.order_quantity_increment_numeric = order_quantity_increment_numeric
        self.minimum_order_quantity = minimum_order_quantity
        self.maximum_order_quantity = maximum_order_quantity
        self.warranty_information = warranty_information
        self.pack_level_code = pack_level_code
        self.contractor_customer_party = contractor_customer_party
        self.seller_supplier_party = seller_supplier_party
        self.warranty_party = warranty_party
        self.warranty_validity_period = warranty_validity_period
        self.line_validity_period = line_validity_period
        self.item_comparison = item_comparison
        self.component_related_item = component_related_item
        self.accessory_related_item = accessory_related_item
        self.required_related_item = required_related_item
        self.replacement_related_item = replacement_related_item
        self.complementary_related_item = complementary_related_item
        self.replaced_related_item = replaced_related_item
        self.required_item_location_quantity = required_item_location_quantity
        self.document_reference = document_reference
        self.keyword_item_property = keyword_item_property
        self.call_for_tenders_line_reference = call_for_tenders_line_reference
        self.call_for_tenders_document_reference = call_for_tenders_document_reference


class __CataloguePricingUpdateLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    contractor_customer_party = None
    seller_supplier_party = None
    required_item_location_quantity = None
    order_list = [
        'id_',
        'contractor_customer_party',
        'seller_supplier_party',
        'required_item_location_quantity',
    ]

    def __init__(self,		id_: cbc.ID,
                 contractor_customer_party: 'ContractorCustomerParty' = None,
                 seller_supplier_party: 'SellerSupplierParty' = None,
                 required_item_location_quantity: List['RequiredItemLocationQuantity'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.contractor_customer_party = contractor_customer_party
        self.seller_supplier_party = seller_supplier_party
        self.required_item_location_quantity = required_item_location_quantity


class __CatalogueReferenceType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    uuid = None
    issue_date = None
    issue_time = None
    revision_date = None
    revision_time = None
    note = None
    description = None
    version_id = None
    previous_version_id = None
    order_list = [
        'id_',
        'uuid',
        'issue_date',
        'issue_time',
        'revision_date',
        'revision_time',
        'note',
        'description',
        'version_id',
        'previous_version_id',
    ]

    def __init__(self,		id_: cbc.ID,
                 uuid: cbc.UUID = None,
                 issue_date: cbc.IssueDate = None,
                 issue_time: cbc.IssueTime = None,
                 revision_date: cbc.RevisionDate = None,
                 revision_time: cbc.RevisionTime = None,
                 note: List[cbc.Note] = None,
                 description: List[cbc.Description] = None,
                 version_id: cbc.VersionID = None,
                 previous_version_id: cbc.PreviousVersionID = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.uuid = uuid
        self.issue_date = issue_date
        self.issue_time = issue_time
        self.revision_date = revision_date
        self.revision_time = revision_time
        self.note = note
        self.description = description
        self.version_id = version_id
        self.previous_version_id = previous_version_id


class __CatalogueRequestLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    item = None
    contract_subdivision = None
    note = None
    line_validity_period = None
    required_item_location_quantity = None
    order_list = [
        'id_',
        'contract_subdivision',
        'note',
        'line_validity_period',
        'required_item_location_quantity',
        'item',
    ]

    def __init__(self,		id_: cbc.ID,
                 item: 'Item',
                 contract_subdivision: cbc.ContractSubdivision = None,
                 note: List[cbc.Note] = None,
                 line_validity_period: 'LineValidityPeriod' = None,
                 required_item_location_quantity: List['RequiredItemLocationQuantity'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.item = item
        self.contract_subdivision = contract_subdivision
        self.note = note
        self.line_validity_period = line_validity_period
        self.required_item_location_quantity = required_item_location_quantity


class __CertificateType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    certificate_type_code = None
    certificate_type = None
    issuer_party = None
    remarks = None
    document_reference = None
    signature = None
    order_list = [
        'id_',
        'certificate_type_code',
        'certificate_type',
        'remarks',
        'issuer_party',
        'document_reference',
        'signature',
    ]

    def __init__(self,		id_: cbc.ID,
                 certificate_type_code: cbc.CertificateTypeCode,
                 certificate_type: cbc.CertificateType,
                 issuer_party: 'IssuerParty',
                 remarks: List[cbc.Remarks] = None,
                 document_reference: List['DocumentReference'] = None,
                 signature: List['Signature'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.certificate_type_code = certificate_type_code
        self.certificate_type = certificate_type
        self.issuer_party = issuer_party
        self.remarks = remarks
        self.document_reference = document_reference
        self.signature = signature


class __CertificateOfOriginApplicationType(PrefixCAC, ComplexXMLParseableObject):
    reference_id = None
    certificate_type = None
    original_job_id = None
    shipment = None
    preparation_party = None
    issuer_party = None
    issuing_country = None
    application_status_code = None
    previous_job_id = None
    remarks = None
    endorser_party = None
    exporter_party = None
    importer_party = None
    document_distribution = None
    supporting_document_reference = None
    signature = None
    order_list = [
        'reference_id',
        'certificate_type',
        'application_status_code',
        'original_job_id',
        'previous_job_id',
        'remarks',
        'shipment',
        'endorser_party',
        'preparation_party',
        'issuer_party',
        'exporter_party',
        'importer_party',
        'issuing_country',
        'document_distribution',
        'supporting_document_reference',
        'signature',
    ]

    def __init__(self,		reference_id: cbc.ReferenceID,
                 certificate_type: cbc.CertificateType,
                 original_job_id: cbc.OriginalJobID,
                 shipment: 'Shipment',
                 preparation_party: 'PreparationParty',
                 issuer_party: 'IssuerParty',
                 issuing_country: 'IssuingCountry',
                 application_status_code: cbc.ApplicationStatusCode = None,
                 previous_job_id: cbc.PreviousJobID = None,
                 remarks: List[cbc.Remarks] = None,
                 endorser_party: List['EndorserParty'] = None,
                 exporter_party: 'ExporterParty' = None,
                 importer_party: 'ImporterParty' = None,
                 document_distribution: List['DocumentDistribution'] = None,
                 supporting_document_reference: List['SupportingDocumentReference'] = None,
                 signature: List['Signature'] = None, xml_namespaces=None):
        if not endorser_party:
            raise ListMustNotBeEmptyException('endorser_party')
        super().__init__(xml_namespaces)
        self.reference_id = reference_id
        self.certificate_type = certificate_type
        self.original_job_id = original_job_id
        self.shipment = shipment
        self.preparation_party = preparation_party
        self.issuer_party = issuer_party
        self.issuing_country = issuing_country
        self.application_status_code = application_status_code
        self.previous_job_id = previous_job_id
        self.remarks = remarks
        self.endorser_party = endorser_party
        self.exporter_party = exporter_party
        self.importer_party = importer_party
        self.document_distribution = document_distribution
        self.supporting_document_reference = supporting_document_reference
        self.signature = signature


class __ClassificationCategoryType(PrefixCAC, ComplexXMLParseableObject):
    name = None
    code_value = None
    description = None
    categorizes_classification_category = None
    order_list = [
        'name',
        'code_value',
        'description',
        'categorizes_classification_category',
    ]

    def __init__(self,		name: cbc.Name = None,
                 code_value: cbc.CodeValue = None,
                 description: List[cbc.Description] = None,
                 categorizes_classification_category: List['CategorizesClassificationCategory'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.name = name
        self.code_value = code_value
        self.description = description
        self.categorizes_classification_category = categorizes_classification_category


class __ClassificationSchemeType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    uuid = None
    last_revision_date = None
    last_revision_time = None
    note = None
    name = None
    description = None
    agency_id = None
    agency_name = None
    version_id = None
    uri = None
    scheme_uri = None
    language_id = None
    classification_category = None
    order_list = [
        'id_',
        'uuid',
        'last_revision_date',
        'last_revision_time',
        'note',
        'name',
        'description',
        'agency_id',
        'agency_name',
        'version_id',
        'uri',
        'scheme_uri',
        'language_id',
        'classification_category',
    ]

    def __init__(self,		id_: cbc.ID,
                 uuid: cbc.UUID = None,
                 last_revision_date: cbc.LastRevisionDate = None,
                 last_revision_time: cbc.LastRevisionTime = None,
                 note: List[cbc.Note] = None,
                 name: cbc.Name = None,
                 description: List[cbc.Description] = None,
                 agency_id: cbc.AgencyID = None,
                 agency_name: cbc.AgencyName = None,
                 version_id: cbc.VersionID = None,
                 uri: cbc.URI = None,
                 scheme_uri: cbc.SchemeURI = None,
                 language_id: cbc.LanguageID = None,
                 classification_category: List['ClassificationCategory'] = None, xml_namespaces=None):
        if not classification_category:
            raise ListMustNotBeEmptyException('classification_category')
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.uuid = uuid
        self.last_revision_date = last_revision_date
        self.last_revision_time = last_revision_time
        self.note = note
        self.name = name
        self.description = description
        self.agency_id = agency_id
        self.agency_name = agency_name
        self.version_id = version_id
        self.uri = uri
        self.scheme_uri = scheme_uri
        self.language_id = language_id
        self.classification_category = classification_category


class __ClauseType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    content = None
    order_list = [
        'id_',
        'content',
    ]
    def __init__(self,		id_: cbc.ID = None,
                 content: List[cbc.Content] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.content = content


class __CommodityClassificationType(PrefixCAC, ComplexXMLParseableObject):
    nature_code = None
    cargo_type_code = None
    commodity_code = None
    item_classification_code = None
    order_list = [
        'nature_code',
        'cargo_type_code',
        'commodity_code',
        'item_classification_code',
    ]

    def __init__(self,		nature_code: cbc.NatureCode = None,
                 cargo_type_code: cbc.CargoTypeCode = None,
                 commodity_code: cbc.CommodityCode = None,
                 item_classification_code: cbc.ItemClassificationCode = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.nature_code = nature_code
        self.cargo_type_code = cargo_type_code
        self.commodity_code = commodity_code
        self.item_classification_code = item_classification_code


class __CommunicationType(PrefixCAC, ComplexXMLParseableObject):
    channel_code = None
    channel = None
    value = None
    order_list = [
        'channel_code',
        'channel',
        'value',
    ]

    def __init__(self,		channel_code: cbc.ChannelCode = None,
                 channel: cbc.Channel = None,
                 value: cbc.Value = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.channel_code = channel_code
        self.channel = channel
        self.value = value


class __CompletedTaskType(PrefixCAC, ComplexXMLParseableObject):
    annual_average_amount = None
    total_task_amount = None
    party_capacity_amount = None
    description = None
    evidence_supplied = None
    period = None
    recipient_customer_party = None
    order_list = [
        'annual_average_amount',
        'total_task_amount',
        'party_capacity_amount',
        'description',
        'evidence_supplied',
        'period',
        'recipient_customer_party',
    ]

    def __init__(self,		annual_average_amount: cbc.AnnualAverageAmount = None,
                 total_task_amount: cbc.TotalTaskAmount = None,
                 party_capacity_amount: cbc.PartyCapacityAmount = None,
                 description: List[cbc.Description] = None,
                 evidence_supplied: List['EvidenceSupplied'] = None,
                 period: 'Period' = None,
                 recipient_customer_party: 'RecipientCustomerParty' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.annual_average_amount = annual_average_amount
        self.total_task_amount = total_task_amount
        self.party_capacity_amount = party_capacity_amount
        self.description = description
        self.evidence_supplied = evidence_supplied
        self.period = period
        self.recipient_customer_party = recipient_customer_party


class __ConditionType(PrefixCAC, ComplexXMLParseableObject):
    attribute_id = None
    measure = None
    description = None
    minimum_measure = None
    maximum_measure = None
    order_list = [
        'attribute_id',
        'measure',
        'description',
        'minimum_measure',
        'maximum_measure',
    ]

    def __init__(self,		attribute_id: cbc.AttributeID,
                 measure: cbc.Measure = None,
                 description: List[cbc.Description] = None,
                 minimum_measure: cbc.MinimumMeasure = None,
                 maximum_measure: cbc.MaximumMeasure = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.attribute_id = attribute_id
        self.measure = measure
        self.description = description
        self.minimum_measure = minimum_measure
        self.maximum_measure = maximum_measure


class __ConsignmentType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    carrier_assigned_id = None
    consignee_assigned_id = None
    consignor_assigned_id = None
    freight_forwarder_assigned_id = None
    broker_assigned_id = None
    contracted_carrier_assigned_id = None
    performing_carrier_assigned_id = None
    summary_description = None
    total_invoice_amount = None
    declared_customs_value_amount = None
    tariff_description = None
    tariff_code = None
    insurance_premium_amount = None
    gross_weight_measure = None
    net_weight_measure = None
    net_net_weight_measure = None
    chargeable_weight_measure = None
    gross_volume_measure = None
    net_volume_measure = None
    loading_length_measure = None
    remarks = None
    hazardous_risk_indicator = None
    animal_food_indicator = None
    human_food_indicator = None
    livestock_indicator = None
    bulk_cargo_indicator = None
    containerized_indicator = None
    general_cargo_indicator = None
    special_security_indicator = None
    third_party_payer_indicator = None
    carrier_service_instructions = None
    customs_clearance_service_instructions = None
    forwarder_service_instructions = None
    special_service_instructions = None
    sequence_id = None
    shipping_priority_level_code = None
    handling_code = None
    handling_instructions = None
    information = None
    total_goods_item_quantity = None
    total_transport_handling_unit_quantity = None
    insurance_value_amount = None
    declared_for_carriage_value_amount = None
    declared_statistics_value_amount = None
    free_on_board_value_amount = None
    special_instructions = None
    split_consignment_indicator = None
    delivery_instructions = None
    consignment_quantity = None
    consolidatable_indicator = None
    haulage_instructions = None
    loading_sequence_id = None
    child_consignment_quantity = None
    total_packages_quantity = None
    consolidated_shipment = None
    customs_declaration = None
    requested_pickup_transport_event = None
    requested_delivery_transport_event = None
    planned_pickup_transport_event = None
    planned_delivery_transport_event = None
    status = None
    child_consignment = None
    consignee_party = None
    exporter_party = None
    consignor_party = None
    importer_party = None
    carrier_party = None
    freight_forwarder_party = None
    notify_party = None
    original_despatch_party = None
    final_delivery_party = None
    performing_carrier_party = None
    substitute_carrier_party = None
    logistics_operator_party = None
    transport_advisor_party = None
    hazardous_item_notification_party = None
    insurance_party = None
    mortgage_holder_party = None
    bill_of_lading_holder_party = None
    original_departure_country = None
    final_destination_country = None
    transit_country = None
    transport_contract = None
    transport_event = None
    original_despatch_transportation_service = None
    final_delivery_transportation_service = None
    delivery_terms = None
    payment_terms = None
    collect_payment_terms = None
    disbursement_payment_terms = None
    prepaid_payment_terms = None
    freight_allowance_charge = None
    extra_allowance_charge = None
    main_carriage_shipment_stage = None
    pre_carriage_shipment_stage = None
    on_carriage_shipment_stage = None
    transport_handling_unit = None
    first_arrival_port_location = None
    last_exit_port_location = None
    order_list = [
        'id_',
        'carrier_assigned_id',
        'consignee_assigned_id',
        'consignor_assigned_id',
        'freight_forwarder_assigned_id',
        'broker_assigned_id',
        'contracted_carrier_assigned_id',
        'performing_carrier_assigned_id',
        'summary_description',
        'total_invoice_amount',
        'declared_customs_value_amount',
        'tariff_description',
        'tariff_code',
        'insurance_premium_amount',
        'gross_weight_measure',
        'net_weight_measure',
        'net_net_weight_measure',
        'chargeable_weight_measure',
        'gross_volume_measure',
        'net_volume_measure',
        'loading_length_measure',
        'remarks',
        'hazardous_risk_indicator',
        'animal_food_indicator',
        'human_food_indicator',
        'livestock_indicator',
        'bulk_cargo_indicator',
        'containerized_indicator',
        'general_cargo_indicator',
        'special_security_indicator',
        'third_party_payer_indicator',
        'carrier_service_instructions',
        'customs_clearance_service_instructions',
        'forwarder_service_instructions',
        'special_service_instructions',
        'sequence_id',
        'shipping_priority_level_code',
        'handling_code',
        'handling_instructions',
        'information',
        'total_goods_item_quantity',
        'total_transport_handling_unit_quantity',
        'insurance_value_amount',
        'declared_for_carriage_value_amount',
        'declared_statistics_value_amount',
        'free_on_board_value_amount',
        'special_instructions',
        'split_consignment_indicator',
        'delivery_instructions',
        'consignment_quantity',
        'consolidatable_indicator',
        'haulage_instructions',
        'loading_sequence_id',
        'child_consignment_quantity',
        'total_packages_quantity',
        'consolidated_shipment',
        'customs_declaration',
        'requested_pickup_transport_event',
        'requested_delivery_transport_event',
        'planned_pickup_transport_event',
        'planned_delivery_transport_event',
        'status',
        'child_consignment',
        'consignee_party',
        'exporter_party',
        'consignor_party',
        'importer_party',
        'carrier_party',
        'freight_forwarder_party',
        'notify_party',
        'original_despatch_party',
        'final_delivery_party',
        'performing_carrier_party',
        'substitute_carrier_party',
        'logistics_operator_party',
        'transport_advisor_party',
        'hazardous_item_notification_party',
        'insurance_party',
        'mortgage_holder_party',
        'bill_of_lading_holder_party',
        'original_departure_country',
        'final_destination_country',
        'transit_country',
        'transport_contract',
        'transport_event',
        'original_despatch_transportation_service',
        'final_delivery_transportation_service',
        'delivery_terms',
        'payment_terms',
        'collect_payment_terms',
        'disbursement_payment_terms',
        'prepaid_payment_terms',
        'freight_allowance_charge',
        'extra_allowance_charge',
        'main_carriage_shipment_stage',
        'pre_carriage_shipment_stage',
        'on_carriage_shipment_stage',
        'transport_handling_unit',
        'first_arrival_port_location',
        'last_exit_port_location',
    ]

    def __init__(self,		id_: cbc.ID,
                 carrier_assigned_id: cbc.CarrierAssignedID = None,
                 consignee_assigned_id: cbc.ConsigneeAssignedID = None,
                 consignor_assigned_id: cbc.ConsignorAssignedID = None,
                 freight_forwarder_assigned_id: cbc.FreightForwarderAssignedID = None,
                 broker_assigned_id: cbc.BrokerAssignedID = None,
                 contracted_carrier_assigned_id: cbc.ContractedCarrierAssignedID = None,
                 performing_carrier_assigned_id: cbc.PerformingCarrierAssignedID = None,
                 summary_description: List[cbc.SummaryDescription] = None,
                 total_invoice_amount: cbc.TotalInvoiceAmount = None,
                 declared_customs_value_amount: cbc.DeclaredCustomsValueAmount = None,
                 tariff_description: List[cbc.TariffDescription] = None,
                 tariff_code: cbc.TariffCode = None,
                 insurance_premium_amount: cbc.InsurancePremiumAmount = None,
                 gross_weight_measure: cbc.GrossWeightMeasure = None,
                 net_weight_measure: cbc.NetWeightMeasure = None,
                 net_net_weight_measure: cbc.NetNetWeightMeasure = None,
                 chargeable_weight_measure: cbc.ChargeableWeightMeasure = None,
                 gross_volume_measure: cbc.GrossVolumeMeasure = None,
                 net_volume_measure: cbc.NetVolumeMeasure = None,
                 loading_length_measure: cbc.LoadingLengthMeasure = None,
                 remarks: List[cbc.Remarks] = None,
                 hazardous_risk_indicator: cbc.HazardousRiskIndicator = None,
                 animal_food_indicator: cbc.AnimalFoodIndicator = None,
                 human_food_indicator: cbc.HumanFoodIndicator = None,
                 livestock_indicator: cbc.LivestockIndicator = None,
                 bulk_cargo_indicator: cbc.BulkCargoIndicator = None,
                 containerized_indicator: cbc.ContainerizedIndicator = None,
                 general_cargo_indicator: cbc.GeneralCargoIndicator = None,
                 special_security_indicator: cbc.SpecialSecurityIndicator = None,
                 third_party_payer_indicator: cbc.ThirdPartyPayerIndicator = None,
                 carrier_service_instructions: List[cbc.CarrierServiceInstructions] = None,
                 customs_clearance_service_instructions: List[cbc.CustomsClearanceServiceInstructions] = None,
                 forwarder_service_instructions: List[cbc.ForwarderServiceInstructions] = None,
                 special_service_instructions: List[cbc.SpecialServiceInstructions] = None,
                 sequence_id: cbc.SequenceID = None,
                 shipping_priority_level_code: cbc.ShippingPriorityLevelCode = None,
                 handling_code: cbc.HandlingCode = None,
                 handling_instructions: List[cbc.HandlingInstructions] = None,
                 information: List[cbc.Information] = None,
                 total_goods_item_quantity: cbc.TotalGoodsItemQuantity = None,
                 total_transport_handling_unit_quantity: cbc.TotalTransportHandlingUnitQuantity = None,
                 insurance_value_amount: cbc.InsuranceValueAmount = None,
                 declared_for_carriage_value_amount: cbc.DeclaredForCarriageValueAmount = None,
                 declared_statistics_value_amount: cbc.DeclaredStatisticsValueAmount = None,
                 free_on_board_value_amount: cbc.FreeOnBoardValueAmount = None,
                 special_instructions: List[cbc.SpecialInstructions] = None,
                 split_consignment_indicator: cbc.SplitConsignmentIndicator = None,
                 delivery_instructions: List[cbc.DeliveryInstructions] = None,
                 consignment_quantity: cbc.ConsignmentQuantity = None,
                 consolidatable_indicator: cbc.ConsolidatableIndicator = None,
                 haulage_instructions: List[cbc.HaulageInstructions] = None,
                 loading_sequence_id: cbc.LoadingSequenceID = None,
                 child_consignment_quantity: cbc.ChildConsignmentQuantity = None,
                 total_packages_quantity: cbc.TotalPackagesQuantity = None,
                 consolidated_shipment: List['ConsolidatedShipment'] = None,
                 customs_declaration: List['CustomsDeclaration'] = None,
                 requested_pickup_transport_event: 'RequestedPickupTransportEvent' = None,
                 requested_delivery_transport_event: 'RequestedDeliveryTransportEvent' = None,
                 planned_pickup_transport_event: 'PlannedPickupTransportEvent' = None,
                 planned_delivery_transport_event: 'PlannedDeliveryTransportEvent' = None,
                 status: List['Status'] = None,
                 child_consignment: List['ChildConsignment'] = None,
                 consignee_party: 'ConsigneeParty' = None,
                 exporter_party: 'ExporterParty' = None,
                 consignor_party: 'ConsignorParty' = None,
                 importer_party: 'ImporterParty' = None,
                 carrier_party: 'CarrierParty' = None,
                 freight_forwarder_party: 'FreightForwarderParty' = None,
                 notify_party: 'NotifyParty' = None,
                 original_despatch_party: 'OriginalDespatchParty' = None,
                 final_delivery_party: 'FinalDeliveryParty' = None,
                 performing_carrier_party: 'PerformingCarrierParty' = None,
                 substitute_carrier_party: 'SubstituteCarrierParty' = None,
                 logistics_operator_party: 'LogisticsOperatorParty' = None,
                 transport_advisor_party: 'TransportAdvisorParty' = None,
                 hazardous_item_notification_party: 'HazardousItemNotificationParty' = None,
                 insurance_party: 'InsuranceParty' = None,
                 mortgage_holder_party: 'MortgageHolderParty' = None,
                 bill_of_lading_holder_party: 'BillOfLadingHolderParty' = None,
                 original_departure_country: 'OriginalDepartureCountry' = None,
                 final_destination_country: 'FinalDestinationCountry' = None,
                 transit_country: List['TransitCountry'] = None,
                 transport_contract: 'TransportContract' = None,
                 transport_event: List['TransportEvent'] = None,
                 original_despatch_transportation_service: 'OriginalDespatchTransportationService' = None,
                 final_delivery_transportation_service: 'FinalDeliveryTransportationService' = None,
                 delivery_terms: 'DeliveryTerms' = None,
                 payment_terms: 'PaymentTerms' = None,
                 collect_payment_terms: 'CollectPaymentTerms' = None,
                 disbursement_payment_terms: 'DisbursementPaymentTerms' = None,
                 prepaid_payment_terms: 'PrepaidPaymentTerms' = None,
                 freight_allowance_charge: List['FreightAllowanceCharge'] = None,
                 extra_allowance_charge: List['ExtraAllowanceCharge'] = None,
                 main_carriage_shipment_stage: List['MainCarriageShipmentStage'] = None,
                 pre_carriage_shipment_stage: List['PreCarriageShipmentStage'] = None,
                 on_carriage_shipment_stage: List['OnCarriageShipmentStage'] = None,
                 transport_handling_unit: List['TransportHandlingUnit'] = None,
                 first_arrival_port_location: 'FirstArrivalPortLocation' = None,
                 last_exit_port_location: 'LastExitPortLocation' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.carrier_assigned_id = carrier_assigned_id
        self.consignee_assigned_id = consignee_assigned_id
        self.consignor_assigned_id = consignor_assigned_id
        self.freight_forwarder_assigned_id = freight_forwarder_assigned_id
        self.broker_assigned_id = broker_assigned_id
        self.contracted_carrier_assigned_id = contracted_carrier_assigned_id
        self.performing_carrier_assigned_id = performing_carrier_assigned_id
        self.summary_description = summary_description
        self.total_invoice_amount = total_invoice_amount
        self.declared_customs_value_amount = declared_customs_value_amount
        self.tariff_description = tariff_description
        self.tariff_code = tariff_code
        self.insurance_premium_amount = insurance_premium_amount
        self.gross_weight_measure = gross_weight_measure
        self.net_weight_measure = net_weight_measure
        self.net_net_weight_measure = net_net_weight_measure
        self.chargeable_weight_measure = chargeable_weight_measure
        self.gross_volume_measure = gross_volume_measure
        self.net_volume_measure = net_volume_measure
        self.loading_length_measure = loading_length_measure
        self.remarks = remarks
        self.hazardous_risk_indicator = hazardous_risk_indicator
        self.animal_food_indicator = animal_food_indicator
        self.human_food_indicator = human_food_indicator
        self.livestock_indicator = livestock_indicator
        self.bulk_cargo_indicator = bulk_cargo_indicator
        self.containerized_indicator = containerized_indicator
        self.general_cargo_indicator = general_cargo_indicator
        self.special_security_indicator = special_security_indicator
        self.third_party_payer_indicator = third_party_payer_indicator
        self.carrier_service_instructions = carrier_service_instructions
        self.customs_clearance_service_instructions = customs_clearance_service_instructions
        self.forwarder_service_instructions = forwarder_service_instructions
        self.special_service_instructions = special_service_instructions
        self.sequence_id = sequence_id
        self.shipping_priority_level_code = shipping_priority_level_code
        self.handling_code = handling_code
        self.handling_instructions = handling_instructions
        self.information = information
        self.total_goods_item_quantity = total_goods_item_quantity
        self.total_transport_handling_unit_quantity = total_transport_handling_unit_quantity
        self.insurance_value_amount = insurance_value_amount
        self.declared_for_carriage_value_amount = declared_for_carriage_value_amount
        self.declared_statistics_value_amount = declared_statistics_value_amount
        self.free_on_board_value_amount = free_on_board_value_amount
        self.special_instructions = special_instructions
        self.split_consignment_indicator = split_consignment_indicator
        self.delivery_instructions = delivery_instructions
        self.consignment_quantity = consignment_quantity
        self.consolidatable_indicator = consolidatable_indicator
        self.haulage_instructions = haulage_instructions
        self.loading_sequence_id = loading_sequence_id
        self.child_consignment_quantity = child_consignment_quantity
        self.total_packages_quantity = total_packages_quantity
        self.consolidated_shipment = consolidated_shipment
        self.customs_declaration = customs_declaration
        self.requested_pickup_transport_event = requested_pickup_transport_event
        self.requested_delivery_transport_event = requested_delivery_transport_event
        self.planned_pickup_transport_event = planned_pickup_transport_event
        self.planned_delivery_transport_event = planned_delivery_transport_event
        self.status = status
        self.child_consignment = child_consignment
        self.consignee_party = consignee_party
        self.exporter_party = exporter_party
        self.consignor_party = consignor_party
        self.importer_party = importer_party
        self.carrier_party = carrier_party
        self.freight_forwarder_party = freight_forwarder_party
        self.notify_party = notify_party
        self.original_despatch_party = original_despatch_party
        self.final_delivery_party = final_delivery_party
        self.performing_carrier_party = performing_carrier_party
        self.substitute_carrier_party = substitute_carrier_party
        self.logistics_operator_party = logistics_operator_party
        self.transport_advisor_party = transport_advisor_party
        self.hazardous_item_notification_party = hazardous_item_notification_party
        self.insurance_party = insurance_party
        self.mortgage_holder_party = mortgage_holder_party
        self.bill_of_lading_holder_party = bill_of_lading_holder_party
        self.original_departure_country = original_departure_country
        self.final_destination_country = final_destination_country
        self.transit_country = transit_country
        self.transport_contract = transport_contract
        self.transport_event = transport_event
        self.original_despatch_transportation_service = original_despatch_transportation_service
        self.final_delivery_transportation_service = final_delivery_transportation_service
        self.delivery_terms = delivery_terms
        self.payment_terms = payment_terms
        self.collect_payment_terms = collect_payment_terms
        self.disbursement_payment_terms = disbursement_payment_terms
        self.prepaid_payment_terms = prepaid_payment_terms
        self.freight_allowance_charge = freight_allowance_charge
        self.extra_allowance_charge = extra_allowance_charge
        self.main_carriage_shipment_stage = main_carriage_shipment_stage
        self.pre_carriage_shipment_stage = pre_carriage_shipment_stage
        self.on_carriage_shipment_stage = on_carriage_shipment_stage
        self.transport_handling_unit = transport_handling_unit
        self.first_arrival_port_location = first_arrival_port_location
        self.last_exit_port_location = last_exit_port_location


class __ConsumptionType(PrefixCAC, ComplexXMLParseableObject):
    legal_monetary_total = None
    utility_statement_type_code = None
    main_period = None
    allowance_charge = None
    tax_total = None
    energy_water_supply = None
    telecommunications_supply = None
    order_list = [
        'utility_statement_type_code',
        'main_period',
        'allowance_charge',
        'tax_total',
        'energy_water_supply',
        'telecommunications_supply',
        'legal_monetary_total',
    ]

    def __init__(self,		legal_monetary_total: 'LegalMonetaryTotal',
                 utility_statement_type_code: cbc.UtilityStatementTypeCode = None,
                 main_period: 'MainPeriod' = None,
                 allowance_charge: List['AllowanceCharge'] = None,
                 tax_total: List['TaxTotal'] = None,
                 energy_water_supply: 'EnergyWaterSupply' = None,
                 telecommunications_supply: 'TelecommunicationsSupply' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.legal_monetary_total = legal_monetary_total
        self.utility_statement_type_code = utility_statement_type_code
        self.main_period = main_period
        self.allowance_charge = allowance_charge
        self.tax_total = tax_total
        self.energy_water_supply = energy_water_supply
        self.telecommunications_supply = telecommunications_supply


class __ConsumptionAverageType(PrefixCAC, ComplexXMLParseableObject):
    average_amount = None
    description = None
    order_list = [
        'average_amount',
        'description',
    ]
    def __init__(self,		average_amount: cbc.AverageAmount = None,
                 description: List[cbc.Description] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.average_amount = average_amount
        self.description = description


class __ConsumptionCorrectionType(PrefixCAC, ComplexXMLParseableObject):
    correction_type = None
    correction_type_code = None
    meter_number = None
    gas_pressure_quantity = None
    actual_temperature_reduction_quantity = None
    normal_temperature_reduction_quantity = None
    difference_temperature_reduction_quantity = None
    description = None
    correction_unit_amount = None
    consumption_energy_quantity = None
    consumption_water_quantity = None
    correction_amount = None
    order_list = [
        'correction_type',
        'correction_type_code',
        'meter_number',
        'gas_pressure_quantity',
        'actual_temperature_reduction_quantity',
        'normal_temperature_reduction_quantity',
        'difference_temperature_reduction_quantity',
        'description',
        'correction_unit_amount',
        'consumption_energy_quantity',
        'consumption_water_quantity',
        'correction_amount',
    ]

    def __init__(self,		correction_type: cbc.CorrectionType = None,
                 correction_type_code: cbc.CorrectionTypeCode = None,
                 meter_number: cbc.MeterNumber = None,
                 gas_pressure_quantity: cbc.GasPressureQuantity = None,
                 actual_temperature_reduction_quantity: cbc.ActualTemperatureReductionQuantity = None,
                 normal_temperature_reduction_quantity: cbc.NormalTemperatureReductionQuantity = None,
                 difference_temperature_reduction_quantity: cbc.DifferenceTemperatureReductionQuantity = None,
                 description: List[cbc.Description] = None,
                 correction_unit_amount: cbc.CorrectionUnitAmount = None,
                 consumption_energy_quantity: cbc.ConsumptionEnergyQuantity = None,
                 consumption_water_quantity: cbc.ConsumptionWaterQuantity = None,
                 correction_amount: cbc.CorrectionAmount = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.correction_type = correction_type
        self.correction_type_code = correction_type_code
        self.meter_number = meter_number
        self.gas_pressure_quantity = gas_pressure_quantity
        self.actual_temperature_reduction_quantity = actual_temperature_reduction_quantity
        self.normal_temperature_reduction_quantity = normal_temperature_reduction_quantity
        self.difference_temperature_reduction_quantity = difference_temperature_reduction_quantity
        self.description = description
        self.correction_unit_amount = correction_unit_amount
        self.consumption_energy_quantity = consumption_energy_quantity
        self.consumption_water_quantity = consumption_water_quantity
        self.correction_amount = correction_amount


class __ConsumptionHistoryType(PrefixCAC, ComplexXMLParseableObject):
    quantity = None
    period = None
    meter_number = None
    amount = None
    consumption_level_code = None
    consumption_level = None
    description = None
    order_list = [
        'meter_number',
        'quantity',
        'amount',
        'consumption_level_code',
        'consumption_level',
        'description',
        'period',
    ]

    def __init__(self,		quantity: cbc.Quantity,
                 period: 'Period',
                 meter_number: cbc.MeterNumber = None,
                 amount: cbc.Amount = None,
                 consumption_level_code: cbc.ConsumptionLevelCode = None,
                 consumption_level: cbc.ConsumptionLevel = None,
                 description: List[cbc.Description] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.quantity = quantity
        self.period = period
        self.meter_number = meter_number
        self.amount = amount
        self.consumption_level_code = consumption_level_code
        self.consumption_level = consumption_level
        self.description = description


class __ConsumptionLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    invoiced_quantity = None
    line_extension_amount = None
    utility_item = None
    parent_document_line_reference_id = None
    period = None
    delivery = None
    allowance_charge = None
    tax_total = None
    price = None
    unstructured_price = None
    order_list = [
        'id_',
        'parent_document_line_reference_id',
        'invoiced_quantity',
        'line_extension_amount',
        'period',
        'delivery',
        'allowance_charge',
        'tax_total',
        'utility_item',
        'price',
        'unstructured_price',
    ]

    def __init__(self,		id_: cbc.ID,
                 invoiced_quantity: cbc.InvoicedQuantity,
                 line_extension_amount: cbc.LineExtensionAmount,
                 utility_item: 'UtilityItem',
                 parent_document_line_reference_id: cbc.ParentDocumentLineReferenceID = None,
                 period: 'Period' = None,
                 delivery: List['Delivery'] = None,
                 allowance_charge: List['AllowanceCharge'] = None,
                 tax_total: List['TaxTotal'] = None,
                 price: 'Price' = None,
                 unstructured_price: 'UnstructuredPrice' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.invoiced_quantity = invoiced_quantity
        self.line_extension_amount = line_extension_amount
        self.utility_item = utility_item
        self.parent_document_line_reference_id = parent_document_line_reference_id
        self.period = period
        self.delivery = delivery
        self.allowance_charge = allowance_charge
        self.tax_total = tax_total
        self.price = price
        self.unstructured_price = unstructured_price


class __ConsumptionPointType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    description = None
    subscriber_id = None
    subscriber_type = None
    subscriber_type_code = None
    total_delivered_quantity = None
    address = None
    web_site_access = None
    utility_meter = None
    order_list = [
        'id_',
        'description',
        'subscriber_id',
        'subscriber_type',
        'subscriber_type_code',
        'total_delivered_quantity',
        'address',
        'web_site_access',
        'utility_meter',
    ]

    def __init__(self,		id_: cbc.ID,
                 description: List[cbc.Description] = None,
                 subscriber_id: cbc.SubscriberID = None,
                 subscriber_type: cbc.SubscriberType = None,
                 subscriber_type_code: cbc.SubscriberTypeCode = None,
                 total_delivered_quantity: cbc.TotalDeliveredQuantity = None,
                 address: 'Address' = None,
                 web_site_access: 'WebSiteAccess' = None,
                 utility_meter: List['UtilityMeter'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.description = description
        self.subscriber_id = subscriber_id
        self.subscriber_type = subscriber_type
        self.subscriber_type_code = subscriber_type_code
        self.total_delivered_quantity = total_delivered_quantity
        self.address = address
        self.web_site_access = web_site_access
        self.utility_meter = utility_meter


class __ConsumptionReportType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    consumption_type = None
    consumption_type_code = None
    description = None
    total_consumed_quantity = None
    basic_consumed_quantity = None
    resident_occupants_numeric = None
    consumers_energy_level_code = None
    consumers_energy_level = None
    residence_type = None
    residence_type_code = None
    heating_type = None
    heating_type_code = None
    period = None
    guidance_document_reference = None
    document_reference = None
    consumption_report_reference = None
    consumption_history = None
    order_list = [
        'id_',
        'consumption_type',
        'consumption_type_code',
        'description',
        'total_consumed_quantity',
        'basic_consumed_quantity',
        'resident_occupants_numeric',
        'consumers_energy_level_code',
        'consumers_energy_level',
        'residence_type',
        'residence_type_code',
        'heating_type',
        'heating_type_code',
        'period',
        'guidance_document_reference',
        'document_reference',
        'consumption_report_reference',
        'consumption_history',
    ]

    def __init__(self,		id_: cbc.ID,
                 consumption_type: cbc.ConsumptionType = None,
                 consumption_type_code: cbc.ConsumptionTypeCode = None,
                 description: List[cbc.Description] = None,
                 total_consumed_quantity: cbc.TotalConsumedQuantity = None,
                 basic_consumed_quantity: cbc.BasicConsumedQuantity = None,
                 resident_occupants_numeric: cbc.ResidentOccupantsNumeric = None,
                 consumers_energy_level_code: cbc.ConsumersEnergyLevelCode = None,
                 consumers_energy_level: cbc.ConsumersEnergyLevel = None,
                 residence_type: cbc.ResidenceType = None,
                 residence_type_code: cbc.ResidenceTypeCode = None,
                 heating_type: cbc.HeatingType = None,
                 heating_type_code: cbc.HeatingTypeCode = None,
                 period: 'Period' = None,
                 guidance_document_reference: 'GuidanceDocumentReference' = None,
                 document_reference: 'DocumentReference' = None,
                 consumption_report_reference: List['ConsumptionReportReference'] = None,
                 consumption_history: List['ConsumptionHistory'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.consumption_type = consumption_type
        self.consumption_type_code = consumption_type_code
        self.description = description
        self.total_consumed_quantity = total_consumed_quantity
        self.basic_consumed_quantity = basic_consumed_quantity
        self.resident_occupants_numeric = resident_occupants_numeric
        self.consumers_energy_level_code = consumers_energy_level_code
        self.consumers_energy_level = consumers_energy_level
        self.residence_type = residence_type
        self.residence_type_code = residence_type_code
        self.heating_type = heating_type
        self.heating_type_code = heating_type_code
        self.period = period
        self.guidance_document_reference = guidance_document_reference
        self.document_reference = document_reference
        self.consumption_report_reference = consumption_report_reference
        self.consumption_history = consumption_history


class __ConsumptionReportReferenceType(PrefixCAC, ComplexXMLParseableObject):
    consumption_report_id = None
    total_consumed_quantity = None
    period = None
    consumption_type = None
    consumption_type_code = None
    order_list = [
        'consumption_report_id',
        'consumption_type',
        'consumption_type_code',
        'total_consumed_quantity',
        'period',
    ]

    def __init__(self,		consumption_report_id: cbc.ConsumptionReportID,
                 total_consumed_quantity: cbc.TotalConsumedQuantity,
                 period: 'Period',
                 consumption_type: cbc.ConsumptionType = None,
                 consumption_type_code: cbc.ConsumptionTypeCode = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.consumption_report_id = consumption_report_id
        self.total_consumed_quantity = total_consumed_quantity
        self.period = period
        self.consumption_type = consumption_type
        self.consumption_type_code = consumption_type_code


class __ContactType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    name = None
    telephone = None
    telefax = None
    electronic_mail = None
    note = None
    other_communication = None
    order_list = [
        'id_',
        'name',
        'telephone',
        'telefax',
        'electronic_mail',
        'note',
        'other_communication',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 name: cbc.Name = None,
                 telephone: cbc.Telephone = None,
                 telefax: cbc.Telefax = None,
                 electronic_mail: cbc.ElectronicMail = None,
                 note: List[cbc.Note] = None,
                 other_communication: List['OtherCommunication'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.name = name
        self.telephone = telephone
        self.telefax = telefax
        self.electronic_mail = electronic_mail
        self.note = note
        self.other_communication = other_communication


class __ContractType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    issue_date = None
    issue_time = None
    nomination_date = None
    nomination_time = None
    contract_type_code = None
    contract_type = None
    note = None
    version_id = None
    description = None
    validity_period = None
    contract_document_reference = None
    nomination_period = None
    contractual_delivery = None
    order_list = [
        'id_',
        'issue_date',
        'issue_time',
        'nomination_date',
        'nomination_time',
        'contract_type_code',
        'contract_type',
        'note',
        'version_id',
        'description',
        'validity_period',
        'contract_document_reference',
        'nomination_period',
        'contractual_delivery',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 issue_date: cbc.IssueDate = None,
                 issue_time: cbc.IssueTime = None,
                 nomination_date: cbc.NominationDate = None,
                 nomination_time: cbc.NominationTime = None,
                 contract_type_code: cbc.ContractTypeCode = None,
                 contract_type: cbc.ContractType = None,
                 note: List[cbc.Note] = None,
                 version_id: cbc.VersionID = None,
                 description: List[cbc.Description] = None,
                 validity_period: 'ValidityPeriod' = None,
                 contract_document_reference: List['ContractDocumentReference'] = None,
                 nomination_period: 'NominationPeriod' = None,
                 contractual_delivery: 'ContractualDelivery' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.issue_date = issue_date
        self.issue_time = issue_time
        self.nomination_date = nomination_date
        self.nomination_time = nomination_time
        self.contract_type_code = contract_type_code
        self.contract_type = contract_type
        self.note = note
        self.version_id = version_id
        self.description = description
        self.validity_period = validity_period
        self.contract_document_reference = contract_document_reference
        self.nomination_period = nomination_period
        self.contractual_delivery = contractual_delivery


class __ContractExecutionRequirementType(PrefixCAC, ComplexXMLParseableObject):
    name = None
    execution_requirement_code = None
    description = None
    order_list = [
        'name',
        'execution_requirement_code',
        'description',
    ]

    def __init__(self,		name: List[cbc.Name] = None,
                 execution_requirement_code: cbc.ExecutionRequirementCode = None,
                 description: List[cbc.Description] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.name = name
        self.execution_requirement_code = execution_requirement_code
        self.description = description


class __ContractExtensionType(PrefixCAC, ComplexXMLParseableObject):
    options_description = None
    minimum_number_numeric = None
    maximum_number_numeric = None
    option_validity_period = None
    renewal = None
    order_list = [
        'options_description',
        'minimum_number_numeric',
        'maximum_number_numeric',
        'option_validity_period',
        'renewal',
    ]

    def __init__(self,		options_description: List[cbc.OptionsDescription] = None,
                 minimum_number_numeric: cbc.MinimumNumberNumeric = None,
                 maximum_number_numeric: cbc.MaximumNumberNumeric = None,
                 option_validity_period: 'OptionValidityPeriod' = None,
                 renewal: List['Renewal'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.options_description = options_description
        self.minimum_number_numeric = minimum_number_numeric
        self.maximum_number_numeric = maximum_number_numeric
        self.option_validity_period = option_validity_period
        self.renewal = renewal


class __ContractingActivityType(PrefixCAC, ComplexXMLParseableObject):
    activity_type_code = None
    activity_type = None
    order_list = [
        'activity_type_code',
        'activity_type',
    ]
    def __init__(self,		activity_type_code: cbc.ActivityTypeCode = None,
                 activity_type: cbc.ActivityType = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.activity_type_code = activity_type_code
        self.activity_type = activity_type


class __ContractingPartyType(PrefixCAC, ComplexXMLParseableObject):
    party = None
    buyer_profile_uri = None
    contracting_party_type = None
    contracting_activity = None
    order_list = [
        'buyer_profile_uri',
        'contracting_party_type',
        'contracting_activity',
        'party',
    ]

    def __init__(self,		party: 'Party',
                 buyer_profile_uri: cbc.BuyerProfileURI = None,
                 contracting_party_type: List['ContractingPartyType'] = None,
                 contracting_activity: List['ContractingActivity'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.party = party
        self.buyer_profile_uri = buyer_profile_uri
        self.contracting_party_type = contracting_party_type
        self.contracting_activity = contracting_activity


class __ContractingPartyTypeType(PrefixCAC, ComplexXMLParseableObject):
    party_type_code = None
    party_type = None
    order_list = [
        'party_type_code',
        'party_type',
    ]
    def __init__(self,		party_type_code: cbc.PartyTypeCode = None,
                 party_type: cbc.PartyType = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.party_type_code = party_type_code
        self.party_type = party_type


class __CorporateRegistrationSchemeType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    name = None
    corporate_registration_type_code = None
    jurisdiction_region_address = None
    order_list = [
        'id_',
        'name',
        'corporate_registration_type_code',
        'jurisdiction_region_address',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 name: cbc.Name = None,
                 corporate_registration_type_code: cbc.CorporateRegistrationTypeCode = None,
                 jurisdiction_region_address: List['JurisdictionRegionAddress'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.name = name
        self.corporate_registration_type_code = corporate_registration_type_code
        self.jurisdiction_region_address = jurisdiction_region_address


class __CountryType(PrefixCAC, ComplexXMLParseableObject):
    identification_code = None
    name = None
    order_list = [
        'identification_code',
        'name',
    ]
    def __init__(self,		identification_code: cbc.IdentificationCode = None,
                 name: cbc.Name = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.identification_code = identification_code
        self.name = name


class __CreditAccountType(PrefixCAC, ComplexXMLParseableObject):
    account_id = None
    order_list = [
        'account_id',
    ]

    def __init__(self,		account_id: cbc.AccountID, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.account_id = account_id


class __CreditNoteLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    uuid = None
    note = None
    credited_quantity = None
    line_extension_amount = None
    tax_point_date = None
    accounting_cost_code = None
    accounting_cost = None
    payment_purpose_code = None
    free_of_charge_indicator = None
    invoice_period = None
    order_line_reference = None
    discrepancy_response = None
    despatch_line_reference = None
    receipt_line_reference = None
    billing_reference = None
    document_reference = None
    pricing_reference = None
    originator_party = None
    delivery = None
    payment_terms = None
    tax_total = None
    allowance_charge = None
    item = None
    price = None
    delivery_terms = None
    sub_credit_note_line = None
    item_price_extension = None
    order_list = [
        'id_',
        'uuid',
        'note',
        'credited_quantity',
        'line_extension_amount',
        'tax_point_date',
        'accounting_cost_code',
        'accounting_cost',
        'payment_purpose_code',
        'free_of_charge_indicator',
        'invoice_period',
        'order_line_reference',
        'discrepancy_response',
        'despatch_line_reference',
        'receipt_line_reference',
        'billing_reference',
        'document_reference',
        'pricing_reference',
        'originator_party',
        'delivery',
        'payment_terms',
        'tax_total',
        'allowance_charge',
        'item',
        'price',
        'delivery_terms',
        'sub_credit_note_line',
        'item_price_extension',
    ]

    def __init__(self,		id_: cbc.ID,
                 uuid: cbc.UUID = None,
                 note: List[cbc.Note] = None,
                 credited_quantity: cbc.CreditedQuantity = None,
                 line_extension_amount: cbc.LineExtensionAmount = None,
                 tax_point_date: cbc.TaxPointDate = None,
                 accounting_cost_code: cbc.AccountingCostCode = None,
                 accounting_cost: cbc.AccountingCost = None,
                 payment_purpose_code: cbc.PaymentPurposeCode = None,
                 free_of_charge_indicator: cbc.FreeOfChargeIndicator = None,
                 invoice_period: List['InvoicePeriod'] = None,
                 order_line_reference: List['OrderLineReference'] = None,
                 discrepancy_response: List['DiscrepancyResponse'] = None,
                 despatch_line_reference: List['DespatchLineReference'] = None,
                 receipt_line_reference: List['ReceiptLineReference'] = None,
                 billing_reference: List['BillingReference'] = None,
                 document_reference: List['DocumentReference'] = None,
                 pricing_reference: 'PricingReference' = None,
                 originator_party: 'OriginatorParty' = None,
                 delivery: List['Delivery'] = None,
                 payment_terms: List['PaymentTerms'] = None,
                 tax_total: List['TaxTotal'] = None,
                 allowance_charge: List['AllowanceCharge'] = None,
                 item: 'Item' = None,
                 price: 'Price' = None,
                 delivery_terms: List['DeliveryTerms'] = None,
                 sub_credit_note_line: List['SubCreditNoteLine'] = None,
                 item_price_extension: 'ItemPriceExtension' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.uuid = uuid
        self.note = note
        self.credited_quantity = credited_quantity
        self.line_extension_amount = line_extension_amount
        self.tax_point_date = tax_point_date
        self.accounting_cost_code = accounting_cost_code
        self.accounting_cost = accounting_cost
        self.payment_purpose_code = payment_purpose_code
        self.free_of_charge_indicator = free_of_charge_indicator
        self.invoice_period = invoice_period
        self.order_line_reference = order_line_reference
        self.discrepancy_response = discrepancy_response
        self.despatch_line_reference = despatch_line_reference
        self.receipt_line_reference = receipt_line_reference
        self.billing_reference = billing_reference
        self.document_reference = document_reference
        self.pricing_reference = pricing_reference
        self.originator_party = originator_party
        self.delivery = delivery
        self.payment_terms = payment_terms
        self.tax_total = tax_total
        self.allowance_charge = allowance_charge
        self.item = item
        self.price = price
        self.delivery_terms = delivery_terms
        self.sub_credit_note_line = sub_credit_note_line
        self.item_price_extension = item_price_extension


class __CustomerPartyType(PrefixCAC, ComplexXMLParseableObject):
    customer_assigned_account_id = None
    supplier_assigned_account_id = None
    additional_account_id = None
    party = None
    delivery_contact = None
    accounting_contact = None
    buyer_contact = None
    order_list = [
        'customer_assigned_account_id',
        'supplier_assigned_account_id',
        'additional_account_id',
        'party',
        'delivery_contact',
        'accounting_contact',
        'buyer_contact',
    ]

    def __init__(self,		customer_assigned_account_id: cbc.CustomerAssignedAccountID = None,
                 supplier_assigned_account_id: cbc.SupplierAssignedAccountID = None,
                 additional_account_id: List[cbc.AdditionalAccountID] = None,
                 party: 'Party' = None,
                 delivery_contact: 'DeliveryContact' = None,
                 accounting_contact: 'AccountingContact' = None,
                 buyer_contact: 'BuyerContact' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.customer_assigned_account_id = customer_assigned_account_id
        self.supplier_assigned_account_id = supplier_assigned_account_id
        self.additional_account_id = additional_account_id
        self.party = party
        self.delivery_contact = delivery_contact
        self.accounting_contact = accounting_contact
        self.buyer_contact = buyer_contact


class __CustomsDeclarationType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    issuer_party = None
    order_list = [
        'id_',
        'issuer_party',
    ]
    def __init__(self,		id_: cbc.ID,
                 issuer_party: 'IssuerParty' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.issuer_party = issuer_party


class __DebitNoteLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    line_extension_amount = None
    uuid = None
    note = None
    debited_quantity = None
    tax_point_date = None
    accounting_cost_code = None
    accounting_cost = None
    payment_purpose_code = None
    discrepancy_response = None
    despatch_line_reference = None
    receipt_line_reference = None
    billing_reference = None
    document_reference = None
    pricing_reference = None
    delivery = None
    tax_total = None
    allowance_charge = None
    item = None
    price = None
    sub_debit_note_line = None
    order_list = [
        'id_',
        'uuid',
        'note',
        'debited_quantity',
        'line_extension_amount',
        'tax_point_date',
        'accounting_cost_code',
        'accounting_cost',
        'payment_purpose_code',
        'discrepancy_response',
        'despatch_line_reference',
        'receipt_line_reference',
        'billing_reference',
        'document_reference',
        'pricing_reference',
        'delivery',
        'tax_total',
        'allowance_charge',
        'item',
        'price',
        'sub_debit_note_line',
    ]

    def __init__(self,		id_: cbc.ID,
                 line_extension_amount: cbc.LineExtensionAmount,
                 uuid: cbc.UUID = None,
                 note: List[cbc.Note] = None,
                 debited_quantity: cbc.DebitedQuantity = None,
                 tax_point_date: cbc.TaxPointDate = None,
                 accounting_cost_code: cbc.AccountingCostCode = None,
                 accounting_cost: cbc.AccountingCost = None,
                 payment_purpose_code: cbc.PaymentPurposeCode = None,
                 discrepancy_response: List['DiscrepancyResponse'] = None,
                 despatch_line_reference: List['DespatchLineReference'] = None,
                 receipt_line_reference: List['ReceiptLineReference'] = None,
                 billing_reference: List['BillingReference'] = None,
                 document_reference: List['DocumentReference'] = None,
                 pricing_reference: 'PricingReference' = None,
                 delivery: List['Delivery'] = None,
                 tax_total: List['TaxTotal'] = None,
                 allowance_charge: List['AllowanceCharge'] = None,
                 item: 'Item' = None,
                 price: 'Price' = None,
                 sub_debit_note_line: List['SubDebitNoteLine'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.line_extension_amount = line_extension_amount
        self.uuid = uuid
        self.note = note
        self.debited_quantity = debited_quantity
        self.tax_point_date = tax_point_date
        self.accounting_cost_code = accounting_cost_code
        self.accounting_cost = accounting_cost
        self.payment_purpose_code = payment_purpose_code
        self.discrepancy_response = discrepancy_response
        self.despatch_line_reference = despatch_line_reference
        self.receipt_line_reference = receipt_line_reference
        self.billing_reference = billing_reference
        self.document_reference = document_reference
        self.pricing_reference = pricing_reference
        self.delivery = delivery
        self.tax_total = tax_total
        self.allowance_charge = allowance_charge
        self.item = item
        self.price = price
        self.sub_debit_note_line = sub_debit_note_line


class __DeclarationType(PrefixCAC, ComplexXMLParseableObject):
    name = None
    declaration_type_code = None
    description = None
    evidence_supplied = None
    order_list = [
        'name',
        'declaration_type_code',
        'description',
        'evidence_supplied',
    ]

    def __init__(self,		name: List[cbc.Name] = None,
                 declaration_type_code: cbc.DeclarationTypeCode = None,
                 description: List[cbc.Description] = None,
                 evidence_supplied: List['EvidenceSupplied'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.name = name
        self.declaration_type_code = declaration_type_code
        self.description = description
        self.evidence_supplied = evidence_supplied


class __DeliveryType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    quantity = None
    minimum_quantity = None
    maximum_quantity = None
    actual_delivery_date = None
    actual_delivery_time = None
    latest_delivery_date = None
    latest_delivery_time = None
    release_id = None
    tracking_id = None
    delivery_address = None
    delivery_location = None
    alternative_delivery_location = None
    requested_delivery_period = None
    promised_delivery_period = None
    estimated_delivery_period = None
    carrier_party = None
    delivery_party = None
    notify_party = None
    despatch = None
    delivery_terms = None
    minimum_delivery_unit = None
    maximum_delivery_unit = None
    shipment = None
    order_list = [
        'id_',
        'quantity',
        'minimum_quantity',
        'maximum_quantity',
        'actual_delivery_date',
        'actual_delivery_time',
        'latest_delivery_date',
        'latest_delivery_time',
        'release_id',
        'tracking_id',
        'delivery_address',
        'delivery_location',
        'alternative_delivery_location',
        'requested_delivery_period',
        'promised_delivery_period',
        'estimated_delivery_period',
        'carrier_party',
        'delivery_party',
        'notify_party',
        'despatch',
        'delivery_terms',
        'minimum_delivery_unit',
        'maximum_delivery_unit',
        'shipment',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 quantity: cbc.Quantity = None,
                 minimum_quantity: cbc.MinimumQuantity = None,
                 maximum_quantity: cbc.MaximumQuantity = None,
                 actual_delivery_date: cbc.ActualDeliveryDate = None,
                 actual_delivery_time: cbc.ActualDeliveryTime = None,
                 latest_delivery_date: cbc.LatestDeliveryDate = None,
                 latest_delivery_time: cbc.LatestDeliveryTime = None,
                 release_id: cbc.ReleaseID = None,
                 tracking_id: cbc.TrackingID = None,
                 delivery_address: 'DeliveryAddress' = None,
                 delivery_location: 'DeliveryLocation' = None,
                 alternative_delivery_location: 'AlternativeDeliveryLocation' = None,
                 requested_delivery_period: 'RequestedDeliveryPeriod' = None,
                 promised_delivery_period: 'PromisedDeliveryPeriod' = None,
                 estimated_delivery_period: 'EstimatedDeliveryPeriod' = None,
                 carrier_party: 'CarrierParty' = None,
                 delivery_party: 'DeliveryParty' = None,
                 notify_party: List['NotifyParty'] = None,
                 despatch: 'Despatch' = None,
                 delivery_terms: List['DeliveryTerms'] = None,
                 minimum_delivery_unit: 'MinimumDeliveryUnit' = None,
                 maximum_delivery_unit: 'MaximumDeliveryUnit' = None,
                 shipment: 'Shipment' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.quantity = quantity
        self.minimum_quantity = minimum_quantity
        self.maximum_quantity = maximum_quantity
        self.actual_delivery_date = actual_delivery_date
        self.actual_delivery_time = actual_delivery_time
        self.latest_delivery_date = latest_delivery_date
        self.latest_delivery_time = latest_delivery_time
        self.release_id = release_id
        self.tracking_id = tracking_id
        self.delivery_address = delivery_address
        self.delivery_location = delivery_location
        self.alternative_delivery_location = alternative_delivery_location
        self.requested_delivery_period = requested_delivery_period
        self.promised_delivery_period = promised_delivery_period
        self.estimated_delivery_period = estimated_delivery_period
        self.carrier_party = carrier_party
        self.delivery_party = delivery_party
        self.notify_party = notify_party
        self.despatch = despatch
        self.delivery_terms = delivery_terms
        self.minimum_delivery_unit = minimum_delivery_unit
        self.maximum_delivery_unit = maximum_delivery_unit
        self.shipment = shipment


class __DeliveryTermsType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    special_terms = None
    loss_risk_responsibility_code = None
    loss_risk = None
    amount = None
    delivery_location = None
    allowance_charge = None
    order_list = [
        'id_',
        'special_terms',
        'loss_risk_responsibility_code',
        'loss_risk',
        'amount',
        'delivery_location',
        'allowance_charge',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 special_terms: List[cbc.SpecialTerms] = None,
                 loss_risk_responsibility_code: cbc.LossRiskResponsibilityCode = None,
                 loss_risk: List[cbc.LossRisk] = None,
                 amount: cbc.Amount = None,
                 delivery_location: 'DeliveryLocation' = None,
                 allowance_charge: 'AllowanceCharge' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.special_terms = special_terms
        self.loss_risk_responsibility_code = loss_risk_responsibility_code
        self.loss_risk = loss_risk
        self.amount = amount
        self.delivery_location = delivery_location
        self.allowance_charge = allowance_charge


class __DeliveryUnitType(PrefixCAC, ComplexXMLParseableObject):
    batch_quantity = None
    consumer_unit_quantity = None
    hazardous_risk_indicator = None
    order_list = [
        'batch_quantity',
        'consumer_unit_quantity',
        'hazardous_risk_indicator',
    ]

    def __init__(self,		batch_quantity: cbc.BatchQuantity,
                 consumer_unit_quantity: cbc.ConsumerUnitQuantity = None,
                 hazardous_risk_indicator: cbc.HazardousRiskIndicator = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.batch_quantity = batch_quantity
        self.consumer_unit_quantity = consumer_unit_quantity
        self.hazardous_risk_indicator = hazardous_risk_indicator


class __DependentPriceReferenceType(PrefixCAC, ComplexXMLParseableObject):
    percent = None
    location_address = None
    dependent_line_reference = None
    order_list = [
        'percent',
        'location_address',
        'dependent_line_reference',
    ]

    def __init__(self,		percent: cbc.Percent = None,
                 location_address: 'LocationAddress' = None,
                 dependent_line_reference: 'DependentLineReference' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.percent = percent
        self.location_address = location_address
        self.dependent_line_reference = dependent_line_reference


class __DespatchType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    requested_despatch_date = None
    requested_despatch_time = None
    estimated_despatch_date = None
    estimated_despatch_time = None
    actual_despatch_date = None
    actual_despatch_time = None
    guaranteed_despatch_date = None
    guaranteed_despatch_time = None
    release_id = None
    instructions = None
    despatch_address = None
    despatch_location = None
    despatch_party = None
    carrier_party = None
    notify_party = None
    contact = None
    estimated_despatch_period = None
    requested_despatch_period = None
    order_list = [
        'id_',
        'requested_despatch_date',
        'requested_despatch_time',
        'estimated_despatch_date',
        'estimated_despatch_time',
        'actual_despatch_date',
        'actual_despatch_time',
        'guaranteed_despatch_date',
        'guaranteed_despatch_time',
        'release_id',
        'instructions',
        'despatch_address',
        'despatch_location',
        'despatch_party',
        'carrier_party',
        'notify_party',
        'contact',
        'estimated_despatch_period',
        'requested_despatch_period',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 requested_despatch_date: cbc.RequestedDespatchDate = None,
                 requested_despatch_time: cbc.RequestedDespatchTime = None,
                 estimated_despatch_date: cbc.EstimatedDespatchDate = None,
                 estimated_despatch_time: cbc.EstimatedDespatchTime = None,
                 actual_despatch_date: cbc.ActualDespatchDate = None,
                 actual_despatch_time: cbc.ActualDespatchTime = None,
                 guaranteed_despatch_date: cbc.GuaranteedDespatchDate = None,
                 guaranteed_despatch_time: cbc.GuaranteedDespatchTime = None,
                 release_id: cbc.ReleaseID = None,
                 instructions: List[cbc.Instructions] = None,
                 despatch_address: 'DespatchAddress' = None,
                 despatch_location: 'DespatchLocation' = None,
                 despatch_party: 'DespatchParty' = None,
                 carrier_party: 'CarrierParty' = None,
                 notify_party: List['NotifyParty'] = None,
                 contact: 'Contact' = None,
                 estimated_despatch_period: 'EstimatedDespatchPeriod' = None,
                 requested_despatch_period: 'RequestedDespatchPeriod' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.requested_despatch_date = requested_despatch_date
        self.requested_despatch_time = requested_despatch_time
        self.estimated_despatch_date = estimated_despatch_date
        self.estimated_despatch_time = estimated_despatch_time
        self.actual_despatch_date = actual_despatch_date
        self.actual_despatch_time = actual_despatch_time
        self.guaranteed_despatch_date = guaranteed_despatch_date
        self.guaranteed_despatch_time = guaranteed_despatch_time
        self.release_id = release_id
        self.instructions = instructions
        self.despatch_address = despatch_address
        self.despatch_location = despatch_location
        self.despatch_party = despatch_party
        self.carrier_party = carrier_party
        self.notify_party = notify_party
        self.contact = contact
        self.estimated_despatch_period = estimated_despatch_period
        self.requested_despatch_period = requested_despatch_period


class __DespatchLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    item = None
    uuid = None
    note = None
    line_status_code = None
    delivered_quantity = None
    backorder_quantity = None
    backorder_reason = None
    outstanding_quantity = None
    outstanding_reason = None
    oversupply_quantity = None
    order_line_reference = None
    document_reference = None
    shipment = None
    order_list = [
        'id_',
        'uuid',
        'note',
        'line_status_code',
        'delivered_quantity',
        'backorder_quantity',
        'backorder_reason',
        'outstanding_quantity',
        'outstanding_reason',
        'oversupply_quantity',
        'order_line_reference',
        'document_reference',
        'item',
        'shipment',
    ]

    def __init__(self,		id_: cbc.ID,
                 item: 'Item',
                 uuid: cbc.UUID = None,
                 note: List[cbc.Note] = None,
                 line_status_code: cbc.LineStatusCode = None,
                 delivered_quantity: cbc.DeliveredQuantity = None,
                 backorder_quantity: cbc.BackorderQuantity = None,
                 backorder_reason: List[cbc.BackorderReason] = None,
                 outstanding_quantity: cbc.OutstandingQuantity = None,
                 outstanding_reason: List[cbc.OutstandingReason] = None,
                 oversupply_quantity: cbc.OversupplyQuantity = None,
                 order_line_reference: List['OrderLineReference'] = None,
                 document_reference: List['DocumentReference'] = None,
                 shipment: List['Shipment'] = None, xml_namespaces=None):
        if not order_line_reference:
            raise ListMustNotBeEmptyException('order_line_reference')
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.item = item
        self.uuid = uuid
        self.note = note
        self.line_status_code = line_status_code
        self.delivered_quantity = delivered_quantity
        self.backorder_quantity = backorder_quantity
        self.backorder_reason = backorder_reason
        self.outstanding_quantity = outstanding_quantity
        self.outstanding_reason = outstanding_reason
        self.oversupply_quantity = oversupply_quantity
        self.order_line_reference = order_line_reference
        self.document_reference = document_reference
        self.shipment = shipment


class __DimensionType(PrefixCAC, ComplexXMLParseableObject):
    attribute_id = None
    measure = None
    description = None
    minimum_measure = None
    maximum_measure = None
    order_list = [
        'attribute_id',
        'measure',
        'description',
        'minimum_measure',
        'maximum_measure',
    ]

    def __init__(self,		attribute_id: cbc.AttributeID,
                 measure: cbc.Measure = None,
                 description: List[cbc.Description] = None,
                 minimum_measure: cbc.MinimumMeasure = None,
                 maximum_measure: cbc.MaximumMeasure = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.attribute_id = attribute_id
        self.measure = measure
        self.description = description
        self.minimum_measure = minimum_measure
        self.maximum_measure = maximum_measure


class __DocumentDistributionType(PrefixCAC, ComplexXMLParseableObject):
    print_qualifier = None
    maximum_copies_numeric = None
    party = None
    order_list = [
        'print_qualifier',
        'maximum_copies_numeric',
        'party',
    ]

    def __init__(self,		print_qualifier: cbc.PrintQualifier,
                 maximum_copies_numeric: cbc.MaximumCopiesNumeric,
                 party: 'Party', xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.print_qualifier = print_qualifier
        self.maximum_copies_numeric = maximum_copies_numeric
        self.party = party


class __DocumentReferenceType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    copy_indicator = None
    uuid = None
    issue_date = None
    issue_time = None
    document_type_code = None
    document_type = None
    xpath = None
    language_id = None
    locale_code = None
    version_id = None
    document_status_code = None
    document_description = None
    attachment = None
    validity_period = None
    issuer_party = None
    result_of_verification = None
    order_list = [
        'id_',
        'copy_indicator',
        'uuid',
        'issue_date',
        'issue_time',
        'document_type_code',
        'document_type',
        'xpath',
        'language_id',
        'locale_code',
        'version_id',
        'document_status_code',
        'document_description',
        'attachment',
        'validity_period',
        'issuer_party',
        'result_of_verification',
    ]

    def __init__(self,		id_: cbc.ID,
                 copy_indicator: cbc.CopyIndicator = None,
                 uuid: cbc.UUID = None,
                 issue_date: cbc.IssueDate = None,
                 issue_time: cbc.IssueTime = None,
                 document_type_code: cbc.DocumentTypeCode = None,
                 document_type: cbc.DocumentType = None,
                 xpath: List[cbc.XPath] = None,
                 language_id: cbc.LanguageID = None,
                 locale_code: cbc.LocaleCode = None,
                 version_id: cbc.VersionID = None,
                 document_status_code: cbc.DocumentStatusCode = None,
                 document_description: List[cbc.DocumentDescription] = None,
                 attachment: 'Attachment' = None,
                 validity_period: 'ValidityPeriod' = None,
                 issuer_party: 'IssuerParty' = None,
                 result_of_verification: 'ResultOfVerification' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.copy_indicator = copy_indicator
        self.uuid = uuid
        self.issue_date = issue_date
        self.issue_time = issue_time
        self.document_type_code = document_type_code
        self.document_type = document_type
        self.xpath = xpath
        self.language_id = language_id
        self.locale_code = locale_code
        self.version_id = version_id
        self.document_status_code = document_status_code
        self.document_description = document_description
        self.attachment = attachment
        self.validity_period = validity_period
        self.issuer_party = issuer_party
        self.result_of_verification = result_of_verification


class __DocumentResponseType(PrefixCAC, ComplexXMLParseableObject):
    response = None
    document_reference = None
    issuer_party = None
    recipient_party = None
    line_response = None
    order_list = [
        'response',
        'document_reference',
        'issuer_party',
        'recipient_party',
        'line_response',
    ]

    def __init__(self,		response: 'Response',
                 document_reference: List['DocumentReference'] = None,
                 issuer_party: 'IssuerParty' = None,
                 recipient_party: 'RecipientParty' = None,
                 line_response: List['LineResponse'] = None, xml_namespaces=None):
        if not document_reference:
            raise ListMustNotBeEmptyException('document_reference')
        super().__init__(xml_namespaces)
        self.response = response
        self.document_reference = document_reference
        self.issuer_party = issuer_party
        self.recipient_party = recipient_party
        self.line_response = line_response


class __DutyType(PrefixCAC, ComplexXMLParseableObject):
    amount = None
    duty = None
    duty_code = None
    tax_category = None
    order_list = [
        'amount',
        'duty',
        'duty_code',
        'tax_category',
    ]

    def __init__(self,		amount: cbc.Amount,
                 duty: cbc.Duty = None,
                 duty_code: cbc.DutyCode = None,
                 tax_category: 'TaxCategory' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.amount = amount
        self.duty = duty
        self.duty_code = duty_code
        self.tax_category = tax_category


class __EconomicOperatorRoleType(PrefixCAC, ComplexXMLParseableObject):
    role_code = None
    role_description = None
    order_list = [
        'role_code',
        'role_description',
    ]
    def __init__(self,		role_code: cbc.RoleCode = None,
                 role_description: List[cbc.RoleDescription] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.role_code = role_code
        self.role_description = role_description


class __EconomicOperatorShortListType(PrefixCAC, ComplexXMLParseableObject):
    limitation_description = None
    expected_quantity = None
    maximum_quantity = None
    minimum_quantity = None
    pre_selected_party = None
    order_list = [
        'limitation_description',
        'expected_quantity',
        'maximum_quantity',
        'minimum_quantity',
        'pre_selected_party',
    ]

    def __init__(self,		limitation_description: List[cbc.LimitationDescription] = None,
                 expected_quantity: cbc.ExpectedQuantity = None,
                 maximum_quantity: cbc.MaximumQuantity = None,
                 minimum_quantity: cbc.MinimumQuantity = None,
                 pre_selected_party: List['PreSelectedParty'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.limitation_description = limitation_description
        self.expected_quantity = expected_quantity
        self.maximum_quantity = maximum_quantity
        self.minimum_quantity = minimum_quantity
        self.pre_selected_party = pre_selected_party


class __EmissionCalculationMethodType(PrefixCAC, ComplexXMLParseableObject):
    calculation_method_code = None
    fullness_indication_code = None
    measurement_from_location = None
    measurement_to_location = None
    order_list = [
        'calculation_method_code',
        'fullness_indication_code',
        'measurement_from_location',
        'measurement_to_location',
    ]

    def __init__(self,		calculation_method_code: cbc.CalculationMethodCode = None,
                 fullness_indication_code: cbc.FullnessIndicationCode = None,
                 measurement_from_location: 'MeasurementFromLocation' = None,
                 measurement_to_location: 'MeasurementToLocation' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.calculation_method_code = calculation_method_code
        self.fullness_indication_code = fullness_indication_code
        self.measurement_from_location = measurement_from_location
        self.measurement_to_location = measurement_to_location


class __EndorsementType(PrefixCAC, ComplexXMLParseableObject):
    document_id = None
    approval_status = None
    endorser_party = None
    remarks = None
    signature = None
    order_list = [
        'document_id',
        'approval_status',
        'remarks',
        'endorser_party',
        'signature',
    ]

    def __init__(self,		document_id: cbc.DocumentID,
                 approval_status: cbc.ApprovalStatus,
                 endorser_party: 'EndorserParty',
                 remarks: List[cbc.Remarks] = None,
                 signature: List['Signature'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.document_id = document_id
        self.approval_status = approval_status
        self.endorser_party = endorser_party
        self.remarks = remarks
        self.signature = signature


class __EndorserPartyType(PrefixCAC, ComplexXMLParseableObject):
    role_code = None
    sequence_numeric = None
    party = None
    signatory_contact = None
    order_list = [
        'role_code',
        'sequence_numeric',
        'party',
        'signatory_contact',
    ]

    def __init__(self,		role_code: cbc.RoleCode,
                 sequence_numeric: cbc.SequenceNumeric,
                 party: 'Party',
                 signatory_contact: 'SignatoryContact', xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.role_code = role_code
        self.sequence_numeric = sequence_numeric
        self.party = party
        self.signatory_contact = signatory_contact


class __EnergyTaxReportType(PrefixCAC, ComplexXMLParseableObject):
    tax_scheme = None
    tax_energy_amount = None
    tax_energy_on_account_amount = None
    tax_energy_balance_amount = None
    order_list = [
        'tax_energy_amount',
        'tax_energy_on_account_amount',
        'tax_energy_balance_amount',
        'tax_scheme',
    ]

    def __init__(self,		tax_scheme: 'TaxScheme',
                 tax_energy_amount: cbc.TaxEnergyAmount = None,
                 tax_energy_on_account_amount: cbc.TaxEnergyOnAccountAmount = None,
                 tax_energy_balance_amount: cbc.TaxEnergyBalanceAmount = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.tax_scheme = tax_scheme
        self.tax_energy_amount = tax_energy_amount
        self.tax_energy_on_account_amount = tax_energy_on_account_amount
        self.tax_energy_balance_amount = tax_energy_balance_amount


class __EnergyWaterSupplyType(PrefixCAC, ComplexXMLParseableObject):
    consumption_report = None
    energy_tax_report = None
    consumption_average = None
    energy_water_consumption_correction = None
    order_list = [
        'consumption_report',
        'energy_tax_report',
        'consumption_average',
        'energy_water_consumption_correction',
    ]

    def __init__(self,		consumption_report: List['ConsumptionReport'] = None,
                 energy_tax_report: List['EnergyTaxReport'] = None,
                 consumption_average: List['ConsumptionAverage'] = None,
                 energy_water_consumption_correction: List['EnergyWaterConsumptionCorrection'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.consumption_report = consumption_report
        self.energy_tax_report = energy_tax_report
        self.consumption_average = consumption_average
        self.energy_water_consumption_correction = energy_water_consumption_correction


class __EnvironmentalEmissionType(PrefixCAC, ComplexXMLParseableObject):
    environmental_emission_type_code = None
    value_measure = None
    description = None
    emission_calculation_method = None
    order_list = [
        'environmental_emission_type_code',
        'value_measure',
        'description',
        'emission_calculation_method',
    ]

    def __init__(self,		environmental_emission_type_code: cbc.EnvironmentalEmissionTypeCode,
                 value_measure: cbc.ValueMeasure,
                 description: List[cbc.Description] = None,
                 emission_calculation_method: List['EmissionCalculationMethod'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.environmental_emission_type_code = environmental_emission_type_code
        self.value_measure = value_measure
        self.description = description
        self.emission_calculation_method = emission_calculation_method


class __EvaluationCriterionType(PrefixCAC, ComplexXMLParseableObject):
    evaluation_criterion_type_code = None
    description = None
    threshold_amount = None
    threshold_quantity = None
    expression_code = None
    expression = None
    duration_period = None
    suggested_evidence = None
    order_list = [
        'evaluation_criterion_type_code',
        'description',
        'threshold_amount',
        'threshold_quantity',
        'expression_code',
        'expression',
        'duration_period',
        'suggested_evidence',
    ]

    def __init__(self,		evaluation_criterion_type_code: cbc.EvaluationCriterionTypeCode = None,
                 description: List[cbc.Description] = None,
                 threshold_amount: cbc.ThresholdAmount = None,
                 threshold_quantity: cbc.ThresholdQuantity = None,
                 expression_code: cbc.ExpressionCode = None,
                 expression: List[cbc.Expression] = None,
                 duration_period: 'DurationPeriod' = None,
                 suggested_evidence: List['SuggestedEvidence'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.evaluation_criterion_type_code = evaluation_criterion_type_code
        self.description = description
        self.threshold_amount = threshold_amount
        self.threshold_quantity = threshold_quantity
        self.expression_code = expression_code
        self.expression = expression
        self.duration_period = duration_period
        self.suggested_evidence = suggested_evidence


class __EventType(PrefixCAC, ComplexXMLParseableObject):
    identification_id = None
    occurrence_date = None
    occurrence_time = None
    type_code = None
    description = None
    completion_indicator = None
    current_status = None
    contact = None
    occurence_location = None
    order_list = [
        'identification_id',
        'occurrence_date',
        'occurrence_time',
        'type_code',
        'description',
        'completion_indicator',
        'current_status',
        'contact',
        'occurence_location',
    ]

    def __init__(self,		identification_id: cbc.IdentificationID = None,
                 occurrence_date: cbc.OccurrenceDate = None,
                 occurrence_time: cbc.OccurrenceTime = None,
                 type_code: cbc.TypeCode = None,
                 description: List[cbc.Description] = None,
                 completion_indicator: cbc.CompletionIndicator = None,
                 current_status: List['CurrentStatus'] = None,
                 contact: List['Contact'] = None,
                 occurence_location: 'OccurenceLocation' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.identification_id = identification_id
        self.occurrence_date = occurrence_date
        self.occurrence_time = occurrence_time
        self.type_code = type_code
        self.description = description
        self.completion_indicator = completion_indicator
        self.current_status = current_status
        self.contact = contact
        self.occurence_location = occurence_location


class __EventCommentType(PrefixCAC, ComplexXMLParseableObject):
    comment = None
    issue_date = None
    issue_time = None
    order_list = [
        'comment',
        'issue_date',
        'issue_time',
    ]

    def __init__(self,		comment: cbc.Comment,
                 issue_date: cbc.IssueDate = None,
                 issue_time: cbc.IssueTime = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.comment = comment
        self.issue_date = issue_date
        self.issue_time = issue_time


class __EventLineItemType(PrefixCAC, ComplexXMLParseableObject):
    supply_item = None
    line_number_numeric = None
    participating_locations_location = None
    retail_planned_impact = None
    order_list = [
        'line_number_numeric',
        'participating_locations_location',
        'retail_planned_impact',
        'supply_item',
    ]

    def __init__(self,		supply_item: 'SupplyItem',
                 line_number_numeric: cbc.LineNumberNumeric = None,
                 participating_locations_location: 'ParticipatingLocationsLocation' = None,
                 retail_planned_impact: List['RetailPlannedImpact'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.supply_item = supply_item
        self.line_number_numeric = line_number_numeric
        self.participating_locations_location = participating_locations_location
        self.retail_planned_impact = retail_planned_impact


class __EventTacticType(PrefixCAC, ComplexXMLParseableObject):
    event_tactic_enumeration = None
    comment = None
    quantity = None
    period = None
    order_list = [
        'comment',
        'quantity',
        'event_tactic_enumeration',
        'period',
    ]

    def __init__(self,		event_tactic_enumeration: 'EventTacticEnumeration',
                 comment: cbc.Comment = None,
                 quantity: cbc.Quantity = None,
                 period: 'Period' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.event_tactic_enumeration = event_tactic_enumeration
        self.comment = comment
        self.quantity = quantity
        self.period = period


class __EventTacticEnumerationType(PrefixCAC, ComplexXMLParseableObject):
    consumer_incentive_tactic_type_code = None
    display_tactic_type_code = None
    feature_tactic_type_code = None
    trade_item_packing_labeling_type_code = None
    order_list = [
        'consumer_incentive_tactic_type_code',
        'display_tactic_type_code',
        'feature_tactic_type_code',
        'trade_item_packing_labeling_type_code',
    ]

    def __init__(self,		consumer_incentive_tactic_type_code: cbc.ConsumerIncentiveTacticTypeCode = None,
                 display_tactic_type_code: cbc.DisplayTacticTypeCode = None,
                 feature_tactic_type_code: cbc.FeatureTacticTypeCode = None,
                 trade_item_packing_labeling_type_code: cbc.TradeItemPackingLabelingTypeCode = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.consumer_incentive_tactic_type_code = consumer_incentive_tactic_type_code
        self.display_tactic_type_code = display_tactic_type_code
        self.feature_tactic_type_code = feature_tactic_type_code
        self.trade_item_packing_labeling_type_code = trade_item_packing_labeling_type_code


class __EvidenceType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    evidence_type_code = None
    description = None
    candidate_statement = None
    evidence_issuing_party = None
    document_reference = None
    language = None
    order_list = [
        'id_',
        'evidence_type_code',
        'description',
        'candidate_statement',
        'evidence_issuing_party',
        'document_reference',
        'language',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 evidence_type_code: cbc.EvidenceTypeCode = None,
                 description: List[cbc.Description] = None,
                 candidate_statement: List[cbc.CandidateStatement] = None,
                 evidence_issuing_party: 'EvidenceIssuingParty' = None,
                 document_reference: 'DocumentReference' = None,
                 language: 'Language' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.evidence_type_code = evidence_type_code
        self.description = description
        self.candidate_statement = candidate_statement
        self.evidence_issuing_party = evidence_issuing_party
        self.document_reference = document_reference
        self.language = language


class __EvidenceSuppliedType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    order_list = [
        'id_',
    ]

    def __init__(self,		id_: cbc.ID, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_


class __ExceptionCriteriaLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    threshold_value_comparison_code = None
    threshold_quantity = None
    note = None
    exception_status_code = None
    collaboration_priority_code = None
    exception_resolution_code = None
    supply_chain_activity_type_code = None
    performance_metric_type_code = None
    effective_period = None
    supply_item = None
    forecast_exception_criterion_line = None
    order_list = [
        'id_',
        'note',
        'threshold_value_comparison_code',
        'threshold_quantity',
        'exception_status_code',
        'collaboration_priority_code',
        'exception_resolution_code',
        'supply_chain_activity_type_code',
        'performance_metric_type_code',
        'effective_period',
        'supply_item',
        'forecast_exception_criterion_line',
    ]

    def __init__(self,		id_: cbc.ID,
                 threshold_value_comparison_code: cbc.ThresholdValueComparisonCode,
                 threshold_quantity: cbc.ThresholdQuantity,
                 note: List[cbc.Note] = None,
                 exception_status_code: cbc.ExceptionStatusCode = None,
                 collaboration_priority_code: cbc.CollaborationPriorityCode = None,
                 exception_resolution_code: cbc.ExceptionResolutionCode = None,
                 supply_chain_activity_type_code: cbc.SupplyChainActivityTypeCode = None,
                 performance_metric_type_code: cbc.PerformanceMetricTypeCode = None,
                 effective_period: 'EffectivePeriod' = None,
                 supply_item: List['SupplyItem'] = None,
                 forecast_exception_criterion_line: 'ForecastExceptionCriterionLine' = None, xml_namespaces=None):
        if not supply_item:
            raise ListMustNotBeEmptyException('supply_item')
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.threshold_value_comparison_code = threshold_value_comparison_code
        self.threshold_quantity = threshold_quantity
        self.note = note
        self.exception_status_code = exception_status_code
        self.collaboration_priority_code = collaboration_priority_code
        self.exception_resolution_code = exception_resolution_code
        self.supply_chain_activity_type_code = supply_chain_activity_type_code
        self.performance_metric_type_code = performance_metric_type_code
        self.effective_period = effective_period
        self.supply_item = supply_item
        self.forecast_exception_criterion_line = forecast_exception_criterion_line


class __ExceptionNotificationLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    compared_value_measure = None
    source_value_measure = None
    supply_item = None
    note = None
    description = None
    exception_status_code = None
    collaboration_priority_code = None
    resolution_code = None
    variance_quantity = None
    supply_chain_activity_type_code = None
    performance_metric_type_code = None
    exception_observation_period = None
    document_reference = None
    forecast_exception = None
    order_list = [
        'id_',
        'note',
        'description',
        'exception_status_code',
        'collaboration_priority_code',
        'resolution_code',
        'compared_value_measure',
        'source_value_measure',
        'variance_quantity',
        'supply_chain_activity_type_code',
        'performance_metric_type_code',
        'exception_observation_period',
        'document_reference',
        'forecast_exception',
        'supply_item',
    ]

    def __init__(self,		id_: cbc.ID,
                 compared_value_measure: cbc.ComparedValueMeasure,
                 source_value_measure: cbc.SourceValueMeasure,
                 supply_item: 'SupplyItem',
                 note: List[cbc.Note] = None,
                 description: List[cbc.Description] = None,
                 exception_status_code: cbc.ExceptionStatusCode = None,
                 collaboration_priority_code: cbc.CollaborationPriorityCode = None,
                 resolution_code: cbc.ResolutionCode = None,
                 variance_quantity: cbc.VarianceQuantity = None,
                 supply_chain_activity_type_code: cbc.SupplyChainActivityTypeCode = None,
                 performance_metric_type_code: cbc.PerformanceMetricTypeCode = None,
                 exception_observation_period: 'ExceptionObservationPeriod' = None,
                 document_reference: List['DocumentReference'] = None,
                 forecast_exception: 'ForecastException' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.compared_value_measure = compared_value_measure
        self.source_value_measure = source_value_measure
        self.supply_item = supply_item
        self.note = note
        self.description = description
        self.exception_status_code = exception_status_code
        self.collaboration_priority_code = collaboration_priority_code
        self.resolution_code = resolution_code
        self.variance_quantity = variance_quantity
        self.supply_chain_activity_type_code = supply_chain_activity_type_code
        self.performance_metric_type_code = performance_metric_type_code
        self.exception_observation_period = exception_observation_period
        self.document_reference = document_reference
        self.forecast_exception = forecast_exception


class __ExchangeRateType(PrefixCAC, ComplexXMLParseableObject):
    source_currency_code = None
    target_currency_code = None
    source_currency_base_rate = None
    target_currency_base_rate = None
    exchange_market_id = None
    calculation_rate = None
    mathematic_operator_code = None
    date = None
    foreign_exchange_contract = None
    order_list = [
        'source_currency_code',
        'source_currency_base_rate',
        'target_currency_code',
        'target_currency_base_rate',
        'exchange_market_id',
        'calculation_rate',
        'mathematic_operator_code',
        'date',
        'foreign_exchange_contract',
    ]

    def __init__(self,		source_currency_code: cbc.SourceCurrencyCode,
                 target_currency_code: cbc.TargetCurrencyCode,
                 source_currency_base_rate: cbc.SourceCurrencyBaseRate = None,
                 target_currency_base_rate: cbc.TargetCurrencyBaseRate = None,
                 exchange_market_id: cbc.ExchangeMarketID = None,
                 calculation_rate: cbc.CalculationRate = None,
                 mathematic_operator_code: cbc.MathematicOperatorCode = None,
                 date: cbc.Date = None,
                 foreign_exchange_contract: 'ForeignExchangeContract' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.source_currency_code = source_currency_code
        self.target_currency_code = target_currency_code
        self.source_currency_base_rate = source_currency_base_rate
        self.target_currency_base_rate = target_currency_base_rate
        self.exchange_market_id = exchange_market_id
        self.calculation_rate = calculation_rate
        self.mathematic_operator_code = mathematic_operator_code
        self.date = date
        self.foreign_exchange_contract = foreign_exchange_contract


class __ExternalReferenceType(PrefixCAC, ComplexXMLParseableObject):
    uri = None
    document_hash = None
    hash_algorithm_method = None
    expiry_date = None
    expiry_time = None
    mime_code = None
    format_code = None
    encoding_code = None
    character_set_code = None
    file_name = None
    description = None
    order_list = [
        'uri',
        'document_hash',
        'hash_algorithm_method',
        'expiry_date',
        'expiry_time',
        'mime_code',
        'format_code',
        'encoding_code',
        'character_set_code',
        'file_name',
        'description',
    ]

    def __init__(self,		uri: cbc.URI = None,
                 document_hash: cbc.DocumentHash = None,
                 hash_algorithm_method: cbc.HashAlgorithmMethod = None,
                 expiry_date: cbc.ExpiryDate = None,
                 expiry_time: cbc.ExpiryTime = None,
                 mime_code: cbc.MimeCode = None,
                 format_code: cbc.FormatCode = None,
                 encoding_code: cbc.EncodingCode = None,
                 character_set_code: cbc.CharacterSetCode = None,
                 file_name: cbc.FileName = None,
                 description: List[cbc.Description] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.uri = uri
        self.document_hash = document_hash
        self.hash_algorithm_method = hash_algorithm_method
        self.expiry_date = expiry_date
        self.expiry_time = expiry_time
        self.mime_code = mime_code
        self.format_code = format_code
        self.encoding_code = encoding_code
        self.character_set_code = character_set_code
        self.file_name = file_name
        self.description = description


class __FinancialAccountType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    name = None
    alias_name = None
    account_type_code = None
    account_format_code = None
    currency_code = None
    payment_note = None
    financial_institution_branch = None
    country = None
    order_list = [
        'id_',
        'name',
        'alias_name',
        'account_type_code',
        'account_format_code',
        'currency_code',
        'payment_note',
        'financial_institution_branch',
        'country',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 name: cbc.Name = None,
                 alias_name: cbc.AliasName = None,
                 account_type_code: cbc.AccountTypeCode = None,
                 account_format_code: cbc.AccountFormatCode = None,
                 currency_code: cbc.CurrencyCode = None,
                 payment_note: List[cbc.PaymentNote] = None,
                 financial_institution_branch: 'FinancialInstitutionBranch' = None,
                 country: 'Country' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.name = name
        self.alias_name = alias_name
        self.account_type_code = account_type_code
        self.account_format_code = account_format_code
        self.currency_code = currency_code
        self.payment_note = payment_note
        self.financial_institution_branch = financial_institution_branch
        self.country = country


class __FinancialGuaranteeType(PrefixCAC, ComplexXMLParseableObject):
    guarantee_type_code = None
    description = None
    liability_amount = None
    amount_rate = None
    constitution_period = None
    order_list = [
        'guarantee_type_code',
        'description',
        'liability_amount',
        'amount_rate',
        'constitution_period',
    ]

    def __init__(self,		guarantee_type_code: cbc.GuaranteeTypeCode,
                 description: List[cbc.Description] = None,
                 liability_amount: cbc.LiabilityAmount = None,
                 amount_rate: cbc.AmountRate = None,
                 constitution_period: 'ConstitutionPeriod' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.guarantee_type_code = guarantee_type_code
        self.description = description
        self.liability_amount = liability_amount
        self.amount_rate = amount_rate
        self.constitution_period = constitution_period


class __FinancialInstitutionType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    name = None
    address = None
    order_list = [
        'id_',
        'name',
        'address',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 name: cbc.Name = None,
                 address: 'Address' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.name = name
        self.address = address


class __ForecastExceptionType(PrefixCAC, ComplexXMLParseableObject):
    forecast_purpose_code = None
    forecast_type_code = None
    issue_date = None
    data_source_code = None
    issue_time = None
    comparison_data_code = None
    comparison_forecast_issue_time = None
    comparison_forecast_issue_date = None
    order_list = [
        'forecast_purpose_code',
        'forecast_type_code',
        'issue_date',
        'issue_time',
        'data_source_code',
        'comparison_data_code',
        'comparison_forecast_issue_time',
        'comparison_forecast_issue_date',
    ]

    def __init__(self,		forecast_purpose_code: cbc.ForecastPurposeCode,
                 forecast_type_code: cbc.ForecastTypeCode,
                 issue_date: cbc.IssueDate,
                 data_source_code: cbc.DataSourceCode,
                 issue_time: cbc.IssueTime = None,
                 comparison_data_code: cbc.ComparisonDataCode = None,
                 comparison_forecast_issue_time: cbc.ComparisonForecastIssueTime = None,
                 comparison_forecast_issue_date: cbc.ComparisonForecastIssueDate = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.forecast_purpose_code = forecast_purpose_code
        self.forecast_type_code = forecast_type_code
        self.issue_date = issue_date
        self.data_source_code = data_source_code
        self.issue_time = issue_time
        self.comparison_data_code = comparison_data_code
        self.comparison_forecast_issue_time = comparison_forecast_issue_time
        self.comparison_forecast_issue_date = comparison_forecast_issue_date


class __ForecastExceptionCriterionLineType(PrefixCAC, ComplexXMLParseableObject):
    forecast_purpose_code = None
    forecast_type_code = None
    data_source_code = None
    comparison_data_source_code = None
    time_delta_days_quantity = None
    order_list = [
        'forecast_purpose_code',
        'forecast_type_code',
        'comparison_data_source_code',
        'data_source_code',
        'time_delta_days_quantity',
    ]

    def __init__(self,		forecast_purpose_code: cbc.ForecastPurposeCode,
                 forecast_type_code: cbc.ForecastTypeCode,
                 data_source_code: cbc.DataSourceCode,
                 comparison_data_source_code: cbc.ComparisonDataSourceCode = None,
                 time_delta_days_quantity: cbc.TimeDeltaDaysQuantity = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.forecast_purpose_code = forecast_purpose_code
        self.forecast_type_code = forecast_type_code
        self.data_source_code = data_source_code
        self.comparison_data_source_code = comparison_data_source_code
        self.time_delta_days_quantity = time_delta_days_quantity


class __ForecastLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    forecast_type_code = None
    note = None
    frozen_document_indicator = None
    forecast_period = None
    sales_item = None
    order_list = [
        'id_',
        'note',
        'frozen_document_indicator',
        'forecast_type_code',
        'forecast_period',
        'sales_item',
    ]

    def __init__(self,		id_: cbc.ID,
                 forecast_type_code: cbc.ForecastTypeCode,
                 note: List[cbc.Note] = None,
                 frozen_document_indicator: cbc.FrozenDocumentIndicator = None,
                 forecast_period: 'ForecastPeriod' = None,
                 sales_item: 'SalesItem' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.forecast_type_code = forecast_type_code
        self.note = note
        self.frozen_document_indicator = frozen_document_indicator
        self.forecast_period = forecast_period
        self.sales_item = sales_item


class __ForecastRevisionLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    revised_forecast_line_id = None
    source_forecast_issue_date = None
    source_forecast_issue_time = None
    note = None
    description = None
    adjustment_reason_code = None
    forecast_period = None
    sales_item = None
    order_list = [
        'id_',
        'note',
        'description',
        'revised_forecast_line_id',
        'source_forecast_issue_date',
        'source_forecast_issue_time',
        'adjustment_reason_code',
        'forecast_period',
        'sales_item',
    ]

    def __init__(self,		id_: cbc.ID,
                 revised_forecast_line_id: cbc.RevisedForecastLineID,
                 source_forecast_issue_date: cbc.SourceForecastIssueDate,
                 source_forecast_issue_time: cbc.SourceForecastIssueTime,
                 note: List[cbc.Note] = None,
                 description: List[cbc.Description] = None,
                 adjustment_reason_code: cbc.AdjustmentReasonCode = None,
                 forecast_period: 'ForecastPeriod' = None,
                 sales_item: 'SalesItem' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.revised_forecast_line_id = revised_forecast_line_id
        self.source_forecast_issue_date = source_forecast_issue_date
        self.source_forecast_issue_time = source_forecast_issue_time
        self.note = note
        self.description = description
        self.adjustment_reason_code = adjustment_reason_code
        self.forecast_period = forecast_period
        self.sales_item = sales_item


class __FrameworkAgreementType(PrefixCAC, ComplexXMLParseableObject):
    expected_operator_quantity = None
    maximum_operator_quantity = None
    justification = None
    frequency = None
    duration_period = None
    subsequent_process_tender_requirement = None
    order_list = [
        'expected_operator_quantity',
        'maximum_operator_quantity',
        'justification',
        'frequency',
        'duration_period',
        'subsequent_process_tender_requirement',
    ]

    def __init__(self,		expected_operator_quantity: cbc.ExpectedOperatorQuantity = None,
                 maximum_operator_quantity: cbc.MaximumOperatorQuantity = None,
                 justification: List[cbc.Justification] = None,
                 frequency: List[cbc.Frequency] = None,
                 duration_period: 'DurationPeriod' = None,
                 subsequent_process_tender_requirement: List['SubsequentProcessTenderRequirement'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.expected_operator_quantity = expected_operator_quantity
        self.maximum_operator_quantity = maximum_operator_quantity
        self.justification = justification
        self.frequency = frequency
        self.duration_period = duration_period
        self.subsequent_process_tender_requirement = subsequent_process_tender_requirement


class __GoodsItemType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    sequence_number_id = None
    description = None
    hazardous_risk_indicator = None
    declared_customs_value_amount = None
    declared_for_carriage_value_amount = None
    declared_statistics_value_amount = None
    free_on_board_value_amount = None
    insurance_value_amount = None
    value_amount = None
    gross_weight_measure = None
    net_weight_measure = None
    net_net_weight_measure = None
    chargeable_weight_measure = None
    gross_volume_measure = None
    net_volume_measure = None
    quantity = None
    preference_criterion_code = None
    required_customs_id = None
    customs_status_code = None
    customs_tariff_quantity = None
    customs_import_classified_indicator = None
    chargeable_quantity = None
    returnable_quantity = None
    trace_id = None
    item = None
    goods_item_container = None
    freight_allowance_charge = None
    invoice_line = None
    temperature = None
    contained_goods_item = None
    origin_address = None
    delivery = None
    pickup = None
    despatch = None
    measurement_dimension = None
    containing_package = None
    shipment_document_reference = None
    minimum_temperature = None
    maximum_temperature = None
    order_list = [
        'id_',
        'sequence_number_id',
        'description',
        'hazardous_risk_indicator',
        'declared_customs_value_amount',
        'declared_for_carriage_value_amount',
        'declared_statistics_value_amount',
        'free_on_board_value_amount',
        'insurance_value_amount',
        'value_amount',
        'gross_weight_measure',
        'net_weight_measure',
        'net_net_weight_measure',
        'chargeable_weight_measure',
        'gross_volume_measure',
        'net_volume_measure',
        'quantity',
        'preference_criterion_code',
        'required_customs_id',
        'customs_status_code',
        'customs_tariff_quantity',
        'customs_import_classified_indicator',
        'chargeable_quantity',
        'returnable_quantity',
        'trace_id',
        'item',
        'goods_item_container',
        'freight_allowance_charge',
        'invoice_line',
        'temperature',
        'contained_goods_item',
        'origin_address',
        'delivery',
        'pickup',
        'despatch',
        'measurement_dimension',
        'containing_package',
        'shipment_document_reference',
        'minimum_temperature',
        'maximum_temperature',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 sequence_number_id: cbc.SequenceNumberID = None,
                 description: List[cbc.Description] = None,
                 hazardous_risk_indicator: cbc.HazardousRiskIndicator = None,
                 declared_customs_value_amount: cbc.DeclaredCustomsValueAmount = None,
                 declared_for_carriage_value_amount: cbc.DeclaredForCarriageValueAmount = None,
                 declared_statistics_value_amount: cbc.DeclaredStatisticsValueAmount = None,
                 free_on_board_value_amount: cbc.FreeOnBoardValueAmount = None,
                 insurance_value_amount: cbc.InsuranceValueAmount = None,
                 value_amount: cbc.ValueAmount = None,
                 gross_weight_measure: cbc.GrossWeightMeasure = None,
                 net_weight_measure: cbc.NetWeightMeasure = None,
                 net_net_weight_measure: cbc.NetNetWeightMeasure = None,
                 chargeable_weight_measure: cbc.ChargeableWeightMeasure = None,
                 gross_volume_measure: cbc.GrossVolumeMeasure = None,
                 net_volume_measure: cbc.NetVolumeMeasure = None,
                 quantity: cbc.Quantity = None,
                 preference_criterion_code: cbc.PreferenceCriterionCode = None,
                 required_customs_id: cbc.RequiredCustomsID = None,
                 customs_status_code: cbc.CustomsStatusCode = None,
                 customs_tariff_quantity: cbc.CustomsTariffQuantity = None,
                 customs_import_classified_indicator: cbc.CustomsImportClassifiedIndicator = None,
                 chargeable_quantity: cbc.ChargeableQuantity = None,
                 returnable_quantity: cbc.ReturnableQuantity = None,
                 trace_id: cbc.TraceID = None,
                 item: List['Item'] = None,
                 goods_item_container: List['GoodsItemContainer'] = None,
                 freight_allowance_charge: List['FreightAllowanceCharge'] = None,
                 invoice_line: List['InvoiceLine'] = None,
                 temperature: List['Temperature'] = None,
                 contained_goods_item: List['ContainedGoodsItem'] = None,
                 origin_address: 'OriginAddress' = None,
                 delivery: 'Delivery' = None,
                 pickup: 'Pickup' = None,
                 despatch: 'Despatch' = None,
                 measurement_dimension: List['MeasurementDimension'] = None,
                 containing_package: List['ContainingPackage'] = None,
                 shipment_document_reference: 'ShipmentDocumentReference' = None,
                 minimum_temperature: 'MinimumTemperature' = None,
                 maximum_temperature: 'MaximumTemperature' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.sequence_number_id = sequence_number_id
        self.description = description
        self.hazardous_risk_indicator = hazardous_risk_indicator
        self.declared_customs_value_amount = declared_customs_value_amount
        self.declared_for_carriage_value_amount = declared_for_carriage_value_amount
        self.declared_statistics_value_amount = declared_statistics_value_amount
        self.free_on_board_value_amount = free_on_board_value_amount
        self.insurance_value_amount = insurance_value_amount
        self.value_amount = value_amount
        self.gross_weight_measure = gross_weight_measure
        self.net_weight_measure = net_weight_measure
        self.net_net_weight_measure = net_net_weight_measure
        self.chargeable_weight_measure = chargeable_weight_measure
        self.gross_volume_measure = gross_volume_measure
        self.net_volume_measure = net_volume_measure
        self.quantity = quantity
        self.preference_criterion_code = preference_criterion_code
        self.required_customs_id = required_customs_id
        self.customs_status_code = customs_status_code
        self.customs_tariff_quantity = customs_tariff_quantity
        self.customs_import_classified_indicator = customs_import_classified_indicator
        self.chargeable_quantity = chargeable_quantity
        self.returnable_quantity = returnable_quantity
        self.trace_id = trace_id
        self.item = item
        self.goods_item_container = goods_item_container
        self.freight_allowance_charge = freight_allowance_charge
        self.invoice_line = invoice_line
        self.temperature = temperature
        self.contained_goods_item = contained_goods_item
        self.origin_address = origin_address
        self.delivery = delivery
        self.pickup = pickup
        self.despatch = despatch
        self.measurement_dimension = measurement_dimension
        self.containing_package = containing_package
        self.shipment_document_reference = shipment_document_reference
        self.minimum_temperature = minimum_temperature
        self.maximum_temperature = maximum_temperature


class __GoodsItemContainerType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    quantity = None
    transport_equipment = None
    order_list = [
        'id_',
        'quantity',
        'transport_equipment',
    ]

    def __init__(self,		id_: cbc.ID,
                 quantity: cbc.Quantity = None,
                 transport_equipment: List['TransportEquipment'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.quantity = quantity
        self.transport_equipment = transport_equipment


class __HazardousGoodsTransitType(PrefixCAC, ComplexXMLParseableObject):
    transport_emergency_card_code = None
    packing_criteria_code = None
    hazardous_regulation_code = None
    inhalation_toxicity_zone_code = None
    transport_authorization_code = None
    maximum_temperature = None
    minimum_temperature = None
    order_list = [
        'transport_emergency_card_code',
        'packing_criteria_code',
        'hazardous_regulation_code',
        'inhalation_toxicity_zone_code',
        'transport_authorization_code',
        'maximum_temperature',
        'minimum_temperature',
    ]

    def __init__(self,		transport_emergency_card_code: cbc.TransportEmergencyCardCode = None,
                 packing_criteria_code: cbc.PackingCriteriaCode = None,
                 hazardous_regulation_code: cbc.HazardousRegulationCode = None,
                 inhalation_toxicity_zone_code: cbc.InhalationToxicityZoneCode = None,
                 transport_authorization_code: cbc.TransportAuthorizationCode = None,
                 maximum_temperature: 'MaximumTemperature' = None,
                 minimum_temperature: 'MinimumTemperature' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.transport_emergency_card_code = transport_emergency_card_code
        self.packing_criteria_code = packing_criteria_code
        self.hazardous_regulation_code = hazardous_regulation_code
        self.inhalation_toxicity_zone_code = inhalation_toxicity_zone_code
        self.transport_authorization_code = transport_authorization_code
        self.maximum_temperature = maximum_temperature
        self.minimum_temperature = minimum_temperature


class __HazardousItemType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    placard_notation = None
    placard_endorsement = None
    additional_information = None
    undgcode = None
    emergency_procedures_code = None
    medical_first_aid_guide_code = None
    technical_name = None
    category_name = None
    hazardous_category_code = None
    upper_orange_hazard_placard_id = None
    lower_orange_hazard_placard_id = None
    marking_id = None
    hazard_class_id = None
    net_weight_measure = None
    net_volume_measure = None
    quantity = None
    contact_party = None
    secondary_hazard = None
    hazardous_goods_transit = None
    emergency_temperature = None
    flashpoint_temperature = None
    additional_temperature = None
    order_list = [
        'id_',
        'placard_notation',
        'placard_endorsement',
        'additional_information',
        'undgcode',
        'emergency_procedures_code',
        'medical_first_aid_guide_code',
        'technical_name',
        'category_name',
        'hazardous_category_code',
        'upper_orange_hazard_placard_id',
        'lower_orange_hazard_placard_id',
        'marking_id',
        'hazard_class_id',
        'net_weight_measure',
        'net_volume_measure',
        'quantity',
        'contact_party',
        'secondary_hazard',
        'hazardous_goods_transit',
        'emergency_temperature',
        'flashpoint_temperature',
        'additional_temperature',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 placard_notation: cbc.PlacardNotation = None,
                 placard_endorsement: cbc.PlacardEndorsement = None,
                 additional_information: List[cbc.AdditionalInformation] = None,
                 undgcode: cbc.UNDGCode = None,
                 emergency_procedures_code: cbc.EmergencyProceduresCode = None,
                 medical_first_aid_guide_code: cbc.MedicalFirstAidGuideCode = None,
                 technical_name: cbc.TechnicalName = None,
                 category_name: cbc.CategoryName = None,
                 hazardous_category_code: cbc.HazardousCategoryCode = None,
                 upper_orange_hazard_placard_id: cbc.UpperOrangeHazardPlacardID = None,
                 lower_orange_hazard_placard_id: cbc.LowerOrangeHazardPlacardID = None,
                 marking_id: cbc.MarkingID = None,
                 hazard_class_id: cbc.HazardClassID = None,
                 net_weight_measure: cbc.NetWeightMeasure = None,
                 net_volume_measure: cbc.NetVolumeMeasure = None,
                 quantity: cbc.Quantity = None,
                 contact_party: 'ContactParty' = None,
                 secondary_hazard: List['SecondaryHazard'] = None,
                 hazardous_goods_transit: List['HazardousGoodsTransit'] = None,
                 emergency_temperature: 'EmergencyTemperature' = None,
                 flashpoint_temperature: 'FlashpointTemperature' = None,
                 additional_temperature: List['AdditionalTemperature'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.placard_notation = placard_notation
        self.placard_endorsement = placard_endorsement
        self.additional_information = additional_information
        self.undgcode = undgcode
        self.emergency_procedures_code = emergency_procedures_code
        self.medical_first_aid_guide_code = medical_first_aid_guide_code
        self.technical_name = technical_name
        self.category_name = category_name
        self.hazardous_category_code = hazardous_category_code
        self.upper_orange_hazard_placard_id = upper_orange_hazard_placard_id
        self.lower_orange_hazard_placard_id = lower_orange_hazard_placard_id
        self.marking_id = marking_id
        self.hazard_class_id = hazard_class_id
        self.net_weight_measure = net_weight_measure
        self.net_volume_measure = net_volume_measure
        self.quantity = quantity
        self.contact_party = contact_party
        self.secondary_hazard = secondary_hazard
        self.hazardous_goods_transit = hazardous_goods_transit
        self.emergency_temperature = emergency_temperature
        self.flashpoint_temperature = flashpoint_temperature
        self.additional_temperature = additional_temperature


class __ImmobilizedSecurityType(PrefixCAC, ComplexXMLParseableObject):
    immobilization_certificate_id = None
    security_id = None
    issue_date = None
    face_value_amount = None
    market_value_amount = None
    shares_number_quantity = None
    issuer_party = None
    order_list = [
        'immobilization_certificate_id',
        'security_id',
        'issue_date',
        'face_value_amount',
        'market_value_amount',
        'shares_number_quantity',
        'issuer_party',
    ]

    def __init__(self,		immobilization_certificate_id: cbc.ImmobilizationCertificateID = None,
                 security_id: cbc.SecurityID = None,
                 issue_date: cbc.IssueDate = None,
                 face_value_amount: cbc.FaceValueAmount = None,
                 market_value_amount: cbc.MarketValueAmount = None,
                 shares_number_quantity: cbc.SharesNumberQuantity = None,
                 issuer_party: 'IssuerParty' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.immobilization_certificate_id = immobilization_certificate_id
        self.security_id = security_id
        self.issue_date = issue_date
        self.face_value_amount = face_value_amount
        self.market_value_amount = market_value_amount
        self.shares_number_quantity = shares_number_quantity
        self.issuer_party = issuer_party


class __InstructionForReturnsLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    quantity = None
    item = None
    note = None
    manufacturer_party = None
    order_list = [
        'id_',
        'note',
        'quantity',
        'manufacturer_party',
        'item',
    ]

    def __init__(self,		id_: cbc.ID,
                 quantity: cbc.Quantity,
                 item: 'Item',
                 note: List[cbc.Note] = None,
                 manufacturer_party: 'ManufacturerParty' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.quantity = quantity
        self.item = item
        self.note = note
        self.manufacturer_party = manufacturer_party


class __InventoryReportLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    quantity = None
    item = None
    note = None
    inventory_value_amount = None
    availability_date = None
    availability_status_code = None
    inventory_location = None
    order_list = [
        'id_',
        'note',
        'quantity',
        'inventory_value_amount',
        'availability_date',
        'availability_status_code',
        'item',
        'inventory_location',
    ]

    def __init__(self,		id_: cbc.ID,
                 quantity: cbc.Quantity,
                 item: 'Item',
                 note: List[cbc.Note] = None,
                 inventory_value_amount: cbc.InventoryValueAmount = None,
                 availability_date: cbc.AvailabilityDate = None,
                 availability_status_code: cbc.AvailabilityStatusCode = None,
                 inventory_location: 'InventoryLocation' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.quantity = quantity
        self.item = item
        self.note = note
        self.inventory_value_amount = inventory_value_amount
        self.availability_date = availability_date
        self.availability_status_code = availability_status_code
        self.inventory_location = inventory_location


class __InvoiceLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    line_extension_amount = None
    item = None
    uuid = None
    note = None
    invoiced_quantity = None
    tax_point_date = None
    accounting_cost_code = None
    accounting_cost = None
    payment_purpose_code = None
    free_of_charge_indicator = None
    invoice_period = None
    order_line_reference = None
    despatch_line_reference = None
    receipt_line_reference = None
    billing_reference = None
    document_reference = None
    pricing_reference = None
    originator_party = None
    delivery = None
    payment_terms = None
    allowance_charge = None
    tax_total = None
    withholding_tax_total = None
    price = None
    delivery_terms = None
    sub_invoice_line = None
    item_price_extension = None
    order_list = [
        'id_',
        'uuid',
        'note',
        'invoiced_quantity',
        'line_extension_amount',
        'tax_point_date',
        'accounting_cost_code',
        'accounting_cost',
        'payment_purpose_code',
        'free_of_charge_indicator',
        'invoice_period',
        'order_line_reference',
        'despatch_line_reference',
        'receipt_line_reference',
        'billing_reference',
        'document_reference',
        'pricing_reference',
        'originator_party',
        'delivery',
        'payment_terms',
        'allowance_charge',
        'tax_total',
        'withholding_tax_total',
        'item',
        'price',
        'delivery_terms',
        'sub_invoice_line',
        'item_price_extension',
    ]

    def __init__(self,		id_: cbc.ID,
                 line_extension_amount: cbc.LineExtensionAmount,
                 item: 'Item',
                 uuid: cbc.UUID = None,
                 note: List[cbc.Note] = None,
                 invoiced_quantity: cbc.InvoicedQuantity = None,
                 tax_point_date: cbc.TaxPointDate = None,
                 accounting_cost_code: cbc.AccountingCostCode = None,
                 accounting_cost: cbc.AccountingCost = None,
                 payment_purpose_code: cbc.PaymentPurposeCode = None,
                 free_of_charge_indicator: cbc.FreeOfChargeIndicator = None,
                 invoice_period: List['InvoicePeriod'] = None,
                 order_line_reference: List['OrderLineReference'] = None,
                 despatch_line_reference: List['DespatchLineReference'] = None,
                 receipt_line_reference: List['ReceiptLineReference'] = None,
                 billing_reference: List['BillingReference'] = None,
                 document_reference: List['DocumentReference'] = None,
                 pricing_reference: 'PricingReference' = None,
                 originator_party: 'OriginatorParty' = None,
                 delivery: List['Delivery'] = None,
                 payment_terms: List['PaymentTerms'] = None,
                 allowance_charge: List['AllowanceCharge'] = None,
                 tax_total: List['TaxTotal'] = None,
                 withholding_tax_total: List['WithholdingTaxTotal'] = None,
                 price: 'Price' = None,
                 delivery_terms: 'DeliveryTerms' = None,
                 sub_invoice_line: List['SubInvoiceLine'] = None,
                 item_price_extension: 'ItemPriceExtension' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.line_extension_amount = line_extension_amount
        self.item = item
        self.uuid = uuid
        self.note = note
        self.invoiced_quantity = invoiced_quantity
        self.tax_point_date = tax_point_date
        self.accounting_cost_code = accounting_cost_code
        self.accounting_cost = accounting_cost
        self.payment_purpose_code = payment_purpose_code
        self.free_of_charge_indicator = free_of_charge_indicator
        self.invoice_period = invoice_period
        self.order_line_reference = order_line_reference
        self.despatch_line_reference = despatch_line_reference
        self.receipt_line_reference = receipt_line_reference
        self.billing_reference = billing_reference
        self.document_reference = document_reference
        self.pricing_reference = pricing_reference
        self.originator_party = originator_party
        self.delivery = delivery
        self.payment_terms = payment_terms
        self.allowance_charge = allowance_charge
        self.tax_total = tax_total
        self.withholding_tax_total = withholding_tax_total
        self.price = price
        self.delivery_terms = delivery_terms
        self.sub_invoice_line = sub_invoice_line
        self.item_price_extension = item_price_extension


class __ItemType(PrefixCAC, ComplexXMLParseableObject):
    description = None
    pack_quantity = None
    pack_size_numeric = None
    catalogue_indicator = None
    name = None
    hazardous_risk_indicator = None
    additional_information = None
    keyword = None
    brand_name = None
    model_name = None
    buyers_item_identification = None
    sellers_item_identification = None
    manufacturers_item_identification = None
    standard_item_identification = None
    catalogue_item_identification = None
    additional_item_identification = None
    catalogue_document_reference = None
    item_specification_document_reference = None
    origin_country = None
    commodity_classification = None
    transaction_conditions = None
    hazardous_item = None
    classified_tax_category = None
    additional_item_property = None
    manufacturer_party = None
    information_content_provider_party = None
    origin_address = None
    item_instance = None
    certificate = None
    dimension = None
    order_list = [
        'description',
        'pack_quantity',
        'pack_size_numeric',
        'catalogue_indicator',
        'name',
        'hazardous_risk_indicator',
        'additional_information',
        'keyword',
        'brand_name',
        'model_name',
        'buyers_item_identification',
        'sellers_item_identification',
        'manufacturers_item_identification',
        'standard_item_identification',
        'catalogue_item_identification',
        'additional_item_identification',
        'catalogue_document_reference',
        'item_specification_document_reference',
        'origin_country',
        'commodity_classification',
        'transaction_conditions',
        'hazardous_item',
        'classified_tax_category',
        'additional_item_property',
        'manufacturer_party',
        'information_content_provider_party',
        'origin_address',
        'item_instance',
        'certificate',
        'dimension',
    ]

    def __init__(self,		description: List[cbc.Description] = None,
                 pack_quantity: cbc.PackQuantity = None,
                 pack_size_numeric: cbc.PackSizeNumeric = None,
                 catalogue_indicator: cbc.CatalogueIndicator = None,
                 name: cbc.Name = None,
                 hazardous_risk_indicator: cbc.HazardousRiskIndicator = None,
                 additional_information: List[cbc.AdditionalInformation] = None,
                 keyword: List[cbc.Keyword] = None,
                 brand_name: List[cbc.BrandName] = None,
                 model_name: List[cbc.ModelName] = None,
                 buyers_item_identification: 'BuyersItemIdentification' = None,
                 sellers_item_identification: 'SellersItemIdentification' = None,
                 manufacturers_item_identification: List['ManufacturersItemIdentification'] = None,
                 standard_item_identification: 'StandardItemIdentification' = None,
                 catalogue_item_identification: 'CatalogueItemIdentification' = None,
                 additional_item_identification: List['AdditionalItemIdentification'] = None,
                 catalogue_document_reference: 'CatalogueDocumentReference' = None,
                 item_specification_document_reference: List['ItemSpecificationDocumentReference'] = None,
                 origin_country: 'OriginCountry' = None,
                 commodity_classification: List['CommodityClassification'] = None,
                 transaction_conditions: List['TransactionConditions'] = None,
                 hazardous_item: List['HazardousItem'] = None,
                 classified_tax_category: List['ClassifiedTaxCategory'] = None,
                 additional_item_property: List['AdditionalItemProperty'] = None,
                 manufacturer_party: List['ManufacturerParty'] = None,
                 information_content_provider_party: 'InformationContentProviderParty' = None,
                 origin_address: List['OriginAddress'] = None,
                 item_instance: List['ItemInstance'] = None,
                 certificate: List['Certificate'] = None,
                 dimension: List['Dimension'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.description = description
        self.pack_quantity = pack_quantity
        self.pack_size_numeric = pack_size_numeric
        self.catalogue_indicator = catalogue_indicator
        self.name = name
        self.hazardous_risk_indicator = hazardous_risk_indicator
        self.additional_information = additional_information
        self.keyword = keyword
        self.brand_name = brand_name
        self.model_name = model_name
        self.buyers_item_identification = buyers_item_identification
        self.sellers_item_identification = sellers_item_identification
        self.manufacturers_item_identification = manufacturers_item_identification
        self.standard_item_identification = standard_item_identification
        self.catalogue_item_identification = catalogue_item_identification
        self.additional_item_identification = additional_item_identification
        self.catalogue_document_reference = catalogue_document_reference
        self.item_specification_document_reference = item_specification_document_reference
        self.origin_country = origin_country
        self.commodity_classification = commodity_classification
        self.transaction_conditions = transaction_conditions
        self.hazardous_item = hazardous_item
        self.classified_tax_category = classified_tax_category
        self.additional_item_property = additional_item_property
        self.manufacturer_party = manufacturer_party
        self.information_content_provider_party = information_content_provider_party
        self.origin_address = origin_address
        self.item_instance = item_instance
        self.certificate = certificate
        self.dimension = dimension


class __ItemComparisonType(PrefixCAC, ComplexXMLParseableObject):
    price_amount = None
    quantity = None
    order_list = [
        'price_amount',
        'quantity',
    ]
    def __init__(self,		price_amount: cbc.PriceAmount = None,
                 quantity: cbc.Quantity = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.price_amount = price_amount
        self.quantity = quantity


class __ItemIdentificationType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    extended_id = None
    barcode_symbology_id = None
    physical_attribute = None
    measurement_dimension = None
    issuer_party = None
    order_list = [
        'id_',
        'extended_id',
        'barcode_symbology_id',
        'physical_attribute',
        'measurement_dimension',
        'issuer_party',
    ]

    def __init__(self,		id_: cbc.ID,
                 extended_id: cbc.ExtendedID = None,
                 barcode_symbology_id: cbc.BarcodeSymbologyID = None,
                 physical_attribute: List['PhysicalAttribute'] = None,
                 measurement_dimension: List['MeasurementDimension'] = None,
                 issuer_party: 'IssuerParty' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.extended_id = extended_id
        self.barcode_symbology_id = barcode_symbology_id
        self.physical_attribute = physical_attribute
        self.measurement_dimension = measurement_dimension
        self.issuer_party = issuer_party


class __ItemInformationRequestLineType(PrefixCAC, ComplexXMLParseableObject):
    time_frequency_code = None
    supply_chain_activity_type_code = None
    forecast_type_code = None
    performance_metric_type_code = None
    period = None
    sales_item = None
    order_list = [
        'time_frequency_code',
        'supply_chain_activity_type_code',
        'forecast_type_code',
        'performance_metric_type_code',
        'period',
        'sales_item',
    ]

    def __init__(self,		time_frequency_code: cbc.TimeFrequencyCode = None,
                 supply_chain_activity_type_code: cbc.SupplyChainActivityTypeCode = None,
                 forecast_type_code: cbc.ForecastTypeCode = None,
                 performance_metric_type_code: cbc.PerformanceMetricTypeCode = None,
                 period: List['Period'] = None,
                 sales_item: List['SalesItem'] = None, xml_namespaces=None):
        if not period:
            raise ListMustNotBeEmptyException('period')
        if not sales_item:
            raise ListMustNotBeEmptyException('sales_item')
        super().__init__(xml_namespaces)
        self.time_frequency_code = time_frequency_code
        self.supply_chain_activity_type_code = supply_chain_activity_type_code
        self.forecast_type_code = forecast_type_code
        self.performance_metric_type_code = performance_metric_type_code
        self.period = period
        self.sales_item = sales_item


class __ItemInstanceType(PrefixCAC, ComplexXMLParseableObject):
    product_trace_id = None
    manufacture_date = None
    manufacture_time = None
    best_before_date = None
    registration_id = None
    serial_id = None
    additional_item_property = None
    lot_identification = None
    order_list = [
        'product_trace_id',
        'manufacture_date',
        'manufacture_time',
        'best_before_date',
        'registration_id',
        'serial_id',
        'additional_item_property',
        'lot_identification',
    ]

    def __init__(self,		product_trace_id: cbc.ProductTraceID = None,
                 manufacture_date: cbc.ManufactureDate = None,
                 manufacture_time: cbc.ManufactureTime = None,
                 best_before_date: cbc.BestBeforeDate = None,
                 registration_id: cbc.RegistrationID = None,
                 serial_id: cbc.SerialID = None,
                 additional_item_property: List['AdditionalItemProperty'] = None,
                 lot_identification: 'LotIdentification' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.product_trace_id = product_trace_id
        self.manufacture_date = manufacture_date
        self.manufacture_time = manufacture_time
        self.best_before_date = best_before_date
        self.registration_id = registration_id
        self.serial_id = serial_id
        self.additional_item_property = additional_item_property
        self.lot_identification = lot_identification


class __ItemLocationQuantityType(PrefixCAC, ComplexXMLParseableObject):
    lead_time_measure = None
    minimum_quantity = None
    maximum_quantity = None
    hazardous_risk_indicator = None
    trading_restrictions = None
    applicable_territory_address = None
    price = None
    delivery_unit = None
    applicable_tax_category = None
    package = None
    allowance_charge = None
    dependent_price_reference = None
    order_list = [
        'lead_time_measure',
        'minimum_quantity',
        'maximum_quantity',
        'hazardous_risk_indicator',
        'trading_restrictions',
        'applicable_territory_address',
        'price',
        'delivery_unit',
        'applicable_tax_category',
        'package',
        'allowance_charge',
        'dependent_price_reference',
    ]

    def __init__(self,		lead_time_measure: cbc.LeadTimeMeasure = None,
                 minimum_quantity: cbc.MinimumQuantity = None,
                 maximum_quantity: cbc.MaximumQuantity = None,
                 hazardous_risk_indicator: cbc.HazardousRiskIndicator = None,
                 trading_restrictions: List[cbc.TradingRestrictions] = None,
                 applicable_territory_address: List['ApplicableTerritoryAddress'] = None,
                 price: 'Price' = None,
                 delivery_unit: List['DeliveryUnit'] = None,
                 applicable_tax_category: List['ApplicableTaxCategory'] = None,
                 package: 'Package' = None,
                 allowance_charge: List['AllowanceCharge'] = None,
                 dependent_price_reference: 'DependentPriceReference' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.lead_time_measure = lead_time_measure
        self.minimum_quantity = minimum_quantity
        self.maximum_quantity = maximum_quantity
        self.hazardous_risk_indicator = hazardous_risk_indicator
        self.trading_restrictions = trading_restrictions
        self.applicable_territory_address = applicable_territory_address
        self.price = price
        self.delivery_unit = delivery_unit
        self.applicable_tax_category = applicable_tax_category
        self.package = package
        self.allowance_charge = allowance_charge
        self.dependent_price_reference = dependent_price_reference


class __ItemManagementProfileType(PrefixCAC, ComplexXMLParseableObject):
    effective_period = None
    item = None
    frozen_period_days_numeric = None
    minimum_inventory_quantity = None
    multiple_order_quantity = None
    order_interval_days_numeric = None
    replenishment_owner_description = None
    target_service_percent = None
    target_inventory_quantity = None
    item_location_quantity = None
    order_list = [
        'frozen_period_days_numeric',
        'minimum_inventory_quantity',
        'multiple_order_quantity',
        'order_interval_days_numeric',
        'replenishment_owner_description',
        'target_service_percent',
        'target_inventory_quantity',
        'effective_period',
        'item',
        'item_location_quantity',
    ]

    def __init__(self,		effective_period: 'EffectivePeriod',
                 item: 'Item',
                 frozen_period_days_numeric: cbc.FrozenPeriodDaysNumeric = None,
                 minimum_inventory_quantity: cbc.MinimumInventoryQuantity = None,
                 multiple_order_quantity: cbc.MultipleOrderQuantity = None,
                 order_interval_days_numeric: cbc.OrderIntervalDaysNumeric = None,
                 replenishment_owner_description: List[cbc.ReplenishmentOwnerDescription] = None,
                 target_service_percent: cbc.TargetServicePercent = None,
                 target_inventory_quantity: cbc.TargetInventoryQuantity = None,
                 item_location_quantity: 'ItemLocationQuantity' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.effective_period = effective_period
        self.item = item
        self.frozen_period_days_numeric = frozen_period_days_numeric
        self.minimum_inventory_quantity = minimum_inventory_quantity
        self.multiple_order_quantity = multiple_order_quantity
        self.order_interval_days_numeric = order_interval_days_numeric
        self.replenishment_owner_description = replenishment_owner_description
        self.target_service_percent = target_service_percent
        self.target_inventory_quantity = target_inventory_quantity
        self.item_location_quantity = item_location_quantity


class __ItemPropertyType(PrefixCAC, ComplexXMLParseableObject):
    name = None
    id_ = None
    name_code = None
    test_method = None
    value = None
    value_quantity = None
    value_qualifier = None
    importance_code = None
    list_value = None
    usability_period = None
    item_property_group = None
    range_dimension = None
    item_property_range = None
    order_list = [
        'id_',
        'name',
        'name_code',
        'test_method',
        'value',
        'value_quantity',
        'value_qualifier',
        'importance_code',
        'list_value',
        'usability_period',
        'item_property_group',
        'range_dimension',
        'item_property_range',
    ]

    def __init__(self,		name: cbc.Name,
                 id_: cbc.ID = None,
                 name_code: cbc.NameCode = None,
                 test_method: cbc.TestMethod = None,
                 value: cbc.Value = None,
                 value_quantity: cbc.ValueQuantity = None,
                 value_qualifier: List[cbc.ValueQualifier] = None,
                 importance_code: cbc.ImportanceCode = None,
                 list_value: List[cbc.ListValue] = None,
                 usability_period: 'UsabilityPeriod' = None,
                 item_property_group: List['ItemPropertyGroup'] = None,
                 range_dimension: 'RangeDimension' = None,
                 item_property_range: 'ItemPropertyRange' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.name = name
        self.id_ = id_
        self.name_code = name_code
        self.test_method = test_method
        self.value = value
        self.value_quantity = value_quantity
        self.value_qualifier = value_qualifier
        self.importance_code = importance_code
        self.list_value = list_value
        self.usability_period = usability_period
        self.item_property_group = item_property_group
        self.range_dimension = range_dimension
        self.item_property_range = item_property_range


class __ItemPropertyGroupType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    name = None
    importance_code = None
    order_list = [
        'id_',
        'name',
        'importance_code',
    ]

    def __init__(self,		id_: cbc.ID,
                 name: cbc.Name = None,
                 importance_code: cbc.ImportanceCode = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.name = name
        self.importance_code = importance_code


class __ItemPropertyRangeType(PrefixCAC, ComplexXMLParseableObject):
    minimum_value = None
    maximum_value = None
    order_list = [
        'minimum_value',
        'maximum_value',
    ]
    def __init__(self,		minimum_value: cbc.MinimumValue = None,
                 maximum_value: cbc.MaximumValue = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value


class __LanguageType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    name = None
    locale_code = None
    order_list = [
        'id_',
        'name',
        'locale_code',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 name: cbc.Name = None,
                 locale_code: cbc.LocaleCode = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.name = name
        self.locale_code = locale_code


class __LineItemType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    item = None
    sales_order_id = None
    uuid = None
    note = None
    line_status_code = None
    quantity = None
    line_extension_amount = None
    total_tax_amount = None
    minimum_quantity = None
    maximum_quantity = None
    minimum_backorder_quantity = None
    maximum_backorder_quantity = None
    inspection_method_code = None
    partial_delivery_indicator = None
    back_order_allowed_indicator = None
    accounting_cost_code = None
    accounting_cost = None
    warranty_information = None
    delivery = None
    delivery_terms = None
    originator_party = None
    ordered_shipment = None
    pricing_reference = None
    allowance_charge = None
    price = None
    sub_line_item = None
    warranty_validity_period = None
    warranty_party = None
    tax_total = None
    item_price_extension = None
    line_reference = None
    order_list = [
        'id_',
        'sales_order_id',
        'uuid',
        'note',
        'line_status_code',
        'quantity',
        'line_extension_amount',
        'total_tax_amount',
        'minimum_quantity',
        'maximum_quantity',
        'minimum_backorder_quantity',
        'maximum_backorder_quantity',
        'inspection_method_code',
        'partial_delivery_indicator',
        'back_order_allowed_indicator',
        'accounting_cost_code',
        'accounting_cost',
        'warranty_information',
        'delivery',
        'delivery_terms',
        'originator_party',
        'ordered_shipment',
        'pricing_reference',
        'allowance_charge',
        'price',
        'item',
        'sub_line_item',
        'warranty_validity_period',
        'warranty_party',
        'tax_total',
        'item_price_extension',
        'line_reference',
    ]

    def __init__(self,		id_: cbc.ID,
                 item: 'Item',
                 sales_order_id: cbc.SalesOrderID = None,
                 uuid: cbc.UUID = None,
                 note: List[cbc.Note] = None,
                 line_status_code: cbc.LineStatusCode = None,
                 quantity: cbc.Quantity = None,
                 line_extension_amount: cbc.LineExtensionAmount = None,
                 total_tax_amount: cbc.TotalTaxAmount = None,
                 minimum_quantity: cbc.MinimumQuantity = None,
                 maximum_quantity: cbc.MaximumQuantity = None,
                 minimum_backorder_quantity: cbc.MinimumBackorderQuantity = None,
                 maximum_backorder_quantity: cbc.MaximumBackorderQuantity = None,
                 inspection_method_code: cbc.InspectionMethodCode = None,
                 partial_delivery_indicator: cbc.PartialDeliveryIndicator = None,
                 back_order_allowed_indicator: cbc.BackOrderAllowedIndicator = None,
                 accounting_cost_code: cbc.AccountingCostCode = None,
                 accounting_cost: cbc.AccountingCost = None,
                 warranty_information: List[cbc.WarrantyInformation] = None,
                 delivery: List['Delivery'] = None,
                 delivery_terms: 'DeliveryTerms' = None,
                 originator_party: 'OriginatorParty' = None,
                 ordered_shipment: List['OrderedShipment'] = None,
                 pricing_reference: 'PricingReference' = None,
                 allowance_charge: List['AllowanceCharge'] = None,
                 price: 'Price' = None,
                 sub_line_item: List['SubLineItem'] = None,
                 warranty_validity_period: 'WarrantyValidityPeriod' = None,
                 warranty_party: 'WarrantyParty' = None,
                 tax_total: List['TaxTotal'] = None,
                 item_price_extension: 'ItemPriceExtension' = None,
                 line_reference: List['LineReference'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.item = item
        self.sales_order_id = sales_order_id
        self.uuid = uuid
        self.note = note
        self.line_status_code = line_status_code
        self.quantity = quantity
        self.line_extension_amount = line_extension_amount
        self.total_tax_amount = total_tax_amount
        self.minimum_quantity = minimum_quantity
        self.maximum_quantity = maximum_quantity
        self.minimum_backorder_quantity = minimum_backorder_quantity
        self.maximum_backorder_quantity = maximum_backorder_quantity
        self.inspection_method_code = inspection_method_code
        self.partial_delivery_indicator = partial_delivery_indicator
        self.back_order_allowed_indicator = back_order_allowed_indicator
        self.accounting_cost_code = accounting_cost_code
        self.accounting_cost = accounting_cost
        self.warranty_information = warranty_information
        self.delivery = delivery
        self.delivery_terms = delivery_terms
        self.originator_party = originator_party
        self.ordered_shipment = ordered_shipment
        self.pricing_reference = pricing_reference
        self.allowance_charge = allowance_charge
        self.price = price
        self.sub_line_item = sub_line_item
        self.warranty_validity_period = warranty_validity_period
        self.warranty_party = warranty_party
        self.tax_total = tax_total
        self.item_price_extension = item_price_extension
        self.line_reference = line_reference


class __LineReferenceType(PrefixCAC, ComplexXMLParseableObject):
    line_id = None
    uuid = None
    line_status_code = None
    document_reference = None
    order_list = [
        'line_id',
        'uuid',
        'line_status_code',
        'document_reference',
    ]

    def __init__(self,		line_id: cbc.LineID,
                 uuid: cbc.UUID = None,
                 line_status_code: cbc.LineStatusCode = None,
                 document_reference: 'DocumentReference' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.line_id = line_id
        self.uuid = uuid
        self.line_status_code = line_status_code
        self.document_reference = document_reference


class __LineResponseType(PrefixCAC, ComplexXMLParseableObject):
    line_reference = None
    response = None
    order_list = [
        'line_reference',
        'response',
    ]
    def __init__(self,		line_reference: 'LineReference',
                 response: List['Response'] = None, xml_namespaces=None):
        if not response:
            raise ListMustNotBeEmptyException('response')
        super().__init__(xml_namespaces)
        self.line_reference = line_reference
        self.response = response


class __LocationType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    description = None
    conditions = None
    country_subentity = None
    country_subentity_code = None
    location_type_code = None
    information_uri = None
    name = None
    validity_period = None
    address = None
    subsidiary_location = None
    location_coordinate = None
    order_list = [
        'id_',
        'description',
        'conditions',
        'country_subentity',
        'country_subentity_code',
        'location_type_code',
        'information_uri',
        'name',
        'validity_period',
        'address',
        'subsidiary_location',
        'location_coordinate',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 description: List[cbc.Description] = None,
                 conditions: List[cbc.Conditions] = None,
                 country_subentity: cbc.CountrySubentity = None,
                 country_subentity_code: cbc.CountrySubentityCode = None,
                 location_type_code: cbc.LocationTypeCode = None,
                 information_uri: cbc.InformationURI = None,
                 name: cbc.Name = None,
                 validity_period: List['ValidityPeriod'] = None,
                 address: 'Address' = None,
                 subsidiary_location: List['SubsidiaryLocation'] = None,
                 location_coordinate: List['LocationCoordinate'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.description = description
        self.conditions = conditions
        self.country_subentity = country_subentity
        self.country_subentity_code = country_subentity_code
        self.location_type_code = location_type_code
        self.information_uri = information_uri
        self.name = name
        self.validity_period = validity_period
        self.address = address
        self.subsidiary_location = subsidiary_location
        self.location_coordinate = location_coordinate


class __LocationCoordinateType(PrefixCAC, ComplexXMLParseableObject):
    coordinate_system_code = None
    latitude_degrees_measure = None
    latitude_minutes_measure = None
    latitude_direction_code = None
    longitude_degrees_measure = None
    longitude_minutes_measure = None
    longitude_direction_code = None
    altitude_measure = None
    order_list = [
        'coordinate_system_code',
        'latitude_degrees_measure',
        'latitude_minutes_measure',
        'latitude_direction_code',
        'longitude_degrees_measure',
        'longitude_minutes_measure',
        'longitude_direction_code',
        'altitude_measure',
    ]

    def __init__(self,		coordinate_system_code: cbc.CoordinateSystemCode = None,
                 latitude_degrees_measure: cbc.LatitudeDegreesMeasure = None,
                 latitude_minutes_measure: cbc.LatitudeMinutesMeasure = None,
                 latitude_direction_code: cbc.LatitudeDirectionCode = None,
                 longitude_degrees_measure: cbc.LongitudeDegreesMeasure = None,
                 longitude_minutes_measure: cbc.LongitudeMinutesMeasure = None,
                 longitude_direction_code: cbc.LongitudeDirectionCode = None,
                 altitude_measure: cbc.AltitudeMeasure = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.coordinate_system_code = coordinate_system_code
        self.latitude_degrees_measure = latitude_degrees_measure
        self.latitude_minutes_measure = latitude_minutes_measure
        self.latitude_direction_code = latitude_direction_code
        self.longitude_degrees_measure = longitude_degrees_measure
        self.longitude_minutes_measure = longitude_minutes_measure
        self.longitude_direction_code = longitude_direction_code
        self.altitude_measure = altitude_measure


class __LotIdentificationType(PrefixCAC, ComplexXMLParseableObject):
    lot_number_id = None
    expiry_date = None
    additional_item_property = None
    order_list = [
        'lot_number_id',
        'expiry_date',
        'additional_item_property',
    ]

    def __init__(self,		lot_number_id: cbc.LotNumberID = None,
                 expiry_date: cbc.ExpiryDate = None,
                 additional_item_property: List['AdditionalItemProperty'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.lot_number_id = lot_number_id
        self.expiry_date = expiry_date
        self.additional_item_property = additional_item_property


class __MaritimeTransportType(PrefixCAC, ComplexXMLParseableObject):
    vessel_id = None
    vessel_name = None
    radio_call_sign_id = None
    ships_requirements = None
    gross_tonnage_measure = None
    net_tonnage_measure = None
    registry_certificate_document_reference = None
    registry_port_location = None
    order_list = [
        'vessel_id',
        'vessel_name',
        'radio_call_sign_id',
        'ships_requirements',
        'gross_tonnage_measure',
        'net_tonnage_measure',
        'registry_certificate_document_reference',
        'registry_port_location',
    ]

    def __init__(self,		vessel_id: cbc.VesselID = None,
                 vessel_name: cbc.VesselName = None,
                 radio_call_sign_id: cbc.RadioCallSignID = None,
                 ships_requirements: List[cbc.ShipsRequirements] = None,
                 gross_tonnage_measure: cbc.GrossTonnageMeasure = None,
                 net_tonnage_measure: cbc.NetTonnageMeasure = None,
                 registry_certificate_document_reference: 'RegistryCertificateDocumentReference' = None,
                 registry_port_location: 'RegistryPortLocation' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.vessel_id = vessel_id
        self.vessel_name = vessel_name
        self.radio_call_sign_id = radio_call_sign_id
        self.ships_requirements = ships_requirements
        self.gross_tonnage_measure = gross_tonnage_measure
        self.net_tonnage_measure = net_tonnage_measure
        self.registry_certificate_document_reference = registry_certificate_document_reference
        self.registry_port_location = registry_port_location


class __MeterType(PrefixCAC, ComplexXMLParseableObject):
    meter_number = None
    meter_name = None
    meter_constant = None
    meter_constant_code = None
    total_delivered_quantity = None
    meter_reading = None
    meter_property = None
    order_list = [
        'meter_number',
        'meter_name',
        'meter_constant',
        'meter_constant_code',
        'total_delivered_quantity',
        'meter_reading',
        'meter_property',
    ]

    def __init__(self,		meter_number: cbc.MeterNumber = None,
                 meter_name: cbc.MeterName = None,
                 meter_constant: cbc.MeterConstant = None,
                 meter_constant_code: cbc.MeterConstantCode = None,
                 total_delivered_quantity: cbc.TotalDeliveredQuantity = None,
                 meter_reading: List['MeterReading'] = None,
                 meter_property: List['MeterProperty'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.meter_number = meter_number
        self.meter_name = meter_name
        self.meter_constant = meter_constant
        self.meter_constant_code = meter_constant_code
        self.total_delivered_quantity = total_delivered_quantity
        self.meter_reading = meter_reading
        self.meter_property = meter_property


class __MeterPropertyType(PrefixCAC, ComplexXMLParseableObject):
    name = None
    name_code = None
    value = None
    value_quantity = None
    value_qualifier = None
    order_list = [
        'name',
        'name_code',
        'value',
        'value_quantity',
        'value_qualifier',
    ]

    def __init__(self,		name: cbc.Name = None,
                 name_code: cbc.NameCode = None,
                 value: cbc.Value = None,
                 value_quantity: cbc.ValueQuantity = None,
                 value_qualifier: List[cbc.ValueQualifier] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.name = name
        self.name_code = name_code
        self.value = value
        self.value_quantity = value_quantity
        self.value_qualifier = value_qualifier


class __MeterReadingType(PrefixCAC, ComplexXMLParseableObject):
    previous_meter_reading_date = None
    previous_meter_quantity = None
    latest_meter_reading_date = None
    latest_meter_quantity = None
    delivered_quantity = None
    id_ = None
    meter_reading_type = None
    meter_reading_type_code = None
    previous_meter_reading_method = None
    previous_meter_reading_method_code = None
    latest_meter_reading_method = None
    latest_meter_reading_method_code = None
    meter_reading_comments = None
    order_list = [
        'id_',
        'meter_reading_type',
        'meter_reading_type_code',
        'previous_meter_reading_date',
        'previous_meter_quantity',
        'latest_meter_reading_date',
        'latest_meter_quantity',
        'previous_meter_reading_method',
        'previous_meter_reading_method_code',
        'latest_meter_reading_method',
        'latest_meter_reading_method_code',
        'meter_reading_comments',
        'delivered_quantity',
    ]

    def __init__(self,		previous_meter_reading_date: cbc.PreviousMeterReadingDate,
                 previous_meter_quantity: cbc.PreviousMeterQuantity,
                 latest_meter_reading_date: cbc.LatestMeterReadingDate,
                 latest_meter_quantity: cbc.LatestMeterQuantity,
                 delivered_quantity: cbc.DeliveredQuantity,
                 id_: cbc.ID = None,
                 meter_reading_type: cbc.MeterReadingType = None,
                 meter_reading_type_code: cbc.MeterReadingTypeCode = None,
                 previous_meter_reading_method: cbc.PreviousMeterReadingMethod = None,
                 previous_meter_reading_method_code: cbc.PreviousMeterReadingMethodCode = None,
                 latest_meter_reading_method: cbc.LatestMeterReadingMethod = None,
                 latest_meter_reading_method_code: cbc.LatestMeterReadingMethodCode = None,
                 meter_reading_comments: List[cbc.MeterReadingComments] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.previous_meter_reading_date = previous_meter_reading_date
        self.previous_meter_quantity = previous_meter_quantity
        self.latest_meter_reading_date = latest_meter_reading_date
        self.latest_meter_quantity = latest_meter_quantity
        self.delivered_quantity = delivered_quantity
        self.id_ = id_
        self.meter_reading_type = meter_reading_type
        self.meter_reading_type_code = meter_reading_type_code
        self.previous_meter_reading_method = previous_meter_reading_method
        self.previous_meter_reading_method_code = previous_meter_reading_method_code
        self.latest_meter_reading_method = latest_meter_reading_method
        self.latest_meter_reading_method_code = latest_meter_reading_method_code
        self.meter_reading_comments = meter_reading_comments


class __MiscellaneousEventType(PrefixCAC, ComplexXMLParseableObject):
    miscellaneous_event_type_code = None
    event_line_item = None
    order_list = [
        'miscellaneous_event_type_code',
        'event_line_item',
    ]
    def __init__(self,		miscellaneous_event_type_code: cbc.MiscellaneousEventTypeCode,
                 event_line_item: List['EventLineItem'] = None, xml_namespaces=None):
        if not event_line_item:
            raise ListMustNotBeEmptyException('event_line_item')
        super().__init__(xml_namespaces)
        self.miscellaneous_event_type_code = miscellaneous_event_type_code
        self.event_line_item = event_line_item


class __MonetaryTotalType(PrefixCAC, ComplexXMLParseableObject):
    payable_amount = None
    line_extension_amount = None
    tax_exclusive_amount = None
    tax_inclusive_amount = None
    allowance_total_amount = None
    charge_total_amount = None
    prepaid_amount = None
    payable_rounding_amount = None
    payable_alternative_amount = None
    order_list = [
        'line_extension_amount',
        'tax_exclusive_amount',
        'tax_inclusive_amount',
        'allowance_total_amount',
        'charge_total_amount',
        'prepaid_amount',
        'payable_rounding_amount',
        'payable_amount',
        'payable_alternative_amount',
    ]

    def __init__(self,		payable_amount: cbc.PayableAmount,
                 line_extension_amount: cbc.LineExtensionAmount = None,
                 tax_exclusive_amount: cbc.TaxExclusiveAmount = None,
                 tax_inclusive_amount: cbc.TaxInclusiveAmount = None,
                 allowance_total_amount: cbc.AllowanceTotalAmount = None,
                 charge_total_amount: cbc.ChargeTotalAmount = None,
                 prepaid_amount: cbc.PrepaidAmount = None,
                 payable_rounding_amount: cbc.PayableRoundingAmount = None,
                 payable_alternative_amount: cbc.PayableAlternativeAmount = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.payable_amount = payable_amount
        self.line_extension_amount = line_extension_amount
        self.tax_exclusive_amount = tax_exclusive_amount
        self.tax_inclusive_amount = tax_inclusive_amount
        self.allowance_total_amount = allowance_total_amount
        self.charge_total_amount = charge_total_amount
        self.prepaid_amount = prepaid_amount
        self.payable_rounding_amount = payable_rounding_amount
        self.payable_alternative_amount = payable_alternative_amount


class __NotificationRequirementType(PrefixCAC, ComplexXMLParseableObject):
    notification_type_code = None
    post_event_notification_duration_measure = None
    pre_event_notification_duration_measure = None
    notify_party = None
    notification_period = None
    notification_location = None
    order_list = [
        'notification_type_code',
        'post_event_notification_duration_measure',
        'pre_event_notification_duration_measure',
        'notify_party',
        'notification_period',
        'notification_location',
    ]

    def __init__(self,		notification_type_code: cbc.NotificationTypeCode,
                 post_event_notification_duration_measure: cbc.PostEventNotificationDurationMeasure = None,
                 pre_event_notification_duration_measure: cbc.PreEventNotificationDurationMeasure = None,
                 notify_party: List['NotifyParty'] = None,
                 notification_period: List['NotificationPeriod'] = None,
                 notification_location: List['NotificationLocation'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.notification_type_code = notification_type_code
        self.post_event_notification_duration_measure = post_event_notification_duration_measure
        self.pre_event_notification_duration_measure = pre_event_notification_duration_measure
        self.notify_party = notify_party
        self.notification_period = notification_period
        self.notification_location = notification_location


class __OnAccountPaymentType(PrefixCAC, ComplexXMLParseableObject):
    estimated_consumed_quantity = None
    note = None
    payment_terms = None
    order_list = [
        'estimated_consumed_quantity',
        'note',
        'payment_terms',
    ]

    def __init__(self,		estimated_consumed_quantity: cbc.EstimatedConsumedQuantity,
                 note: List[cbc.Note] = None,
                 payment_terms: List['PaymentTerms'] = None, xml_namespaces=None):
        if not payment_terms:
            raise ListMustNotBeEmptyException('payment_terms')
        super().__init__(xml_namespaces)
        self.estimated_consumed_quantity = estimated_consumed_quantity
        self.note = note
        self.payment_terms = payment_terms


class __OrderLineType(PrefixCAC, ComplexXMLParseableObject):
    line_item = None
    substitution_status_code = None
    note = None
    seller_proposed_substitute_line_item = None
    seller_substituted_line_item = None
    buyer_proposed_substitute_line_item = None
    catalogue_line_reference = None
    quotation_line_reference = None
    order_line_reference = None
    document_reference = None
    order_list = [
        'substitution_status_code',
        'note',
        'line_item',
        'seller_proposed_substitute_line_item',
        'seller_substituted_line_item',
        'buyer_proposed_substitute_line_item',
        'catalogue_line_reference',
        'quotation_line_reference',
        'order_line_reference',
        'document_reference',
    ]

    def __init__(self,		line_item: 'LineItem',
                 substitution_status_code: cbc.SubstitutionStatusCode = None,
                 note: List[cbc.Note] = None,
                 seller_proposed_substitute_line_item: List['SellerProposedSubstituteLineItem'] = None,
                 seller_substituted_line_item: List['SellerSubstitutedLineItem'] = None,
                 buyer_proposed_substitute_line_item: List['BuyerProposedSubstituteLineItem'] = None,
                 catalogue_line_reference: 'CatalogueLineReference' = None,
                 quotation_line_reference: 'QuotationLineReference' = None,
                 order_line_reference: List['OrderLineReference'] = None,
                 document_reference: List['DocumentReference'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.line_item = line_item
        self.substitution_status_code = substitution_status_code
        self.note = note
        self.seller_proposed_substitute_line_item = seller_proposed_substitute_line_item
        self.seller_substituted_line_item = seller_substituted_line_item
        self.buyer_proposed_substitute_line_item = buyer_proposed_substitute_line_item
        self.catalogue_line_reference = catalogue_line_reference
        self.quotation_line_reference = quotation_line_reference
        self.order_line_reference = order_line_reference
        self.document_reference = document_reference


class __OrderLineReferenceType(PrefixCAC, ComplexXMLParseableObject):
    line_id = None
    sales_order_line_id = None
    uuid = None
    line_status_code = None
    order_reference = None
    order_list = [
        'line_id',
        'sales_order_line_id',
        'uuid',
        'line_status_code',
        'order_reference',
    ]

    def __init__(self,		line_id: cbc.LineID,
                 sales_order_line_id: cbc.SalesOrderLineID = None,
                 uuid: cbc.UUID = None,
                 line_status_code: cbc.LineStatusCode = None,
                 order_reference: 'OrderReference' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.line_id = line_id
        self.sales_order_line_id = sales_order_line_id
        self.uuid = uuid
        self.line_status_code = line_status_code
        self.order_reference = order_reference


class __OrderReferenceType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    sales_order_id = None
    copy_indicator = None
    uuid = None
    issue_date = None
    issue_time = None
    customer_reference = None
    order_type_code = None
    document_reference = None
    order_list = [
        'id_',
        'sales_order_id',
        'copy_indicator',
        'uuid',
        'issue_date',
        'issue_time',
        'customer_reference',
        'order_type_code',
        'document_reference',
    ]

    def __init__(self,		id_: cbc.ID,
                 sales_order_id: cbc.SalesOrderID = None,
                 copy_indicator: cbc.CopyIndicator = None,
                 uuid: cbc.UUID = None,
                 issue_date: cbc.IssueDate = None,
                 issue_time: cbc.IssueTime = None,
                 customer_reference: cbc.CustomerReference = None,
                 order_type_code: cbc.OrderTypeCode = None,
                 document_reference: 'DocumentReference' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.sales_order_id = sales_order_id
        self.copy_indicator = copy_indicator
        self.uuid = uuid
        self.issue_date = issue_date
        self.issue_time = issue_time
        self.customer_reference = customer_reference
        self.order_type_code = order_type_code
        self.document_reference = document_reference


class __OrderedShipmentType(PrefixCAC, ComplexXMLParseableObject):
    shipment = None
    package = None
    order_list = [
        'shipment',
        'package',
    ]
    def __init__(self,		shipment: 'Shipment',
                 package: List['Package'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.shipment = shipment
        self.package = package


class __PackageType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    quantity = None
    returnable_material_indicator = None
    package_level_code = None
    packaging_type_code = None
    packing_material = None
    trace_id = None
    contained_package = None
    containing_transport_equipment = None
    goods_item = None
    measurement_dimension = None
    delivery_unit = None
    delivery = None
    pickup = None
    despatch = None
    order_list = [
        'id_',
        'quantity',
        'returnable_material_indicator',
        'package_level_code',
        'packaging_type_code',
        'packing_material',
        'trace_id',
        'contained_package',
        'containing_transport_equipment',
        'goods_item',
        'measurement_dimension',
        'delivery_unit',
        'delivery',
        'pickup',
        'despatch',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 quantity: cbc.Quantity = None,
                 returnable_material_indicator: cbc.ReturnableMaterialIndicator = None,
                 package_level_code: cbc.PackageLevelCode = None,
                 packaging_type_code: cbc.PackagingTypeCode = None,
                 packing_material: List[cbc.PackingMaterial] = None,
                 trace_id: cbc.TraceID = None,
                 contained_package: List['ContainedPackage'] = None,
                 containing_transport_equipment: 'ContainingTransportEquipment' = None,
                 goods_item: List['GoodsItem'] = None,
                 measurement_dimension: List['MeasurementDimension'] = None,
                 delivery_unit: List['DeliveryUnit'] = None,
                 delivery: 'Delivery' = None,
                 pickup: 'Pickup' = None,
                 despatch: 'Despatch' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.quantity = quantity
        self.returnable_material_indicator = returnable_material_indicator
        self.package_level_code = package_level_code
        self.packaging_type_code = packaging_type_code
        self.packing_material = packing_material
        self.trace_id = trace_id
        self.contained_package = contained_package
        self.containing_transport_equipment = containing_transport_equipment
        self.goods_item = goods_item
        self.measurement_dimension = measurement_dimension
        self.delivery_unit = delivery_unit
        self.delivery = delivery
        self.pickup = pickup
        self.despatch = despatch


class __PartyType(PrefixCAC, ComplexXMLParseableObject):
    mark_care_indicator = None
    mark_attention_indicator = None
    website_uri = None
    logo_reference_id = None
    endpoint_id = None
    industry_classification_code = None
    party_identification = None
    party_name = None
    language = None
    postal_address = None
    physical_location = None
    party_tax_scheme = None
    party_legal_entity = None
    contact = None
    person = None
    agent_party = None
    service_provider_party = None
    power_of_attorney = None
    financial_account = None
    order_list = [
        'mark_care_indicator',
        'mark_attention_indicator',
        'website_uri',
        'logo_reference_id',
        'endpoint_id',
        'industry_classification_code',
        'party_identification',
        'party_name',
        'language',
        'postal_address',
        'physical_location',
        'party_tax_scheme',
        'party_legal_entity',
        'contact',
        'person',
        'agent_party',
        'service_provider_party',
        'power_of_attorney',
        'financial_account',
    ]

    def __init__(self,		mark_care_indicator: cbc.MarkCareIndicator = None,
                 mark_attention_indicator: cbc.MarkAttentionIndicator = None,
                 website_uri: cbc.WebsiteURI = None,
                 logo_reference_id: cbc.LogoReferenceID = None,
                 endpoint_id: cbc.EndpointID = None,
                 industry_classification_code: cbc.IndustryClassificationCode = None,
                 party_identification: List['PartyIdentification'] = None,
                 party_name: List['PartyName'] = None,
                 language: 'Language' = None,
                 postal_address: 'PostalAddress' = None,
                 physical_location: 'PhysicalLocation' = None,
                 party_tax_scheme: List['PartyTaxScheme'] = None,
                 party_legal_entity: List['PartyLegalEntity'] = None,
                 contact: 'Contact' = None,
                 person: List['Person'] = None,
                 agent_party: 'AgentParty' = None,
                 service_provider_party: List['ServiceProviderParty'] = None,
                 power_of_attorney: List['PowerOfAttorney'] = None,
                 financial_account: 'FinancialAccount' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.mark_care_indicator = mark_care_indicator
        self.mark_attention_indicator = mark_attention_indicator
        self.website_uri = website_uri
        self.logo_reference_id = logo_reference_id
        self.endpoint_id = endpoint_id
        self.industry_classification_code = industry_classification_code
        self.party_identification = party_identification
        self.party_name = party_name
        self.language = language
        self.postal_address = postal_address
        self.physical_location = physical_location
        self.party_tax_scheme = party_tax_scheme
        self.party_legal_entity = party_legal_entity
        self.contact = contact
        self.person = person
        self.agent_party = agent_party
        self.service_provider_party = service_provider_party
        self.power_of_attorney = power_of_attorney
        self.financial_account = financial_account


class __PartyIdentificationType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    order_list = [
        'id_',
    ]

    def __init__(self,		id_: cbc.ID, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_


class __PartyLegalEntityType(PrefixCAC, ComplexXMLParseableObject):
    registration_name = None
    company_id = None
    registration_date = None
    registration_expiration_date = None
    company_legal_form_code = None
    company_legal_form = None
    sole_proprietorship_indicator = None
    company_liquidation_status_code = None
    corporate_stock_amount = None
    fully_paid_shares_indicator = None
    registration_address = None
    corporate_registration_scheme = None
    head_office_party = None
    shareholder_party = None
    order_list = [
        'registration_name',
        'company_id',
        'registration_date',
        'registration_expiration_date',
        'company_legal_form_code',
        'company_legal_form',
        'sole_proprietorship_indicator',
        'company_liquidation_status_code',
        'corporate_stock_amount',
        'fully_paid_shares_indicator',
        'registration_address',
        'corporate_registration_scheme',
        'head_office_party',
        'shareholder_party',
    ]

    def __init__(self,		registration_name: cbc.RegistrationName = None,
                 company_id: cbc.CompanyID = None,
                 registration_date: cbc.RegistrationDate = None,
                 registration_expiration_date: cbc.RegistrationExpirationDate = None,
                 company_legal_form_code: cbc.CompanyLegalFormCode = None,
                 company_legal_form: cbc.CompanyLegalForm = None,
                 sole_proprietorship_indicator: cbc.SoleProprietorshipIndicator = None,
                 company_liquidation_status_code: cbc.CompanyLiquidationStatusCode = None,
                 corporate_stock_amount: cbc.CorporateStockAmount = None,
                 fully_paid_shares_indicator: cbc.FullyPaidSharesIndicator = None,
                 registration_address: 'RegistrationAddress' = None,
                 corporate_registration_scheme: 'CorporateRegistrationScheme' = None,
                 head_office_party: 'HeadOfficeParty' = None,
                 shareholder_party: List['ShareholderParty'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.registration_name = registration_name
        self.company_id = company_id
        self.registration_date = registration_date
        self.registration_expiration_date = registration_expiration_date
        self.company_legal_form_code = company_legal_form_code
        self.company_legal_form = company_legal_form
        self.sole_proprietorship_indicator = sole_proprietorship_indicator
        self.company_liquidation_status_code = company_liquidation_status_code
        self.corporate_stock_amount = corporate_stock_amount
        self.fully_paid_shares_indicator = fully_paid_shares_indicator
        self.registration_address = registration_address
        self.corporate_registration_scheme = corporate_registration_scheme
        self.head_office_party = head_office_party
        self.shareholder_party = shareholder_party


class __PartyNameType(PrefixCAC, ComplexXMLParseableObject):
    name = None
    order_list = [
        'name',
    ]

    def __init__(self,		name: cbc.Name, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.name = name


class __PartyTaxSchemeType(PrefixCAC, ComplexXMLParseableObject):
    tax_scheme = None
    registration_name = None
    company_id = None
    tax_level_code = None
    exemption_reason_code = None
    exemption_reason = None
    registration_address = None
    order_list = [
        'registration_name',
        'company_id',
        'tax_level_code',
        'exemption_reason_code',
        'exemption_reason',
        'registration_address',
        'tax_scheme',
    ]

    def __init__(self,		tax_scheme: 'TaxScheme',
                 registration_name: cbc.RegistrationName = None,
                 company_id: cbc.CompanyID = None,
                 tax_level_code: cbc.TaxLevelCode = None,
                 exemption_reason_code: cbc.ExemptionReasonCode = None,
                 exemption_reason: List[cbc.ExemptionReason] = None,
                 registration_address: 'RegistrationAddress' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.tax_scheme = tax_scheme
        self.registration_name = registration_name
        self.company_id = company_id
        self.tax_level_code = tax_level_code
        self.exemption_reason_code = exemption_reason_code
        self.exemption_reason = exemption_reason
        self.registration_address = registration_address


class __PaymentType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    paid_amount = None
    received_date = None
    paid_date = None
    paid_time = None
    instruction_id = None
    order_list = [
        'id_',
        'paid_amount',
        'received_date',
        'paid_date',
        'paid_time',
        'instruction_id',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 paid_amount: cbc.PaidAmount = None,
                 received_date: cbc.ReceivedDate = None,
                 paid_date: cbc.PaidDate = None,
                 paid_time: cbc.PaidTime = None,
                 instruction_id: cbc.InstructionID = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.paid_amount = paid_amount
        self.received_date = received_date
        self.paid_date = paid_date
        self.paid_time = paid_time
        self.instruction_id = instruction_id


class __PaymentMandateType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    mandate_type_code = None
    maximum_payment_instructions_numeric = None
    maximum_paid_amount = None
    signature_id = None
    payer_party = None
    payer_financial_account = None
    validity_period = None
    payment_reversal_period = None
    clause = None
    order_list = [
        'id_',
        'mandate_type_code',
        'maximum_payment_instructions_numeric',
        'maximum_paid_amount',
        'signature_id',
        'payer_party',
        'payer_financial_account',
        'validity_period',
        'payment_reversal_period',
        'clause',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 mandate_type_code: cbc.MandateTypeCode = None,
                 maximum_payment_instructions_numeric: cbc.MaximumPaymentInstructionsNumeric = None,
                 maximum_paid_amount: cbc.MaximumPaidAmount = None,
                 signature_id: cbc.SignatureID = None,
                 payer_party: 'PayerParty' = None,
                 payer_financial_account: 'PayerFinancialAccount' = None,
                 validity_period: 'ValidityPeriod' = None,
                 payment_reversal_period: 'PaymentReversalPeriod' = None,
                 clause: List['Clause'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.mandate_type_code = mandate_type_code
        self.maximum_payment_instructions_numeric = maximum_payment_instructions_numeric
        self.maximum_paid_amount = maximum_paid_amount
        self.signature_id = signature_id
        self.payer_party = payer_party
        self.payer_financial_account = payer_financial_account
        self.validity_period = validity_period
        self.payment_reversal_period = payment_reversal_period
        self.clause = clause


class __PaymentMeansType(PrefixCAC, ComplexXMLParseableObject):
    payment_means_code = None
    id_ = None
    payment_due_date = None
    payment_channel_code = None
    instruction_id = None
    instruction_note = None
    payment_id = None
    card_account = None
    payer_financial_account = None
    payee_financial_account = None
    credit_account = None
    payment_mandate = None
    trade_financing = None
    order_list = [
        'id_',
        'payment_means_code',
        'payment_due_date',
        'payment_channel_code',
        'instruction_id',
        'instruction_note',
        'payment_id',
        'card_account',
        'payer_financial_account',
        'payee_financial_account',
        'credit_account',
        'payment_mandate',
        'trade_financing',
    ]

    def __init__(self,		payment_means_code: cbc.PaymentMeansCode,
                 id_: cbc.ID = None,
                 payment_due_date: cbc.PaymentDueDate = None,
                 payment_channel_code: cbc.PaymentChannelCode = None,
                 instruction_id: cbc.InstructionID = None,
                 instruction_note: List[cbc.InstructionNote] = None,
                 payment_id: List[cbc.PaymentID] = None,
                 card_account: 'CardAccount' = None,
                 payer_financial_account: 'PayerFinancialAccount' = None,
                 payee_financial_account: 'PayeeFinancialAccount' = None,
                 credit_account: 'CreditAccount' = None,
                 payment_mandate: 'PaymentMandate' = None,
                 trade_financing: 'TradeFinancing' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.payment_means_code = payment_means_code
        self.id_ = id_
        self.payment_due_date = payment_due_date
        self.payment_channel_code = payment_channel_code
        self.instruction_id = instruction_id
        self.instruction_note = instruction_note
        self.payment_id = payment_id
        self.card_account = card_account
        self.payer_financial_account = payer_financial_account
        self.payee_financial_account = payee_financial_account
        self.credit_account = credit_account
        self.payment_mandate = payment_mandate
        self.trade_financing = trade_financing


class __PaymentTermsType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    payment_means_id = None
    prepaid_payment_reference_id = None
    note = None
    reference_event_code = None
    settlement_discount_percent = None
    penalty_surcharge_percent = None
    payment_percent = None
    amount = None
    settlement_discount_amount = None
    penalty_amount = None
    payment_terms_details_uri = None
    payment_due_date = None
    installment_due_date = None
    invoicing_party_reference = None
    settlement_period = None
    penalty_period = None
    exchange_rate = None
    validity_period = None
    order_list = [
        'id_',
        'payment_means_id',
        'prepaid_payment_reference_id',
        'note',
        'reference_event_code',
        'settlement_discount_percent',
        'penalty_surcharge_percent',
        'payment_percent',
        'amount',
        'settlement_discount_amount',
        'penalty_amount',
        'payment_terms_details_uri',
        'payment_due_date',
        'installment_due_date',
        'invoicing_party_reference',
        'settlement_period',
        'penalty_period',
        'exchange_rate',
        'validity_period',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 payment_means_id: List[cbc.PaymentMeansID] = None,
                 prepaid_payment_reference_id: cbc.PrepaidPaymentReferenceID = None,
                 note: List[cbc.Note] = None,
                 reference_event_code: cbc.ReferenceEventCode = None,
                 settlement_discount_percent: cbc.SettlementDiscountPercent = None,
                 penalty_surcharge_percent: cbc.PenaltySurchargePercent = None,
                 payment_percent: cbc.PaymentPercent = None,
                 amount: cbc.Amount = None,
                 settlement_discount_amount: cbc.SettlementDiscountAmount = None,
                 penalty_amount: cbc.PenaltyAmount = None,
                 payment_terms_details_uri: cbc.PaymentTermsDetailsURI = None,
                 payment_due_date: cbc.PaymentDueDate = None,
                 installment_due_date: cbc.InstallmentDueDate = None,
                 invoicing_party_reference: cbc.InvoicingPartyReference = None,
                 settlement_period: 'SettlementPeriod' = None,
                 penalty_period: 'PenaltyPeriod' = None,
                 exchange_rate: 'ExchangeRate' = None,
                 validity_period: 'ValidityPeriod' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.payment_means_id = payment_means_id
        self.prepaid_payment_reference_id = prepaid_payment_reference_id
        self.note = note
        self.reference_event_code = reference_event_code
        self.settlement_discount_percent = settlement_discount_percent
        self.penalty_surcharge_percent = penalty_surcharge_percent
        self.payment_percent = payment_percent
        self.amount = amount
        self.settlement_discount_amount = settlement_discount_amount
        self.penalty_amount = penalty_amount
        self.payment_terms_details_uri = payment_terms_details_uri
        self.payment_due_date = payment_due_date
        self.installment_due_date = installment_due_date
        self.invoicing_party_reference = invoicing_party_reference
        self.settlement_period = settlement_period
        self.penalty_period = penalty_period
        self.exchange_rate = exchange_rate
        self.validity_period = validity_period


class __PerformanceDataLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    performance_value_quantity = None
    performance_metric_type_code = None
    note = None
    period = None
    item = None
    order_list = [
        'id_',
        'note',
        'performance_value_quantity',
        'performance_metric_type_code',
        'period',
        'item',
    ]

    def __init__(self,		id_: cbc.ID,
                 performance_value_quantity: cbc.PerformanceValueQuantity,
                 performance_metric_type_code: cbc.PerformanceMetricTypeCode,
                 note: List[cbc.Note] = None,
                 period: 'Period' = None,
                 item: 'Item' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.performance_value_quantity = performance_value_quantity
        self.performance_metric_type_code = performance_metric_type_code
        self.note = note
        self.period = period
        self.item = item


class __PeriodType(PrefixCAC, ComplexXMLParseableObject):
    start_date = None
    start_time = None
    end_date = None
    end_time = None
    duration_measure = None
    description_code = None
    description = None
    order_list = [
        'start_date',
        'start_time',
        'end_date',
        'end_time',
        'duration_measure',
        'description_code',
        'description',
    ]

    def __init__(self,		start_date: cbc.StartDate = None,
                 start_time: cbc.StartTime = None,
                 end_date: cbc.EndDate = None,
                 end_time: cbc.EndTime = None,
                 duration_measure: cbc.DurationMeasure = None,
                 description_code: List[cbc.DescriptionCode] = None,
                 description: List[cbc.Description] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.duration_measure = duration_measure
        self.description_code = description_code
        self.description = description


class __PersonType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    first_name = None
    family_name = None
    title = None
    middle_name = None
    other_name = None
    name_suffix = None
    job_title = None
    nationality_id = None
    gender_code = None
    birth_date = None
    birthplace_name = None
    organization_department = None
    contact = None
    financial_account = None
    identity_document_reference = None
    residence_address = None
    order_list = [
        'id_',
        'first_name',
        'family_name',
        'title',
        'middle_name',
        'other_name',
        'name_suffix',
        'job_title',
        'nationality_id',
        'gender_code',
        'birth_date',
        'birthplace_name',
        'organization_department',
        'contact',
        'financial_account',
        'identity_document_reference',
        'residence_address',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 first_name: cbc.FirstName = None,
                 family_name: cbc.FamilyName = None,
                 title: cbc.Title = None,
                 middle_name: cbc.MiddleName = None,
                 other_name: cbc.OtherName = None,
                 name_suffix: cbc.NameSuffix = None,
                 job_title: cbc.JobTitle = None,
                 nationality_id: cbc.NationalityID = None,
                 gender_code: cbc.GenderCode = None,
                 birth_date: cbc.BirthDate = None,
                 birthplace_name: cbc.BirthplaceName = None,
                 organization_department: cbc.OrganizationDepartment = None,
                 contact: 'Contact' = None,
                 financial_account: 'FinancialAccount' = None,
                 identity_document_reference: List['IdentityDocumentReference'] = None,
                 residence_address: 'ResidenceAddress' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.first_name = first_name
        self.family_name = family_name
        self.title = title
        self.middle_name = middle_name
        self.other_name = other_name
        self.name_suffix = name_suffix
        self.job_title = job_title
        self.nationality_id = nationality_id
        self.gender_code = gender_code
        self.birth_date = birth_date
        self.birthplace_name = birthplace_name
        self.organization_department = organization_department
        self.contact = contact
        self.financial_account = financial_account
        self.identity_document_reference = identity_document_reference
        self.residence_address = residence_address


class __PhysicalAttributeType(PrefixCAC, ComplexXMLParseableObject):
    attribute_id = None
    position_code = None
    description_code = None
    description = None
    order_list = [
        'attribute_id',
        'position_code',
        'description_code',
        'description',
    ]

    def __init__(self,		attribute_id: cbc.AttributeID,
                 position_code: cbc.PositionCode = None,
                 description_code: cbc.DescriptionCode = None,
                 description: List[cbc.Description] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.attribute_id = attribute_id
        self.position_code = position_code
        self.description_code = description_code
        self.description = description


class __PickupType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    actual_pickup_date = None
    actual_pickup_time = None
    earliest_pickup_date = None
    earliest_pickup_time = None
    latest_pickup_date = None
    latest_pickup_time = None
    pickup_location = None
    pickup_party = None
    order_list = [
        'id_',
        'actual_pickup_date',
        'actual_pickup_time',
        'earliest_pickup_date',
        'earliest_pickup_time',
        'latest_pickup_date',
        'latest_pickup_time',
        'pickup_location',
        'pickup_party',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 actual_pickup_date: cbc.ActualPickupDate = None,
                 actual_pickup_time: cbc.ActualPickupTime = None,
                 earliest_pickup_date: cbc.EarliestPickupDate = None,
                 earliest_pickup_time: cbc.EarliestPickupTime = None,
                 latest_pickup_date: cbc.LatestPickupDate = None,
                 latest_pickup_time: cbc.LatestPickupTime = None,
                 pickup_location: 'PickupLocation' = None,
                 pickup_party: 'PickupParty' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.actual_pickup_date = actual_pickup_date
        self.actual_pickup_time = actual_pickup_time
        self.earliest_pickup_date = earliest_pickup_date
        self.earliest_pickup_time = earliest_pickup_time
        self.latest_pickup_date = latest_pickup_date
        self.latest_pickup_time = latest_pickup_time
        self.pickup_location = pickup_location
        self.pickup_party = pickup_party


class __PowerOfAttorneyType(PrefixCAC, ComplexXMLParseableObject):
    agent_party = None
    id_ = None
    issue_date = None
    issue_time = None
    description = None
    notary_party = None
    witness_party = None
    mandate_document_reference = None
    order_list = [
        'id_',
        'issue_date',
        'issue_time',
        'description',
        'notary_party',
        'agent_party',
        'witness_party',
        'mandate_document_reference',
    ]

    def __init__(self,		agent_party: 'AgentParty',
                 id_: cbc.ID = None,
                 issue_date: cbc.IssueDate = None,
                 issue_time: cbc.IssueTime = None,
                 description: List[cbc.Description] = None,
                 notary_party: 'NotaryParty' = None,
                 witness_party: List['WitnessParty'] = None,
                 mandate_document_reference: List['MandateDocumentReference'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.agent_party = agent_party
        self.id_ = id_
        self.issue_date = issue_date
        self.issue_time = issue_time
        self.description = description
        self.notary_party = notary_party
        self.witness_party = witness_party
        self.mandate_document_reference = mandate_document_reference


class __PriceType(PrefixCAC, ComplexXMLParseableObject):
    price_amount = None
    base_quantity = None
    price_change_reason = None
    price_type_code = None
    price_type = None
    orderable_unit_factor_rate = None
    validity_period = None
    price_list = None
    allowance_charge = None
    pricing_exchange_rate = None
    order_list = [
        'price_amount',
        'base_quantity',
        'price_change_reason',
        'price_type_code',
        'price_type',
        'orderable_unit_factor_rate',
        'validity_period',
        'price_list',
        'allowance_charge',
        'pricing_exchange_rate',
    ]

    def __init__(self,		price_amount: cbc.PriceAmount,
                 base_quantity: cbc.BaseQuantity = None,
                 price_change_reason: List[cbc.PriceChangeReason] = None,
                 price_type_code: cbc.PriceTypeCode = None,
                 price_type: cbc.PriceType = None,
                 orderable_unit_factor_rate: cbc.OrderableUnitFactorRate = None,
                 validity_period: List['ValidityPeriod'] = None,
                 price_list: 'PriceList' = None,
                 allowance_charge: List['AllowanceCharge'] = None,
                 pricing_exchange_rate: 'PricingExchangeRate' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.price_amount = price_amount
        self.base_quantity = base_quantity
        self.price_change_reason = price_change_reason
        self.price_type_code = price_type_code
        self.price_type = price_type
        self.orderable_unit_factor_rate = orderable_unit_factor_rate
        self.validity_period = validity_period
        self.price_list = price_list
        self.allowance_charge = allowance_charge
        self.pricing_exchange_rate = pricing_exchange_rate


class __PriceExtensionType(PrefixCAC, ComplexXMLParseableObject):
    amount = None
    tax_total = None
    order_list = [
        'amount',
        'tax_total',
    ]
    def __init__(self,		amount: cbc.Amount,
                 tax_total: List['TaxTotal'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.amount = amount
        self.tax_total = tax_total


class __PriceListType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    status_code = None
    validity_period = None
    previous_price_list = None
    order_list = [
        'id_',
        'status_code',
        'validity_period',
        'previous_price_list',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 status_code: cbc.StatusCode = None,
                 validity_period: List['ValidityPeriod'] = None,
                 previous_price_list: 'PreviousPriceList' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.status_code = status_code
        self.validity_period = validity_period
        self.previous_price_list = previous_price_list


class __PricingReferenceType(PrefixCAC, ComplexXMLParseableObject):
    original_item_location_quantity = None
    alternative_condition_price = None
    order_list = [
        'original_item_location_quantity',
        'alternative_condition_price',
    ]
    def __init__(self,		original_item_location_quantity: 'OriginalItemLocationQuantity' = None,
                 alternative_condition_price: List['AlternativeConditionPrice'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.original_item_location_quantity = original_item_location_quantity
        self.alternative_condition_price = alternative_condition_price


class __ProcessJustificationType(PrefixCAC, ComplexXMLParseableObject):
    previous_cancellation_reason_code = None
    process_reason_code = None
    process_reason = None
    description = None
    order_list = [
        'previous_cancellation_reason_code',
        'process_reason_code',
        'process_reason',
        'description',
    ]

    def __init__(self,		previous_cancellation_reason_code: cbc.PreviousCancellationReasonCode = None,
                 process_reason_code: cbc.ProcessReasonCode = None,
                 process_reason: List[cbc.ProcessReason] = None,
                 description: List[cbc.Description] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.previous_cancellation_reason_code = previous_cancellation_reason_code
        self.process_reason_code = process_reason_code
        self.process_reason = process_reason
        self.description = description


class __ProcurementProjectType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    name = None
    description = None
    procurement_type_code = None
    procurement_sub_type_code = None
    quality_control_code = None
    required_fee_amount = None
    fee_description = None
    requested_delivery_date = None
    estimated_overall_contract_quantity = None
    note = None
    requested_tender_total = None
    main_commodity_classification = None
    additional_commodity_classification = None
    realized_location = None
    planned_period = None
    contract_extension = None
    request_for_tender_line = None
    order_list = [
        'id_',
        'name',
        'description',
        'procurement_type_code',
        'procurement_sub_type_code',
        'quality_control_code',
        'required_fee_amount',
        'fee_description',
        'requested_delivery_date',
        'estimated_overall_contract_quantity',
        'note',
        'requested_tender_total',
        'main_commodity_classification',
        'additional_commodity_classification',
        'realized_location',
        'planned_period',
        'contract_extension',
        'request_for_tender_line',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 name: List[cbc.Name] = None,
                 description: List[cbc.Description] = None,
                 procurement_type_code: cbc.ProcurementTypeCode = None,
                 procurement_sub_type_code: cbc.ProcurementSubTypeCode = None,
                 quality_control_code: cbc.QualityControlCode = None,
                 required_fee_amount: cbc.RequiredFeeAmount = None,
                 fee_description: List[cbc.FeeDescription] = None,
                 requested_delivery_date: cbc.RequestedDeliveryDate = None,
                 estimated_overall_contract_quantity: cbc.EstimatedOverallContractQuantity = None,
                 note: List[cbc.Note] = None,
                 requested_tender_total: 'RequestedTenderTotal' = None,
                 main_commodity_classification: 'MainCommodityClassification' = None,
                 additional_commodity_classification: List['AdditionalCommodityClassification'] = None,
                 realized_location: List['RealizedLocation'] = None,
                 planned_period: 'PlannedPeriod' = None,
                 contract_extension: 'ContractExtension' = None,
                 request_for_tender_line: List['RequestForTenderLine'] = None, xml_namespaces=None):
        if not name:
            raise ListMustNotBeEmptyException('name')
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.name = name
        self.description = description
        self.procurement_type_code = procurement_type_code
        self.procurement_sub_type_code = procurement_sub_type_code
        self.quality_control_code = quality_control_code
        self.required_fee_amount = required_fee_amount
        self.fee_description = fee_description
        self.requested_delivery_date = requested_delivery_date
        self.estimated_overall_contract_quantity = estimated_overall_contract_quantity
        self.note = note
        self.requested_tender_total = requested_tender_total
        self.main_commodity_classification = main_commodity_classification
        self.additional_commodity_classification = additional_commodity_classification
        self.realized_location = realized_location
        self.planned_period = planned_period
        self.contract_extension = contract_extension
        self.request_for_tender_line = request_for_tender_line


class __ProcurementProjectLotType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    tendering_terms = None
    procurement_project = None
    order_list = [
        'id_',
        'tendering_terms',
        'procurement_project',
    ]

    def __init__(self,		id_: cbc.ID,
                 tendering_terms: 'TenderingTerms' = None,
                 procurement_project: 'ProcurementProject' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.tendering_terms = tendering_terms
        self.procurement_project = procurement_project


class __ProjectReferenceType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    uuid = None
    issue_date = None
    work_phase_reference = None
    order_list = [
        'id_',
        'uuid',
        'issue_date',
        'work_phase_reference',
    ]

    def __init__(self,		id_: cbc.ID,
                 uuid: cbc.UUID = None,
                 issue_date: cbc.IssueDate = None,
                 work_phase_reference: List['WorkPhaseReference'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.uuid = uuid
        self.issue_date = issue_date
        self.work_phase_reference = work_phase_reference


class __PromotionalEventType(PrefixCAC, ComplexXMLParseableObject):
    promotional_event_type_code = None
    submission_date = None
    first_shipment_availibility_date = None
    latest_proposal_acceptance_date = None
    promotional_specification = None
    order_list = [
        'promotional_event_type_code',
        'submission_date',
        'first_shipment_availibility_date',
        'latest_proposal_acceptance_date',
        'promotional_specification',
    ]

    def __init__(self,		promotional_event_type_code: cbc.PromotionalEventTypeCode,
                 submission_date: cbc.SubmissionDate = None,
                 first_shipment_availibility_date: cbc.FirstShipmentAvailibilityDate = None,
                 latest_proposal_acceptance_date: cbc.LatestProposalAcceptanceDate = None,
                 promotional_specification: List['PromotionalSpecification'] = None, xml_namespaces=None):
        if not promotional_specification:
            raise ListMustNotBeEmptyException('promotional_specification')
        super().__init__(xml_namespaces)
        self.promotional_event_type_code = promotional_event_type_code
        self.submission_date = submission_date
        self.first_shipment_availibility_date = first_shipment_availibility_date
        self.latest_proposal_acceptance_date = latest_proposal_acceptance_date
        self.promotional_specification = promotional_specification


class __PromotionalEventLineItemType(PrefixCAC, ComplexXMLParseableObject):
    amount = None
    event_line_item = None
    order_list = [
        'amount',
        'event_line_item',
    ]
    def __init__(self,		amount: cbc.Amount,
                 event_line_item: 'EventLineItem', xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.amount = amount
        self.event_line_item = event_line_item


class __PromotionalSpecificationType(PrefixCAC, ComplexXMLParseableObject):
    specification_id = None
    promotional_event_line_item = None
    event_tactic = None
    order_list = [
        'specification_id',
        'promotional_event_line_item',
        'event_tactic',
    ]

    def __init__(self,		specification_id: cbc.SpecificationID = None,
                 promotional_event_line_item: List['PromotionalEventLineItem'] = None,
                 event_tactic: List['EventTactic'] = None, xml_namespaces=None):
        if not promotional_event_line_item:
            raise ListMustNotBeEmptyException('promotional_event_line_item')
        super().__init__(xml_namespaces)
        self.specification_id = specification_id
        self.promotional_event_line_item = promotional_event_line_item
        self.event_tactic = event_tactic


class __QualificationResolutionType(PrefixCAC, ComplexXMLParseableObject):
    admission_code = None
    resolution_date = None
    exclusion_reason = None
    resolution = None
    resolution_time = None
    procurement_project_lot = None
    order_list = [
        'admission_code',
        'exclusion_reason',
        'resolution',
        'resolution_date',
        'resolution_time',
        'procurement_project_lot',
    ]

    def __init__(self,		admission_code: cbc.AdmissionCode,
                 resolution_date: cbc.ResolutionDate,
                 exclusion_reason: List[cbc.ExclusionReason] = None,
                 resolution: List[cbc.Resolution] = None,
                 resolution_time: cbc.ResolutionTime = None,
                 procurement_project_lot: 'ProcurementProjectLot' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.admission_code = admission_code
        self.resolution_date = resolution_date
        self.exclusion_reason = exclusion_reason
        self.resolution = resolution
        self.resolution_time = resolution_time
        self.procurement_project_lot = procurement_project_lot


class __QualifyingPartyType(PrefixCAC, ComplexXMLParseableObject):
    participation_percent = None
    personal_situation = None
    operating_years_quantity = None
    employee_quantity = None
    business_classification_evidence_id = None
    business_identity_evidence_id = None
    tenderer_role_code = None
    business_classification_scheme = None
    technical_capability = None
    financial_capability = None
    completed_task = None
    declaration = None
    party = None
    economic_operator_role = None
    order_list = [
        'participation_percent',
        'personal_situation',
        'operating_years_quantity',
        'employee_quantity',
        'business_classification_evidence_id',
        'business_identity_evidence_id',
        'tenderer_role_code',
        'business_classification_scheme',
        'technical_capability',
        'financial_capability',
        'completed_task',
        'declaration',
        'party',
        'economic_operator_role',
    ]

    def __init__(self,		participation_percent: cbc.ParticipationPercent = None,
                 personal_situation: List[cbc.PersonalSituation] = None,
                 operating_years_quantity: cbc.OperatingYearsQuantity = None,
                 employee_quantity: cbc.EmployeeQuantity = None,
                 business_classification_evidence_id: cbc.BusinessClassificationEvidenceID = None,
                 business_identity_evidence_id: cbc.BusinessIdentityEvidenceID = None,
                 tenderer_role_code: cbc.TendererRoleCode = None,
                 business_classification_scheme: 'BusinessClassificationScheme' = None,
                 technical_capability: List['TechnicalCapability'] = None,
                 financial_capability: List['FinancialCapability'] = None,
                 completed_task: List['CompletedTask'] = None,
                 declaration: List['Declaration'] = None,
                 party: 'Party' = None,
                 economic_operator_role: 'EconomicOperatorRole' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.participation_percent = participation_percent
        self.personal_situation = personal_situation
        self.operating_years_quantity = operating_years_quantity
        self.employee_quantity = employee_quantity
        self.business_classification_evidence_id = business_classification_evidence_id
        self.business_identity_evidence_id = business_identity_evidence_id
        self.tenderer_role_code = tenderer_role_code
        self.business_classification_scheme = business_classification_scheme
        self.technical_capability = technical_capability
        self.financial_capability = financial_capability
        self.completed_task = completed_task
        self.declaration = declaration
        self.party = party
        self.economic_operator_role = economic_operator_role


class __QuotationLineType(PrefixCAC, ComplexXMLParseableObject):
    line_item = None
    id_ = None
    note = None
    quantity = None
    line_extension_amount = None
    total_tax_amount = None
    request_for_quotation_line_id = None
    document_reference = None
    seller_proposed_substitute_line_item = None
    alternative_line_item = None
    request_line_reference = None
    order_list = [
        'id_',
        'note',
        'quantity',
        'line_extension_amount',
        'total_tax_amount',
        'request_for_quotation_line_id',
        'document_reference',
        'line_item',
        'seller_proposed_substitute_line_item',
        'alternative_line_item',
        'request_line_reference',
    ]

    def __init__(self,		line_item: 'LineItem',
                 id_: cbc.ID = None,
                 note: List[cbc.Note] = None,
                 quantity: cbc.Quantity = None,
                 line_extension_amount: cbc.LineExtensionAmount = None,
                 total_tax_amount: cbc.TotalTaxAmount = None,
                 request_for_quotation_line_id: cbc.RequestForQuotationLineID = None,
                 document_reference: List['DocumentReference'] = None,
                 seller_proposed_substitute_line_item: List['SellerProposedSubstituteLineItem'] = None,
                 alternative_line_item: List['AlternativeLineItem'] = None,
                 request_line_reference: 'RequestLineReference' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.line_item = line_item
        self.id_ = id_
        self.note = note
        self.quantity = quantity
        self.line_extension_amount = line_extension_amount
        self.total_tax_amount = total_tax_amount
        self.request_for_quotation_line_id = request_for_quotation_line_id
        self.document_reference = document_reference
        self.seller_proposed_substitute_line_item = seller_proposed_substitute_line_item
        self.alternative_line_item = alternative_line_item
        self.request_line_reference = request_line_reference


class __RailTransportType(PrefixCAC, ComplexXMLParseableObject):
    train_id = None
    rail_car_id = None
    order_list = [
        'train_id',
        'rail_car_id',
    ]
    def __init__(self,		train_id: cbc.TrainID,
                 rail_car_id: cbc.RailCarID = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.train_id = train_id
        self.rail_car_id = rail_car_id


class __ReceiptLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    uuid = None
    note = None
    received_quantity = None
    short_quantity = None
    shortage_action_code = None
    rejected_quantity = None
    reject_reason_code = None
    reject_reason = None
    reject_action_code = None
    quantity_discrepancy_code = None
    oversupply_quantity = None
    received_date = None
    timing_complaint_code = None
    timing_complaint = None
    order_line_reference = None
    despatch_line_reference = None
    document_reference = None
    item = None
    shipment = None
    order_list = [
        'id_',
        'uuid',
        'note',
        'received_quantity',
        'short_quantity',
        'shortage_action_code',
        'rejected_quantity',
        'reject_reason_code',
        'reject_reason',
        'reject_action_code',
        'quantity_discrepancy_code',
        'oversupply_quantity',
        'received_date',
        'timing_complaint_code',
        'timing_complaint',
        'order_line_reference',
        'despatch_line_reference',
        'document_reference',
        'item',
        'shipment',
    ]

    def __init__(self,		id_: cbc.ID,
                 uuid: cbc.UUID = None,
                 note: List[cbc.Note] = None,
                 received_quantity: cbc.ReceivedQuantity = None,
                 short_quantity: cbc.ShortQuantity = None,
                 shortage_action_code: cbc.ShortageActionCode = None,
                 rejected_quantity: cbc.RejectedQuantity = None,
                 reject_reason_code: cbc.RejectReasonCode = None,
                 reject_reason: List[cbc.RejectReason] = None,
                 reject_action_code: cbc.RejectActionCode = None,
                 quantity_discrepancy_code: cbc.QuantityDiscrepancyCode = None,
                 oversupply_quantity: cbc.OversupplyQuantity = None,
                 received_date: cbc.ReceivedDate = None,
                 timing_complaint_code: cbc.TimingComplaintCode = None,
                 timing_complaint: cbc.TimingComplaint = None,
                 order_line_reference: 'OrderLineReference' = None,
                 despatch_line_reference: List['DespatchLineReference'] = None,
                 document_reference: List['DocumentReference'] = None,
                 item: List['Item'] = None,
                 shipment: List['Shipment'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.uuid = uuid
        self.note = note
        self.received_quantity = received_quantity
        self.short_quantity = short_quantity
        self.shortage_action_code = shortage_action_code
        self.rejected_quantity = rejected_quantity
        self.reject_reason_code = reject_reason_code
        self.reject_reason = reject_reason
        self.reject_action_code = reject_action_code
        self.quantity_discrepancy_code = quantity_discrepancy_code
        self.oversupply_quantity = oversupply_quantity
        self.received_date = received_date
        self.timing_complaint_code = timing_complaint_code
        self.timing_complaint = timing_complaint
        self.order_line_reference = order_line_reference
        self.despatch_line_reference = despatch_line_reference
        self.document_reference = document_reference
        self.item = item
        self.shipment = shipment


class __RegulationType(PrefixCAC, ComplexXMLParseableObject):
    name = None
    legal_reference = None
    ontology_uri = None
    order_list = [
        'name',
        'legal_reference',
        'ontology_uri',
    ]

    def __init__(self,		name: cbc.Name,
                 legal_reference: cbc.LegalReference = None,
                 ontology_uri: cbc.OntologyURI = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.name = name
        self.legal_reference = legal_reference
        self.ontology_uri = ontology_uri


class __RelatedItemType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    quantity = None
    description = None
    order_list = [
        'id_',
        'quantity',
        'description',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 quantity: cbc.Quantity = None,
                 description: List[cbc.Description] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.quantity = quantity
        self.description = description


class __ReminderLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    note = None
    uuid = None
    balance_brought_forward_indicator = None
    debit_line_amount = None
    credit_line_amount = None
    accounting_cost_code = None
    accounting_cost = None
    penalty_surcharge_percent = None
    amount = None
    payment_purpose_code = None
    reminder_period = None
    billing_reference = None
    exchange_rate = None
    order_list = [
        'id_',
        'note',
        'uuid',
        'balance_brought_forward_indicator',
        'debit_line_amount',
        'credit_line_amount',
        'accounting_cost_code',
        'accounting_cost',
        'penalty_surcharge_percent',
        'amount',
        'payment_purpose_code',
        'reminder_period',
        'billing_reference',
        'exchange_rate',
    ]

    def __init__(self,		id_: cbc.ID,
                 note: List[cbc.Note] = None,
                 uuid: cbc.UUID = None,
                 balance_brought_forward_indicator: cbc.BalanceBroughtForwardIndicator = None,
                 debit_line_amount: cbc.DebitLineAmount = None,
                 credit_line_amount: cbc.CreditLineAmount = None,
                 accounting_cost_code: cbc.AccountingCostCode = None,
                 accounting_cost: cbc.AccountingCost = None,
                 penalty_surcharge_percent: cbc.PenaltySurchargePercent = None,
                 amount: cbc.Amount = None,
                 payment_purpose_code: cbc.PaymentPurposeCode = None,
                 reminder_period: List['ReminderPeriod'] = None,
                 billing_reference: List['BillingReference'] = None,
                 exchange_rate: 'ExchangeRate' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.note = note
        self.uuid = uuid
        self.balance_brought_forward_indicator = balance_brought_forward_indicator
        self.debit_line_amount = debit_line_amount
        self.credit_line_amount = credit_line_amount
        self.accounting_cost_code = accounting_cost_code
        self.accounting_cost = accounting_cost
        self.penalty_surcharge_percent = penalty_surcharge_percent
        self.amount = amount
        self.payment_purpose_code = payment_purpose_code
        self.reminder_period = reminder_period
        self.billing_reference = billing_reference
        self.exchange_rate = exchange_rate


class __RemittanceAdviceLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    note = None
    uuid = None
    debit_line_amount = None
    credit_line_amount = None
    balance_amount = None
    payment_purpose_code = None
    invoicing_party_reference = None
    accounting_supplier_party = None
    accounting_customer_party = None
    buyer_customer_party = None
    seller_supplier_party = None
    originator_customer_party = None
    payee_party = None
    invoice_period = None
    billing_reference = None
    document_reference = None
    exchange_rate = None
    order_list = [
        'id_',
        'note',
        'uuid',
        'debit_line_amount',
        'credit_line_amount',
        'balance_amount',
        'payment_purpose_code',
        'invoicing_party_reference',
        'accounting_supplier_party',
        'accounting_customer_party',
        'buyer_customer_party',
        'seller_supplier_party',
        'originator_customer_party',
        'payee_party',
        'invoice_period',
        'billing_reference',
        'document_reference',
        'exchange_rate',
    ]

    def __init__(self,		id_: cbc.ID,
                 note: List[cbc.Note] = None,
                 uuid: cbc.UUID = None,
                 debit_line_amount: cbc.DebitLineAmount = None,
                 credit_line_amount: cbc.CreditLineAmount = None,
                 balance_amount: cbc.BalanceAmount = None,
                 payment_purpose_code: cbc.PaymentPurposeCode = None,
                 invoicing_party_reference: cbc.InvoicingPartyReference = None,
                 accounting_supplier_party: 'AccountingSupplierParty' = None,
                 accounting_customer_party: 'AccountingCustomerParty' = None,
                 buyer_customer_party: 'BuyerCustomerParty' = None,
                 seller_supplier_party: 'SellerSupplierParty' = None,
                 originator_customer_party: 'OriginatorCustomerParty' = None,
                 payee_party: 'PayeeParty' = None,
                 invoice_period: List['InvoicePeriod'] = None,
                 billing_reference: List['BillingReference'] = None,
                 document_reference: List['DocumentReference'] = None,
                 exchange_rate: 'ExchangeRate' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.note = note
        self.uuid = uuid
        self.debit_line_amount = debit_line_amount
        self.credit_line_amount = credit_line_amount
        self.balance_amount = balance_amount
        self.payment_purpose_code = payment_purpose_code
        self.invoicing_party_reference = invoicing_party_reference
        self.accounting_supplier_party = accounting_supplier_party
        self.accounting_customer_party = accounting_customer_party
        self.buyer_customer_party = buyer_customer_party
        self.seller_supplier_party = seller_supplier_party
        self.originator_customer_party = originator_customer_party
        self.payee_party = payee_party
        self.invoice_period = invoice_period
        self.billing_reference = billing_reference
        self.document_reference = document_reference
        self.exchange_rate = exchange_rate


class __RenewalType(PrefixCAC, ComplexXMLParseableObject):
    amount = None
    period = None
    order_list = [
        'amount',
        'period',
    ]
    def __init__(self,		amount: cbc.Amount = None,
                 period: 'Period' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.amount = amount
        self.period = period


class __RequestForQuotationLineType(PrefixCAC, ComplexXMLParseableObject):
    line_item = None
    id_ = None
    uuid = None
    note = None
    optional_line_item_indicator = None
    privacy_code = None
    security_classification_code = None
    document_reference = None
    order_list = [
        'id_',
        'uuid',
        'note',
        'optional_line_item_indicator',
        'privacy_code',
        'security_classification_code',
        'document_reference',
        'line_item',
    ]

    def __init__(self,		line_item: 'LineItem',
                 id_: cbc.ID = None,
                 uuid: cbc.UUID = None,
                 note: List[cbc.Note] = None,
                 optional_line_item_indicator: cbc.OptionalLineItemIndicator = None,
                 privacy_code: cbc.PrivacyCode = None,
                 security_classification_code: cbc.SecurityClassificationCode = None,
                 document_reference: List['DocumentReference'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.line_item = line_item
        self.id_ = id_
        self.uuid = uuid
        self.note = note
        self.optional_line_item_indicator = optional_line_item_indicator
        self.privacy_code = privacy_code
        self.security_classification_code = security_classification_code
        self.document_reference = document_reference


class __RequestForTenderLineType(PrefixCAC, ComplexXMLParseableObject):
    item = None
    id_ = None
    uuid = None
    note = None
    quantity = None
    minimum_quantity = None
    maximum_quantity = None
    tax_included_indicator = None
    minimum_amount = None
    maximum_amount = None
    estimated_amount = None
    document_reference = None
    delivery_period = None
    required_item_location_quantity = None
    warranty_validity_period = None
    sub_request_for_tender_line = None
    order_list = [
        'id_',
        'uuid',
        'note',
        'quantity',
        'minimum_quantity',
        'maximum_quantity',
        'tax_included_indicator',
        'minimum_amount',
        'maximum_amount',
        'estimated_amount',
        'document_reference',
        'delivery_period',
        'required_item_location_quantity',
        'warranty_validity_period',
        'item',
        'sub_request_for_tender_line',
    ]

    def __init__(self,		item: 'Item',
                 id_: cbc.ID = None,
                 uuid: cbc.UUID = None,
                 note: List[cbc.Note] = None,
                 quantity: cbc.Quantity = None,
                 minimum_quantity: cbc.MinimumQuantity = None,
                 maximum_quantity: cbc.MaximumQuantity = None,
                 tax_included_indicator: cbc.TaxIncludedIndicator = None,
                 minimum_amount: cbc.MinimumAmount = None,
                 maximum_amount: cbc.MaximumAmount = None,
                 estimated_amount: cbc.EstimatedAmount = None,
                 document_reference: List['DocumentReference'] = None,
                 delivery_period: List['DeliveryPeriod'] = None,
                 required_item_location_quantity: List['RequiredItemLocationQuantity'] = None,
                 warranty_validity_period: 'WarrantyValidityPeriod' = None,
                 sub_request_for_tender_line: List['SubRequestForTenderLine'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.item = item
        self.id_ = id_
        self.uuid = uuid
        self.note = note
        self.quantity = quantity
        self.minimum_quantity = minimum_quantity
        self.maximum_quantity = maximum_quantity
        self.tax_included_indicator = tax_included_indicator
        self.minimum_amount = minimum_amount
        self.maximum_amount = maximum_amount
        self.estimated_amount = estimated_amount
        self.document_reference = document_reference
        self.delivery_period = delivery_period
        self.required_item_location_quantity = required_item_location_quantity
        self.warranty_validity_period = warranty_validity_period
        self.sub_request_for_tender_line = sub_request_for_tender_line


class __RequestedTenderTotalType(PrefixCAC, ComplexXMLParseableObject):
    estimated_overall_contract_amount = None
    total_amount = None
    tax_included_indicator = None
    minimum_amount = None
    maximum_amount = None
    monetary_scope = None
    average_subsequent_contract_amount = None
    applicable_tax_category = None
    order_list = [
        'estimated_overall_contract_amount',
        'total_amount',
        'tax_included_indicator',
        'minimum_amount',
        'maximum_amount',
        'monetary_scope',
        'average_subsequent_contract_amount',
        'applicable_tax_category',
    ]

    def __init__(self,		estimated_overall_contract_amount: cbc.EstimatedOverallContractAmount = None,
                 total_amount: cbc.TotalAmount = None,
                 tax_included_indicator: cbc.TaxIncludedIndicator = None,
                 minimum_amount: cbc.MinimumAmount = None,
                 maximum_amount: cbc.MaximumAmount = None,
                 monetary_scope: List[cbc.MonetaryScope] = None,
                 average_subsequent_contract_amount: cbc.AverageSubsequentContractAmount = None,
                 applicable_tax_category: List['ApplicableTaxCategory'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.estimated_overall_contract_amount = estimated_overall_contract_amount
        self.total_amount = total_amount
        self.tax_included_indicator = tax_included_indicator
        self.minimum_amount = minimum_amount
        self.maximum_amount = maximum_amount
        self.monetary_scope = monetary_scope
        self.average_subsequent_contract_amount = average_subsequent_contract_amount
        self.applicable_tax_category = applicable_tax_category


class __ResponseType(PrefixCAC, ComplexXMLParseableObject):
    reference_id = None
    response_code = None
    description = None
    effective_date = None
    effective_time = None
    status = None
    order_list = [
        'reference_id',
        'response_code',
        'description',
        'effective_date',
        'effective_time',
        'status',
    ]

    def __init__(self,		reference_id: cbc.ReferenceID = None,
                 response_code: cbc.ResponseCode = None,
                 description: List[cbc.Description] = None,
                 effective_date: cbc.EffectiveDate = None,
                 effective_time: cbc.EffectiveTime = None,
                 status: List['Status'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.reference_id = reference_id
        self.response_code = response_code
        self.description = description
        self.effective_date = effective_date
        self.effective_time = effective_time
        self.status = status


class __ResultOfVerificationType(PrefixCAC, ComplexXMLParseableObject):
    validator_id = None
    validation_result_code = None
    validation_date = None
    validation_time = None
    validate_process = None
    validate_tool = None
    validate_tool_version = None
    signatory_party = None
    order_list = [
        'validator_id',
        'validation_result_code',
        'validation_date',
        'validation_time',
        'validate_process',
        'validate_tool',
        'validate_tool_version',
        'signatory_party',
    ]

    def __init__(self,		validator_id: cbc.ValidatorID = None,
                 validation_result_code: cbc.ValidationResultCode = None,
                 validation_date: cbc.ValidationDate = None,
                 validation_time: cbc.ValidationTime = None,
                 validate_process: cbc.ValidateProcess = None,
                 validate_tool: cbc.ValidateTool = None,
                 validate_tool_version: cbc.ValidateToolVersion = None,
                 signatory_party: 'SignatoryParty' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.validator_id = validator_id
        self.validation_result_code = validation_result_code
        self.validation_date = validation_date
        self.validation_time = validation_time
        self.validate_process = validate_process
        self.validate_tool = validate_tool
        self.validate_tool_version = validate_tool_version
        self.signatory_party = signatory_party


class __RetailPlannedImpactType(PrefixCAC, ComplexXMLParseableObject):
    amount = None
    forecast_purpose_code = None
    forecast_type_code = None
    period = None
    order_list = [
        'amount',
        'forecast_purpose_code',
        'forecast_type_code',
        'period',
    ]

    def __init__(self,		amount: cbc.Amount,
                 forecast_purpose_code: cbc.ForecastPurposeCode,
                 forecast_type_code: cbc.ForecastTypeCode,
                 period: 'Period' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.amount = amount
        self.forecast_purpose_code = forecast_purpose_code
        self.forecast_type_code = forecast_type_code
        self.period = period


class __RoadTransportType(PrefixCAC, ComplexXMLParseableObject):
    license_plate_id = None
    order_list = [
        'license_plate_id',
    ]

    def __init__(self,		license_plate_id: cbc.LicensePlateID, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.license_plate_id = license_plate_id


class __SalesItemType(PrefixCAC, ComplexXMLParseableObject):
    quantity = None
    item = None
    activity_property = None
    tax_exclusive_price = None
    tax_inclusive_price = None
    order_list = [
        'quantity',
        'activity_property',
        'tax_exclusive_price',
        'tax_inclusive_price',
        'item',
    ]

    def __init__(self,		quantity: cbc.Quantity,
                 item: 'Item',
                 activity_property: List['ActivityProperty'] = None,
                 tax_exclusive_price: List['TaxExclusivePrice'] = None,
                 tax_inclusive_price: List['TaxInclusivePrice'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.quantity = quantity
        self.item = item
        self.activity_property = activity_property
        self.tax_exclusive_price = tax_exclusive_price
        self.tax_inclusive_price = tax_inclusive_price


class __SecondaryHazardType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    placard_notation = None
    placard_endorsement = None
    emergency_procedures_code = None
    extension = None
    order_list = [
        'id_',
        'placard_notation',
        'placard_endorsement',
        'emergency_procedures_code',
        'extension',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 placard_notation: cbc.PlacardNotation = None,
                 placard_endorsement: cbc.PlacardEndorsement = None,
                 emergency_procedures_code: cbc.EmergencyProceduresCode = None,
                 extension: List[cbc.Extension] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.placard_notation = placard_notation
        self.placard_endorsement = placard_endorsement
        self.emergency_procedures_code = emergency_procedures_code
        self.extension = extension


class __ServiceFrequencyType(PrefixCAC, ComplexXMLParseableObject):
    week_day_code = None
    order_list = [
        'week_day_code',
    ]

    def __init__(self,		week_day_code: cbc.WeekDayCode, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.week_day_code = week_day_code


class __ServiceProviderPartyType(PrefixCAC, ComplexXMLParseableObject):
    party = None
    id_ = None
    service_type_code = None
    service_type = None
    seller_contact = None
    order_list = [
        'id_',
        'service_type_code',
        'service_type',
        'party',
        'seller_contact',
    ]

    def __init__(self,		party: 'Party',
                 id_: cbc.ID = None,
                 service_type_code: cbc.ServiceTypeCode = None,
                 service_type: List[cbc.ServiceType] = None,
                 seller_contact: 'SellerContact' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.party = party
        self.id_ = id_
        self.service_type_code = service_type_code
        self.service_type = service_type
        self.seller_contact = seller_contact


class __ShareholderPartyType(PrefixCAC, ComplexXMLParseableObject):
    partecipation_percent = None
    party = None
    order_list = [
        'partecipation_percent',
        'party',
    ]
    def __init__(self,		partecipation_percent: cbc.PartecipationPercent = None,
                 party: 'Party' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.partecipation_percent = partecipation_percent
        self.party = party


class __ShipmentType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    shipping_priority_level_code = None
    handling_code = None
    handling_instructions = None
    information = None
    gross_weight_measure = None
    net_weight_measure = None
    net_net_weight_measure = None
    gross_volume_measure = None
    net_volume_measure = None
    total_goods_item_quantity = None
    total_transport_handling_unit_quantity = None
    insurance_value_amount = None
    declared_customs_value_amount = None
    declared_for_carriage_value_amount = None
    declared_statistics_value_amount = None
    free_on_board_value_amount = None
    special_instructions = None
    delivery_instructions = None
    split_consignment_indicator = None
    consignment_quantity = None
    consignment = None
    goods_item = None
    shipment_stage = None
    delivery = None
    transport_handling_unit = None
    return_address = None
    origin_address = None
    first_arrival_port_location = None
    last_exit_port_location = None
    export_country = None
    freight_allowance_charge = None
    order_list = [
        'id_',
        'shipping_priority_level_code',
        'handling_code',
        'handling_instructions',
        'information',
        'gross_weight_measure',
        'net_weight_measure',
        'net_net_weight_measure',
        'gross_volume_measure',
        'net_volume_measure',
        'total_goods_item_quantity',
        'total_transport_handling_unit_quantity',
        'insurance_value_amount',
        'declared_customs_value_amount',
        'declared_for_carriage_value_amount',
        'declared_statistics_value_amount',
        'free_on_board_value_amount',
        'special_instructions',
        'delivery_instructions',
        'split_consignment_indicator',
        'consignment_quantity',
        'consignment',
        'goods_item',
        'shipment_stage',
        'delivery',
        'transport_handling_unit',
        'return_address',
        'origin_address',
        'first_arrival_port_location',
        'last_exit_port_location',
        'export_country',
        'freight_allowance_charge',
    ]

    def __init__(self,		id_: cbc.ID,
                 shipping_priority_level_code: cbc.ShippingPriorityLevelCode = None,
                 handling_code: cbc.HandlingCode = None,
                 handling_instructions: List[cbc.HandlingInstructions] = None,
                 information: List[cbc.Information] = None,
                 gross_weight_measure: cbc.GrossWeightMeasure = None,
                 net_weight_measure: cbc.NetWeightMeasure = None,
                 net_net_weight_measure: cbc.NetNetWeightMeasure = None,
                 gross_volume_measure: cbc.GrossVolumeMeasure = None,
                 net_volume_measure: cbc.NetVolumeMeasure = None,
                 total_goods_item_quantity: cbc.TotalGoodsItemQuantity = None,
                 total_transport_handling_unit_quantity: cbc.TotalTransportHandlingUnitQuantity = None,
                 insurance_value_amount: cbc.InsuranceValueAmount = None,
                 declared_customs_value_amount: cbc.DeclaredCustomsValueAmount = None,
                 declared_for_carriage_value_amount: cbc.DeclaredForCarriageValueAmount = None,
                 declared_statistics_value_amount: cbc.DeclaredStatisticsValueAmount = None,
                 free_on_board_value_amount: cbc.FreeOnBoardValueAmount = None,
                 special_instructions: List[cbc.SpecialInstructions] = None,
                 delivery_instructions: List[cbc.DeliveryInstructions] = None,
                 split_consignment_indicator: cbc.SplitConsignmentIndicator = None,
                 consignment_quantity: cbc.ConsignmentQuantity = None,
                 consignment: List['Consignment'] = None,
                 goods_item: List['GoodsItem'] = None,
                 shipment_stage: List['ShipmentStage'] = None,
                 delivery: 'Delivery' = None,
                 transport_handling_unit: List['TransportHandlingUnit'] = None,
                 return_address: 'ReturnAddress' = None,
                 origin_address: 'OriginAddress' = None,
                 first_arrival_port_location: 'FirstArrivalPortLocation' = None,
                 last_exit_port_location: 'LastExitPortLocation' = None,
                 export_country: 'ExportCountry' = None,
                 freight_allowance_charge: List['FreightAllowanceCharge'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.shipping_priority_level_code = shipping_priority_level_code
        self.handling_code = handling_code
        self.handling_instructions = handling_instructions
        self.information = information
        self.gross_weight_measure = gross_weight_measure
        self.net_weight_measure = net_weight_measure
        self.net_net_weight_measure = net_net_weight_measure
        self.gross_volume_measure = gross_volume_measure
        self.net_volume_measure = net_volume_measure
        self.total_goods_item_quantity = total_goods_item_quantity
        self.total_transport_handling_unit_quantity = total_transport_handling_unit_quantity
        self.insurance_value_amount = insurance_value_amount
        self.declared_customs_value_amount = declared_customs_value_amount
        self.declared_for_carriage_value_amount = declared_for_carriage_value_amount
        self.declared_statistics_value_amount = declared_statistics_value_amount
        self.free_on_board_value_amount = free_on_board_value_amount
        self.special_instructions = special_instructions
        self.delivery_instructions = delivery_instructions
        self.split_consignment_indicator = split_consignment_indicator
        self.consignment_quantity = consignment_quantity
        self.consignment = consignment
        self.goods_item = goods_item
        self.shipment_stage = shipment_stage
        self.delivery = delivery
        self.transport_handling_unit = transport_handling_unit
        self.return_address = return_address
        self.origin_address = origin_address
        self.first_arrival_port_location = first_arrival_port_location
        self.last_exit_port_location = last_exit_port_location
        self.export_country = export_country
        self.freight_allowance_charge = freight_allowance_charge


class __ShipmentStageType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    transport_mode_code = None
    transport_means_type_code = None
    transit_direction_code = None
    pre_carriage_indicator = None
    on_carriage_indicator = None
    estimated_delivery_date = None
    estimated_delivery_time = None
    required_delivery_date = None
    required_delivery_time = None
    loading_sequence_id = None
    successive_sequence_id = None
    instructions = None
    demurrage_instructions = None
    crew_quantity = None
    passenger_quantity = None
    transit_period = None
    carrier_party = None
    transport_means = None
    loading_port_location = None
    unloading_port_location = None
    transship_port_location = None
    loading_transport_event = None
    examination_transport_event = None
    availability_transport_event = None
    exportation_transport_event = None
    discharge_transport_event = None
    warehousing_transport_event = None
    takeover_transport_event = None
    optional_takeover_transport_event = None
    dropoff_transport_event = None
    actual_pickup_transport_event = None
    delivery_transport_event = None
    receipt_transport_event = None
    storage_transport_event = None
    acceptance_transport_event = None
    terminal_operator_party = None
    customs_agent_party = None
    estimated_transit_period = None
    freight_allowance_charge = None
    freight_charge_location = None
    detention_transport_event = None
    requested_departure_transport_event = None
    requested_arrival_transport_event = None
    requested_waypoint_transport_event = None
    planned_departure_transport_event = None
    planned_arrival_transport_event = None
    planned_waypoint_transport_event = None
    actual_departure_transport_event = None
    actual_waypoint_transport_event = None
    actual_arrival_transport_event = None
    transport_event = None
    estimated_departure_transport_event = None
    estimated_arrival_transport_event = None
    passenger_person = None
    driver_person = None
    reporting_person = None
    crew_member_person = None
    security_officer_person = None
    master_person = None
    ships_surgeon_person = None
    order_list = [
        'id_',
        'transport_mode_code',
        'transport_means_type_code',
        'transit_direction_code',
        'pre_carriage_indicator',
        'on_carriage_indicator',
        'estimated_delivery_date',
        'estimated_delivery_time',
        'required_delivery_date',
        'required_delivery_time',
        'loading_sequence_id',
        'successive_sequence_id',
        'instructions',
        'demurrage_instructions',
        'crew_quantity',
        'passenger_quantity',
        'transit_period',
        'carrier_party',
        'transport_means',
        'loading_port_location',
        'unloading_port_location',
        'transship_port_location',
        'loading_transport_event',
        'examination_transport_event',
        'availability_transport_event',
        'exportation_transport_event',
        'discharge_transport_event',
        'warehousing_transport_event',
        'takeover_transport_event',
        'optional_takeover_transport_event',
        'dropoff_transport_event',
        'actual_pickup_transport_event',
        'delivery_transport_event',
        'receipt_transport_event',
        'storage_transport_event',
        'acceptance_transport_event',
        'terminal_operator_party',
        'customs_agent_party',
        'estimated_transit_period',
        'freight_allowance_charge',
        'freight_charge_location',
        'detention_transport_event',
        'requested_departure_transport_event',
        'requested_arrival_transport_event',
        'requested_waypoint_transport_event',
        'planned_departure_transport_event',
        'planned_arrival_transport_event',
        'planned_waypoint_transport_event',
        'actual_departure_transport_event',
        'actual_waypoint_transport_event',
        'actual_arrival_transport_event',
        'transport_event',
        'estimated_departure_transport_event',
        'estimated_arrival_transport_event',
        'passenger_person',
        'driver_person',
        'reporting_person',
        'crew_member_person',
        'security_officer_person',
        'master_person',
        'ships_surgeon_person',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 transport_mode_code: cbc.TransportModeCode = None,
                 transport_means_type_code: cbc.TransportMeansTypeCode = None,
                 transit_direction_code: cbc.TransitDirectionCode = None,
                 pre_carriage_indicator: cbc.PreCarriageIndicator = None,
                 on_carriage_indicator: cbc.OnCarriageIndicator = None,
                 estimated_delivery_date: cbc.EstimatedDeliveryDate = None,
                 estimated_delivery_time: cbc.EstimatedDeliveryTime = None,
                 required_delivery_date: cbc.RequiredDeliveryDate = None,
                 required_delivery_time: cbc.RequiredDeliveryTime = None,
                 loading_sequence_id: cbc.LoadingSequenceID = None,
                 successive_sequence_id: cbc.SuccessiveSequenceID = None,
                 instructions: List[cbc.Instructions] = None,
                 demurrage_instructions: List[cbc.DemurrageInstructions] = None,
                 crew_quantity: cbc.CrewQuantity = None,
                 passenger_quantity: cbc.PassengerQuantity = None,
                 transit_period: 'TransitPeriod' = None,
                 carrier_party: List['CarrierParty'] = None,
                 transport_means: 'TransportMeans' = None,
                 loading_port_location: 'LoadingPortLocation' = None,
                 unloading_port_location: 'UnloadingPortLocation' = None,
                 transship_port_location: 'TransshipPortLocation' = None,
                 loading_transport_event: 'LoadingTransportEvent' = None,
                 examination_transport_event: 'ExaminationTransportEvent' = None,
                 availability_transport_event: 'AvailabilityTransportEvent' = None,
                 exportation_transport_event: 'ExportationTransportEvent' = None,
                 discharge_transport_event: 'DischargeTransportEvent' = None,
                 warehousing_transport_event: 'WarehousingTransportEvent' = None,
                 takeover_transport_event: 'TakeoverTransportEvent' = None,
                 optional_takeover_transport_event: 'OptionalTakeoverTransportEvent' = None,
                 dropoff_transport_event: 'DropoffTransportEvent' = None,
                 actual_pickup_transport_event: 'ActualPickupTransportEvent' = None,
                 delivery_transport_event: 'DeliveryTransportEvent' = None,
                 receipt_transport_event: 'ReceiptTransportEvent' = None,
                 storage_transport_event: 'StorageTransportEvent' = None,
                 acceptance_transport_event: 'AcceptanceTransportEvent' = None,
                 terminal_operator_party: 'TerminalOperatorParty' = None,
                 customs_agent_party: 'CustomsAgentParty' = None,
                 estimated_transit_period: 'EstimatedTransitPeriod' = None,
                 freight_allowance_charge: List['FreightAllowanceCharge'] = None,
                 freight_charge_location: 'FreightChargeLocation' = None,
                 detention_transport_event: List['DetentionTransportEvent'] = None,
                 requested_departure_transport_event: 'RequestedDepartureTransportEvent' = None,
                 requested_arrival_transport_event: 'RequestedArrivalTransportEvent' = None,
                 requested_waypoint_transport_event: List['RequestedWaypointTransportEvent'] = None,
                 planned_departure_transport_event: 'PlannedDepartureTransportEvent' = None,
                 planned_arrival_transport_event: 'PlannedArrivalTransportEvent' = None,
                 planned_waypoint_transport_event: List['PlannedWaypointTransportEvent'] = None,
                 actual_departure_transport_event: 'ActualDepartureTransportEvent' = None,
                 actual_waypoint_transport_event: 'ActualWaypointTransportEvent' = None,
                 actual_arrival_transport_event: 'ActualArrivalTransportEvent' = None,
                 transport_event: List['TransportEvent'] = None,
                 estimated_departure_transport_event: 'EstimatedDepartureTransportEvent' = None,
                 estimated_arrival_transport_event: 'EstimatedArrivalTransportEvent' = None,
                 passenger_person: List['PassengerPerson'] = None,
                 driver_person: List['DriverPerson'] = None,
                 reporting_person: 'ReportingPerson' = None,
                 crew_member_person: List['CrewMemberPerson'] = None,
                 security_officer_person: 'SecurityOfficerPerson' = None,
                 master_person: 'MasterPerson' = None,
                 ships_surgeon_person: 'ShipsSurgeonPerson' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.transport_mode_code = transport_mode_code
        self.transport_means_type_code = transport_means_type_code
        self.transit_direction_code = transit_direction_code
        self.pre_carriage_indicator = pre_carriage_indicator
        self.on_carriage_indicator = on_carriage_indicator
        self.estimated_delivery_date = estimated_delivery_date
        self.estimated_delivery_time = estimated_delivery_time
        self.required_delivery_date = required_delivery_date
        self.required_delivery_time = required_delivery_time
        self.loading_sequence_id = loading_sequence_id
        self.successive_sequence_id = successive_sequence_id
        self.instructions = instructions
        self.demurrage_instructions = demurrage_instructions
        self.crew_quantity = crew_quantity
        self.passenger_quantity = passenger_quantity
        self.transit_period = transit_period
        self.carrier_party = carrier_party
        self.transport_means = transport_means
        self.loading_port_location = loading_port_location
        self.unloading_port_location = unloading_port_location
        self.transship_port_location = transship_port_location
        self.loading_transport_event = loading_transport_event
        self.examination_transport_event = examination_transport_event
        self.availability_transport_event = availability_transport_event
        self.exportation_transport_event = exportation_transport_event
        self.discharge_transport_event = discharge_transport_event
        self.warehousing_transport_event = warehousing_transport_event
        self.takeover_transport_event = takeover_transport_event
        self.optional_takeover_transport_event = optional_takeover_transport_event
        self.dropoff_transport_event = dropoff_transport_event
        self.actual_pickup_transport_event = actual_pickup_transport_event
        self.delivery_transport_event = delivery_transport_event
        self.receipt_transport_event = receipt_transport_event
        self.storage_transport_event = storage_transport_event
        self.acceptance_transport_event = acceptance_transport_event
        self.terminal_operator_party = terminal_operator_party
        self.customs_agent_party = customs_agent_party
        self.estimated_transit_period = estimated_transit_period
        self.freight_allowance_charge = freight_allowance_charge
        self.freight_charge_location = freight_charge_location
        self.detention_transport_event = detention_transport_event
        self.requested_departure_transport_event = requested_departure_transport_event
        self.requested_arrival_transport_event = requested_arrival_transport_event
        self.requested_waypoint_transport_event = requested_waypoint_transport_event
        self.planned_departure_transport_event = planned_departure_transport_event
        self.planned_arrival_transport_event = planned_arrival_transport_event
        self.planned_waypoint_transport_event = planned_waypoint_transport_event
        self.actual_departure_transport_event = actual_departure_transport_event
        self.actual_waypoint_transport_event = actual_waypoint_transport_event
        self.actual_arrival_transport_event = actual_arrival_transport_event
        self.transport_event = transport_event
        self.estimated_departure_transport_event = estimated_departure_transport_event
        self.estimated_arrival_transport_event = estimated_arrival_transport_event
        self.passenger_person = passenger_person
        self.driver_person = driver_person
        self.reporting_person = reporting_person
        self.crew_member_person = crew_member_person
        self.security_officer_person = security_officer_person
        self.master_person = master_person
        self.ships_surgeon_person = ships_surgeon_person


class __SignatureType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    note = None
    validation_date = None
    validation_time = None
    validator_id = None
    canonicalization_method = None
    signature_method = None
    signatory_party = None
    digital_signature_attachment = None
    original_document_reference = None
    order_list = [
        'id_',
        'note',
        'validation_date',
        'validation_time',
        'validator_id',
        'canonicalization_method',
        'signature_method',
        'signatory_party',
        'digital_signature_attachment',
        'original_document_reference',
    ]

    def __init__(self,		id_: cbc.ID,
                 note: List[cbc.Note] = None,
                 validation_date: cbc.ValidationDate = None,
                 validation_time: cbc.ValidationTime = None,
                 validator_id: cbc.ValidatorID = None,
                 canonicalization_method: cbc.CanonicalizationMethod = None,
                 signature_method: cbc.SignatureMethod = None,
                 signatory_party: 'SignatoryParty' = None,
                 digital_signature_attachment: 'DigitalSignatureAttachment' = None,
                 original_document_reference: 'OriginalDocumentReference' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.note = note
        self.validation_date = validation_date
        self.validation_time = validation_time
        self.validator_id = validator_id
        self.canonicalization_method = canonicalization_method
        self.signature_method = signature_method
        self.signatory_party = signatory_party
        self.digital_signature_attachment = digital_signature_attachment
        self.original_document_reference = original_document_reference


class __StatementLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    note = None
    uuid = None
    balance_brought_forward_indicator = None
    debit_line_amount = None
    credit_line_amount = None
    balance_amount = None
    payment_purpose_code = None
    payment_means = None
    payment_terms = None
    buyer_customer_party = None
    seller_supplier_party = None
    originator_customer_party = None
    accounting_customer_party = None
    accounting_supplier_party = None
    payee_party = None
    invoice_period = None
    billing_reference = None
    document_reference = None
    exchange_rate = None
    allowance_charge = None
    collected_payment = None
    order_list = [
        'id_',
        'note',
        'uuid',
        'balance_brought_forward_indicator',
        'debit_line_amount',
        'credit_line_amount',
        'balance_amount',
        'payment_purpose_code',
        'payment_means',
        'payment_terms',
        'buyer_customer_party',
        'seller_supplier_party',
        'originator_customer_party',
        'accounting_customer_party',
        'accounting_supplier_party',
        'payee_party',
        'invoice_period',
        'billing_reference',
        'document_reference',
        'exchange_rate',
        'allowance_charge',
        'collected_payment',
    ]

    def __init__(self,		id_: cbc.ID,
                 note: List[cbc.Note] = None,
                 uuid: cbc.UUID = None,
                 balance_brought_forward_indicator: cbc.BalanceBroughtForwardIndicator = None,
                 debit_line_amount: cbc.DebitLineAmount = None,
                 credit_line_amount: cbc.CreditLineAmount = None,
                 balance_amount: cbc.BalanceAmount = None,
                 payment_purpose_code: cbc.PaymentPurposeCode = None,
                 payment_means: 'PaymentMeans' = None,
                 payment_terms: List['PaymentTerms'] = None,
                 buyer_customer_party: 'BuyerCustomerParty' = None,
                 seller_supplier_party: 'SellerSupplierParty' = None,
                 originator_customer_party: 'OriginatorCustomerParty' = None,
                 accounting_customer_party: 'AccountingCustomerParty' = None,
                 accounting_supplier_party: 'AccountingSupplierParty' = None,
                 payee_party: 'PayeeParty' = None,
                 invoice_period: List['InvoicePeriod'] = None,
                 billing_reference: List['BillingReference'] = None,
                 document_reference: List['DocumentReference'] = None,
                 exchange_rate: 'ExchangeRate' = None,
                 allowance_charge: List['AllowanceCharge'] = None,
                 collected_payment: List['CollectedPayment'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.note = note
        self.uuid = uuid
        self.balance_brought_forward_indicator = balance_brought_forward_indicator
        self.debit_line_amount = debit_line_amount
        self.credit_line_amount = credit_line_amount
        self.balance_amount = balance_amount
        self.payment_purpose_code = payment_purpose_code
        self.payment_means = payment_means
        self.payment_terms = payment_terms
        self.buyer_customer_party = buyer_customer_party
        self.seller_supplier_party = seller_supplier_party
        self.originator_customer_party = originator_customer_party
        self.accounting_customer_party = accounting_customer_party
        self.accounting_supplier_party = accounting_supplier_party
        self.payee_party = payee_party
        self.invoice_period = invoice_period
        self.billing_reference = billing_reference
        self.document_reference = document_reference
        self.exchange_rate = exchange_rate
        self.allowance_charge = allowance_charge
        self.collected_payment = collected_payment


class __StatusType(PrefixCAC, ComplexXMLParseableObject):
    condition_code = None
    reference_date = None
    reference_time = None
    description = None
    status_reason_code = None
    status_reason = None
    sequence_id = None
    text = None
    indication_indicator = None
    percent = None
    reliability_percent = None
    condition = None
    order_list = [
        'condition_code',
        'reference_date',
        'reference_time',
        'description',
        'status_reason_code',
        'status_reason',
        'sequence_id',
        'text',
        'indication_indicator',
        'percent',
        'reliability_percent',
        'condition',
    ]

    def __init__(self,		condition_code: cbc.ConditionCode = None,
                 reference_date: cbc.ReferenceDate = None,
                 reference_time: cbc.ReferenceTime = None,
                 description: List[cbc.Description] = None,
                 status_reason_code: cbc.StatusReasonCode = None,
                 status_reason: List[cbc.StatusReason] = None,
                 sequence_id: cbc.SequenceID = None,
                 text: List[cbc.Text] = None,
                 indication_indicator: cbc.IndicationIndicator = None,
                 percent: cbc.Percent = None,
                 reliability_percent: cbc.ReliabilityPercent = None,
                 condition: List['Condition'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.condition_code = condition_code
        self.reference_date = reference_date
        self.reference_time = reference_time
        self.description = description
        self.status_reason_code = status_reason_code
        self.status_reason = status_reason
        self.sequence_id = sequence_id
        self.text = text
        self.indication_indicator = indication_indicator
        self.percent = percent
        self.reliability_percent = reliability_percent
        self.condition = condition


class __StockAvailabilityReportLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    quantity = None
    item = None
    note = None
    value_amount = None
    availability_date = None
    availability_status_code = None
    order_list = [
        'id_',
        'note',
        'quantity',
        'value_amount',
        'availability_date',
        'availability_status_code',
        'item',
    ]

    def __init__(self,		id_: cbc.ID,
                 quantity: cbc.Quantity,
                 item: 'Item',
                 note: List[cbc.Note] = None,
                 value_amount: cbc.ValueAmount = None,
                 availability_date: cbc.AvailabilityDate = None,
                 availability_status_code: cbc.AvailabilityStatusCode = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.quantity = quantity
        self.item = item
        self.note = note
        self.value_amount = value_amount
        self.availability_date = availability_date
        self.availability_status_code = availability_status_code


class __StowageType(PrefixCAC, ComplexXMLParseableObject):
    location_id = None
    location = None
    measurement_dimension = None
    order_list = [
        'location_id',
        'location',
        'measurement_dimension',
    ]

    def __init__(self,		location_id: cbc.LocationID = None,
                 location: List[cbc.Location] = None,
                 measurement_dimension: List['MeasurementDimension'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.location_id = location_id
        self.location = location
        self.measurement_dimension = measurement_dimension


class __SubcontractTermsType(PrefixCAC, ComplexXMLParseableObject):
    rate = None
    unknown_price_indicator = None
    description = None
    amount = None
    subcontracting_conditions_code = None
    maximum_percent = None
    minimum_percent = None
    order_list = [
        'rate',
        'unknown_price_indicator',
        'description',
        'amount',
        'subcontracting_conditions_code',
        'maximum_percent',
        'minimum_percent',
    ]

    def __init__(self,		rate: cbc.Rate = None,
                 unknown_price_indicator: cbc.UnknownPriceIndicator = None,
                 description: List[cbc.Description] = None,
                 amount: cbc.Amount = None,
                 subcontracting_conditions_code: cbc.SubcontractingConditionsCode = None,
                 maximum_percent: cbc.MaximumPercent = None,
                 minimum_percent: cbc.MinimumPercent = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.rate = rate
        self.unknown_price_indicator = unknown_price_indicator
        self.description = description
        self.amount = amount
        self.subcontracting_conditions_code = subcontracting_conditions_code
        self.maximum_percent = maximum_percent
        self.minimum_percent = minimum_percent


class __SubscriberConsumptionType(PrefixCAC, ComplexXMLParseableObject):
    utility_consumption_point = None
    consumption_id = None
    specification_type_code = None
    note = None
    total_metered_quantity = None
    subscriber_party = None
    on_account_payment = None
    consumption = None
    supplier_consumption = None
    order_list = [
        'consumption_id',
        'specification_type_code',
        'note',
        'total_metered_quantity',
        'subscriber_party',
        'utility_consumption_point',
        'on_account_payment',
        'consumption',
        'supplier_consumption',
    ]

    def __init__(self,		utility_consumption_point: 'UtilityConsumptionPoint',
                 consumption_id: cbc.ConsumptionID = None,
                 specification_type_code: cbc.SpecificationTypeCode = None,
                 note: List[cbc.Note] = None,
                 total_metered_quantity: cbc.TotalMeteredQuantity = None,
                 subscriber_party: 'SubscriberParty' = None,
                 on_account_payment: List['OnAccountPayment'] = None,
                 consumption: 'Consumption' = None,
                 supplier_consumption: List['SupplierConsumption'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.utility_consumption_point = utility_consumption_point
        self.consumption_id = consumption_id
        self.specification_type_code = specification_type_code
        self.note = note
        self.total_metered_quantity = total_metered_quantity
        self.subscriber_party = subscriber_party
        self.on_account_payment = on_account_payment
        self.consumption = consumption
        self.supplier_consumption = supplier_consumption


class __SupplierConsumptionType(PrefixCAC, ComplexXMLParseableObject):
    consumption = None
    description = None
    utility_supplier_party = None
    utility_customer_party = None
    contract = None
    consumption_line = None
    order_list = [
        'description',
        'utility_supplier_party',
        'utility_customer_party',
        'consumption',
        'contract',
        'consumption_line',
    ]

    def __init__(self,		consumption: 'Consumption',
                 description: List[cbc.Description] = None,
                 utility_supplier_party: 'UtilitySupplierParty' = None,
                 utility_customer_party: 'UtilityCustomerParty' = None,
                 contract: 'Contract' = None,
                 consumption_line: List['ConsumptionLine'] = None, xml_namespaces=None):
        if not consumption_line:
            raise ListMustNotBeEmptyException('consumption_line')
        super().__init__(xml_namespaces)
        self.consumption = consumption
        self.description = description
        self.utility_supplier_party = utility_supplier_party
        self.utility_customer_party = utility_customer_party
        self.contract = contract
        self.consumption_line = consumption_line


class __SupplierPartyType(PrefixCAC, ComplexXMLParseableObject):
    customer_assigned_account_id = None
    additional_account_id = None
    data_sending_capability = None
    party = None
    despatch_contact = None
    accounting_contact = None
    seller_contact = None
    order_list = [
        'customer_assigned_account_id',
        'additional_account_id',
        'data_sending_capability',
        'party',
        'despatch_contact',
        'accounting_contact',
        'seller_contact',
    ]

    def __init__(self,		customer_assigned_account_id: cbc.CustomerAssignedAccountID = None,
                 additional_account_id: List[cbc.AdditionalAccountID] = None,
                 data_sending_capability: cbc.DataSendingCapability = None,
                 party: 'Party' = None,
                 despatch_contact: 'DespatchContact' = None,
                 accounting_contact: 'AccountingContact' = None,
                 seller_contact: 'SellerContact' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.customer_assigned_account_id = customer_assigned_account_id
        self.additional_account_id = additional_account_id
        self.data_sending_capability = data_sending_capability
        self.party = party
        self.despatch_contact = despatch_contact
        self.accounting_contact = accounting_contact
        self.seller_contact = seller_contact


class __TaxCategoryType(PrefixCAC, ComplexXMLParseableObject):
    tax_scheme = None
    id_ = None
    name = None
    percent = None
    base_unit_measure = None
    per_unit_amount = None
    tax_exemption_reason_code = None
    tax_exemption_reason = None
    tier_range = None
    tier_rate_percent = None
    order_list = [
        'id_',
        'name',
        'percent',
        'base_unit_measure',
        'per_unit_amount',
        'tax_exemption_reason_code',
        'tax_exemption_reason',
        'tier_range',
        'tier_rate_percent',
        'tax_scheme',
    ]

    def __init__(self,		tax_scheme: 'TaxScheme',
                 id_: cbc.ID = None,
                 name: cbc.Name = None,
                 percent: cbc.Percent = None,
                 base_unit_measure: cbc.BaseUnitMeasure = None,
                 per_unit_amount: cbc.PerUnitAmount = None,
                 tax_exemption_reason_code: cbc.TaxExemptionReasonCode = None,
                 tax_exemption_reason: List[cbc.TaxExemptionReason] = None,
                 tier_range: cbc.TierRange = None,
                 tier_rate_percent: cbc.TierRatePercent = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.tax_scheme = tax_scheme
        self.id_ = id_
        self.name = name
        self.percent = percent
        self.base_unit_measure = base_unit_measure
        self.per_unit_amount = per_unit_amount
        self.tax_exemption_reason_code = tax_exemption_reason_code
        self.tax_exemption_reason = tax_exemption_reason
        self.tier_range = tier_range
        self.tier_rate_percent = tier_rate_percent


class __TaxSchemeType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    name = None
    tax_type_code = None
    currency_code = None
    jurisdiction_region_address = None
    order_list = [
        'id_',
        'name',
        'tax_type_code',
        'currency_code',
        'jurisdiction_region_address',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 name: cbc.Name = None,
                 tax_type_code: cbc.TaxTypeCode = None,
                 currency_code: cbc.CurrencyCode = None,
                 jurisdiction_region_address: List['JurisdictionRegionAddress'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.name = name
        self.tax_type_code = tax_type_code
        self.currency_code = currency_code
        self.jurisdiction_region_address = jurisdiction_region_address


class __TaxSubtotalType(PrefixCAC, ComplexXMLParseableObject):
    tax_amount = None
    tax_category = None
    taxable_amount = None
    calculation_sequence_numeric = None
    transaction_currency_tax_amount = None
    percent = None
    base_unit_measure = None
    per_unit_amount = None
    tier_range = None
    tier_rate_percent = None
    order_list = [
        'taxable_amount',
        'tax_amount',
        'calculation_sequence_numeric',
        'transaction_currency_tax_amount',
        'percent',
        'base_unit_measure',
        'per_unit_amount',
        'tier_range',
        'tier_rate_percent',
        'tax_category',
    ]

    def __init__(self,		tax_amount: cbc.TaxAmount,
                 tax_category: 'TaxCategory',
                 taxable_amount: cbc.TaxableAmount = None,
                 calculation_sequence_numeric: cbc.CalculationSequenceNumeric = None,
                 transaction_currency_tax_amount: cbc.TransactionCurrencyTaxAmount = None,
                 percent: cbc.Percent = None,
                 base_unit_measure: cbc.BaseUnitMeasure = None,
                 per_unit_amount: cbc.PerUnitAmount = None,
                 tier_range: cbc.TierRange = None,
                 tier_rate_percent: cbc.TierRatePercent = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.tax_amount = tax_amount
        self.tax_category = tax_category
        self.taxable_amount = taxable_amount
        self.calculation_sequence_numeric = calculation_sequence_numeric
        self.transaction_currency_tax_amount = transaction_currency_tax_amount
        self.percent = percent
        self.base_unit_measure = base_unit_measure
        self.per_unit_amount = per_unit_amount
        self.tier_range = tier_range
        self.tier_rate_percent = tier_rate_percent


class __TaxTotalType(PrefixCAC, ComplexXMLParseableObject):
    tax_amount = None
    rounding_amount = None
    tax_evidence_indicator = None
    tax_included_indicator = None
    tax_subtotal = None
    order_list = [
        'tax_amount',
        'rounding_amount',
        'tax_evidence_indicator',
        'tax_included_indicator',
        'tax_subtotal',
    ]

    def __init__(self,		tax_amount: cbc.TaxAmount,
                 rounding_amount: cbc.RoundingAmount = None,
                 tax_evidence_indicator: cbc.TaxEvidenceIndicator = None,
                 tax_included_indicator: cbc.TaxIncludedIndicator = None,
                 tax_subtotal: List['TaxSubtotal'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.tax_amount = tax_amount
        self.rounding_amount = rounding_amount
        self.tax_evidence_indicator = tax_evidence_indicator
        self.tax_included_indicator = tax_included_indicator
        self.tax_subtotal = tax_subtotal


class __TelecommunicationsServiceType(PrefixCAC, ComplexXMLParseableObject):
    call_date = None
    call_time = None
    service_number_called = None
    id_ = None
    telecommunications_service_category = None
    telecommunications_service_category_code = None
    movie_title = None
    roaming_partner_name = None
    pay_per_view = None
    quantity = None
    telecommunications_service_call = None
    telecommunications_service_call_code = None
    call_base_amount = None
    call_extension_amount = None
    price = None
    country = None
    exchange_rate = None
    allowance_charge = None
    tax_total = None
    call_duty = None
    time_duty = None
    order_list = [
        'id_',
        'call_date',
        'call_time',
        'service_number_called',
        'telecommunications_service_category',
        'telecommunications_service_category_code',
        'movie_title',
        'roaming_partner_name',
        'pay_per_view',
        'quantity',
        'telecommunications_service_call',
        'telecommunications_service_call_code',
        'call_base_amount',
        'call_extension_amount',
        'price',
        'country',
        'exchange_rate',
        'allowance_charge',
        'tax_total',
        'call_duty',
        'time_duty',
    ]

    def __init__(self,		call_date: cbc.CallDate,
                 call_time: cbc.CallTime,
                 service_number_called: cbc.ServiceNumberCalled,
                 id_: cbc.ID = None,
                 telecommunications_service_category: cbc.TelecommunicationsServiceCategory = None,
                 telecommunications_service_category_code: cbc.TelecommunicationsServiceCategoryCode = None,
                 movie_title: cbc.MovieTitle = None,
                 roaming_partner_name: cbc.RoamingPartnerName = None,
                 pay_per_view: cbc.PayPerView = None,
                 quantity: cbc.Quantity = None,
                 telecommunications_service_call: cbc.TelecommunicationsServiceCall = None,
                 telecommunications_service_call_code: cbc.TelecommunicationsServiceCallCode = None,
                 call_base_amount: cbc.CallBaseAmount = None,
                 call_extension_amount: cbc.CallExtensionAmount = None,
                 price: 'Price' = None,
                 country: 'Country' = None,
                 exchange_rate: List['ExchangeRate'] = None,
                 allowance_charge: List['AllowanceCharge'] = None,
                 tax_total: List['TaxTotal'] = None,
                 call_duty: List['CallDuty'] = None,
                 time_duty: List['TimeDuty'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.call_date = call_date
        self.call_time = call_time
        self.service_number_called = service_number_called
        self.id_ = id_
        self.telecommunications_service_category = telecommunications_service_category
        self.telecommunications_service_category_code = telecommunications_service_category_code
        self.movie_title = movie_title
        self.roaming_partner_name = roaming_partner_name
        self.pay_per_view = pay_per_view
        self.quantity = quantity
        self.telecommunications_service_call = telecommunications_service_call
        self.telecommunications_service_call_code = telecommunications_service_call_code
        self.call_base_amount = call_base_amount
        self.call_extension_amount = call_extension_amount
        self.price = price
        self.country = country
        self.exchange_rate = exchange_rate
        self.allowance_charge = allowance_charge
        self.tax_total = tax_total
        self.call_duty = call_duty
        self.time_duty = time_duty


class __TelecommunicationsSupplyType(PrefixCAC, ComplexXMLParseableObject):
    privacy_code = None
    telecommunications_supply_type = None
    telecommunications_supply_type_code = None
    description = None
    total_amount = None
    telecommunications_supply_line = None
    order_list = [
        'telecommunications_supply_type',
        'telecommunications_supply_type_code',
        'privacy_code',
        'description',
        'total_amount',
        'telecommunications_supply_line',
    ]

    def __init__(self,		privacy_code: cbc.PrivacyCode,
                 telecommunications_supply_type: cbc.TelecommunicationsSupplyType = None,
                 telecommunications_supply_type_code: cbc.TelecommunicationsSupplyTypeCode = None,
                 description: List[cbc.Description] = None,
                 total_amount: cbc.TotalAmount = None,
                 telecommunications_supply_line: List['TelecommunicationsSupplyLine'] = None, xml_namespaces=None):
        if not telecommunications_supply_line:
            raise ListMustNotBeEmptyException('telecommunications_supply_line')
        super().__init__(xml_namespaces)
        self.privacy_code = privacy_code
        self.telecommunications_supply_type = telecommunications_supply_type
        self.telecommunications_supply_type_code = telecommunications_supply_type_code
        self.description = description
        self.total_amount = total_amount
        self.telecommunications_supply_line = telecommunications_supply_line


class __TelecommunicationsSupplyLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    phone_number = None
    description = None
    line_extension_amount = None
    exchange_rate = None
    allowance_charge = None
    tax_total = None
    telecommunications_service = None
    order_list = [
        'id_',
        'phone_number',
        'description',
        'line_extension_amount',
        'exchange_rate',
        'allowance_charge',
        'tax_total',
        'telecommunications_service',
    ]

    def __init__(self,		id_: cbc.ID,
                 phone_number: cbc.PhoneNumber,
                 description: List[cbc.Description] = None,
                 line_extension_amount: cbc.LineExtensionAmount = None,
                 exchange_rate: List['ExchangeRate'] = None,
                 allowance_charge: List['AllowanceCharge'] = None,
                 tax_total: List['TaxTotal'] = None,
                 telecommunications_service: List['TelecommunicationsService'] = None, xml_namespaces=None):
        if not telecommunications_service:
            raise ListMustNotBeEmptyException('telecommunications_service')
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.phone_number = phone_number
        self.description = description
        self.line_extension_amount = line_extension_amount
        self.exchange_rate = exchange_rate
        self.allowance_charge = allowance_charge
        self.tax_total = tax_total
        self.telecommunications_service = telecommunications_service


class __TemperatureType(PrefixCAC, ComplexXMLParseableObject):
    attribute_id = None
    measure = None
    description = None
    order_list = [
        'attribute_id',
        'measure',
        'description',
    ]

    def __init__(self,		attribute_id: cbc.AttributeID,
                 measure: cbc.Measure,
                 description: List[cbc.Description] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.attribute_id = attribute_id
        self.measure = measure
        self.description = description


class __TenderLineType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    note = None
    quantity = None
    line_extension_amount = None
    total_tax_amount = None
    orderable_unit = None
    content_unit_quantity = None
    order_quantity_increment_numeric = None
    minimum_order_quantity = None
    maximum_order_quantity = None
    warranty_information = None
    pack_level_code = None
    document_reference = None
    item = None
    offered_item_location_quantity = None
    replacement_related_item = None
    warranty_party = None
    warranty_validity_period = None
    sub_tender_line = None
    call_for_tenders_line_reference = None
    call_for_tenders_document_reference = None
    order_list = [
        'id_',
        'note',
        'quantity',
        'line_extension_amount',
        'total_tax_amount',
        'orderable_unit',
        'content_unit_quantity',
        'order_quantity_increment_numeric',
        'minimum_order_quantity',
        'maximum_order_quantity',
        'warranty_information',
        'pack_level_code',
        'document_reference',
        'item',
        'offered_item_location_quantity',
        'replacement_related_item',
        'warranty_party',
        'warranty_validity_period',
        'sub_tender_line',
        'call_for_tenders_line_reference',
        'call_for_tenders_document_reference',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 note: List[cbc.Note] = None,
                 quantity: cbc.Quantity = None,
                 line_extension_amount: cbc.LineExtensionAmount = None,
                 total_tax_amount: cbc.TotalTaxAmount = None,
                 orderable_unit: cbc.OrderableUnit = None,
                 content_unit_quantity: cbc.ContentUnitQuantity = None,
                 order_quantity_increment_numeric: cbc.OrderQuantityIncrementNumeric = None,
                 minimum_order_quantity: cbc.MinimumOrderQuantity = None,
                 maximum_order_quantity: cbc.MaximumOrderQuantity = None,
                 warranty_information: List[cbc.WarrantyInformation] = None,
                 pack_level_code: cbc.PackLevelCode = None,
                 document_reference: List['DocumentReference'] = None,
                 item: 'Item' = None,
                 offered_item_location_quantity: List['OfferedItemLocationQuantity'] = None,
                 replacement_related_item: List['ReplacementRelatedItem'] = None,
                 warranty_party: 'WarrantyParty' = None,
                 warranty_validity_period: 'WarrantyValidityPeriod' = None,
                 sub_tender_line: List['SubTenderLine'] = None,
                 call_for_tenders_line_reference: 'CallForTendersLineReference' = None,
                 call_for_tenders_document_reference: 'CallForTendersDocumentReference' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.note = note
        self.quantity = quantity
        self.line_extension_amount = line_extension_amount
        self.total_tax_amount = total_tax_amount
        self.orderable_unit = orderable_unit
        self.content_unit_quantity = content_unit_quantity
        self.order_quantity_increment_numeric = order_quantity_increment_numeric
        self.minimum_order_quantity = minimum_order_quantity
        self.maximum_order_quantity = maximum_order_quantity
        self.warranty_information = warranty_information
        self.pack_level_code = pack_level_code
        self.document_reference = document_reference
        self.item = item
        self.offered_item_location_quantity = offered_item_location_quantity
        self.replacement_related_item = replacement_related_item
        self.warranty_party = warranty_party
        self.warranty_validity_period = warranty_validity_period
        self.sub_tender_line = sub_tender_line
        self.call_for_tenders_line_reference = call_for_tenders_line_reference
        self.call_for_tenders_document_reference = call_for_tenders_document_reference


class __TenderPreparationType(PrefixCAC, ComplexXMLParseableObject):
    tender_envelope_id = None
    tender_envelope_type_code = None
    description = None
    open_tender_id = None
    procurement_project_lot = None
    document_tender_requirement = None
    order_list = [
        'tender_envelope_id',
        'tender_envelope_type_code',
        'description',
        'open_tender_id',
        'procurement_project_lot',
        'document_tender_requirement',
    ]

    def __init__(self,		tender_envelope_id: cbc.TenderEnvelopeID,
                 tender_envelope_type_code: cbc.TenderEnvelopeTypeCode = None,
                 description: List[cbc.Description] = None,
                 open_tender_id: cbc.OpenTenderID = None,
                 procurement_project_lot: List['ProcurementProjectLot'] = None,
                 document_tender_requirement: List['DocumentTenderRequirement'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.tender_envelope_id = tender_envelope_id
        self.tender_envelope_type_code = tender_envelope_type_code
        self.description = description
        self.open_tender_id = open_tender_id
        self.procurement_project_lot = procurement_project_lot
        self.document_tender_requirement = document_tender_requirement


class __TenderRequirementType(PrefixCAC, ComplexXMLParseableObject):
    name = None
    description = None
    template_document_reference = None
    order_list = [
        'name',
        'description',
        'template_document_reference',
    ]

    def __init__(self,		name: cbc.Name,
                 description: List[cbc.Description] = None,
                 template_document_reference: 'TemplateDocumentReference' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.name = name
        self.description = description
        self.template_document_reference = template_document_reference


class __TenderResultType(PrefixCAC, ComplexXMLParseableObject):
    award_date = None
    tender_result_code = None
    description = None
    advertisement_amount = None
    award_time = None
    received_tender_quantity = None
    lower_tender_amount = None
    higher_tender_amount = None
    start_date = None
    received_electronic_tender_quantity = None
    received_foreign_tender_quantity = None
    contract = None
    awarded_tendered_project = None
    contract_formalization_period = None
    subcontract_terms = None
    winning_party = None
    order_list = [
        'tender_result_code',
        'description',
        'advertisement_amount',
        'award_date',
        'award_time',
        'received_tender_quantity',
        'lower_tender_amount',
        'higher_tender_amount',
        'start_date',
        'received_electronic_tender_quantity',
        'received_foreign_tender_quantity',
        'contract',
        'awarded_tendered_project',
        'contract_formalization_period',
        'subcontract_terms',
        'winning_party',
    ]

    def __init__(self,		award_date: cbc.AwardDate,
                 tender_result_code: cbc.TenderResultCode = None,
                 description: List[cbc.Description] = None,
                 advertisement_amount: cbc.AdvertisementAmount = None,
                 award_time: cbc.AwardTime = None,
                 received_tender_quantity: cbc.ReceivedTenderQuantity = None,
                 lower_tender_amount: cbc.LowerTenderAmount = None,
                 higher_tender_amount: cbc.HigherTenderAmount = None,
                 start_date: cbc.StartDate = None,
                 received_electronic_tender_quantity: cbc.ReceivedElectronicTenderQuantity = None,
                 received_foreign_tender_quantity: cbc.ReceivedForeignTenderQuantity = None,
                 contract: 'Contract' = None,
                 awarded_tendered_project: 'AwardedTenderedProject' = None,
                 contract_formalization_period: 'ContractFormalizationPeriod' = None,
                 subcontract_terms: List['SubcontractTerms'] = None,
                 winning_party: List['WinningParty'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.award_date = award_date
        self.tender_result_code = tender_result_code
        self.description = description
        self.advertisement_amount = advertisement_amount
        self.award_time = award_time
        self.received_tender_quantity = received_tender_quantity
        self.lower_tender_amount = lower_tender_amount
        self.higher_tender_amount = higher_tender_amount
        self.start_date = start_date
        self.received_electronic_tender_quantity = received_electronic_tender_quantity
        self.received_foreign_tender_quantity = received_foreign_tender_quantity
        self.contract = contract
        self.awarded_tendered_project = awarded_tendered_project
        self.contract_formalization_period = contract_formalization_period
        self.subcontract_terms = subcontract_terms
        self.winning_party = winning_party


class __TenderedProjectType(PrefixCAC, ComplexXMLParseableObject):
    variant_id = None
    fee_amount = None
    fee_description = None
    tender_envelope_id = None
    tender_envelope_type_code = None
    procurement_project_lot = None
    evidence_document_reference = None
    tax_total = None
    legal_monetary_total = None
    tender_line = None
    awarding_criterion_response = None
    order_list = [
        'variant_id',
        'fee_amount',
        'fee_description',
        'tender_envelope_id',
        'tender_envelope_type_code',
        'procurement_project_lot',
        'evidence_document_reference',
        'tax_total',
        'legal_monetary_total',
        'tender_line',
        'awarding_criterion_response',
    ]

    def __init__(self,		variant_id: cbc.VariantID = None,
                 fee_amount: cbc.FeeAmount = None,
                 fee_description: List[cbc.FeeDescription] = None,
                 tender_envelope_id: cbc.TenderEnvelopeID = None,
                 tender_envelope_type_code: cbc.TenderEnvelopeTypeCode = None,
                 procurement_project_lot: 'ProcurementProjectLot' = None,
                 evidence_document_reference: List['EvidenceDocumentReference'] = None,
                 tax_total: List['TaxTotal'] = None,
                 legal_monetary_total: 'LegalMonetaryTotal' = None,
                 tender_line: List['TenderLine'] = None,
                 awarding_criterion_response: List['AwardingCriterionResponse'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.variant_id = variant_id
        self.fee_amount = fee_amount
        self.fee_description = fee_description
        self.tender_envelope_id = tender_envelope_id
        self.tender_envelope_type_code = tender_envelope_type_code
        self.procurement_project_lot = procurement_project_lot
        self.evidence_document_reference = evidence_document_reference
        self.tax_total = tax_total
        self.legal_monetary_total = legal_monetary_total
        self.tender_line = tender_line
        self.awarding_criterion_response = awarding_criterion_response


class __TendererPartyQualificationType(PrefixCAC, ComplexXMLParseableObject):
    main_qualifying_party = None
    interested_procurement_project_lot = None
    additional_qualifying_party = None
    order_list = [
        'interested_procurement_project_lot',
        'main_qualifying_party',
        'additional_qualifying_party',
    ]

    def __init__(self,		main_qualifying_party: 'MainQualifyingParty',
                 interested_procurement_project_lot: List['InterestedProcurementProjectLot'] = None,
                 additional_qualifying_party: List['AdditionalQualifyingParty'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.main_qualifying_party = main_qualifying_party
        self.interested_procurement_project_lot = interested_procurement_project_lot
        self.additional_qualifying_party = additional_qualifying_party


class __TendererQualificationRequestType(PrefixCAC, ComplexXMLParseableObject):
    company_legal_form_code = None
    company_legal_form = None
    personal_situation = None
    operating_years_quantity = None
    employee_quantity = None
    description = None
    required_business_classification_scheme = None
    technical_evaluation_criterion = None
    financial_evaluation_criterion = None
    specific_tenderer_requirement = None
    economic_operator_role = None
    order_list = [
        'company_legal_form_code',
        'company_legal_form',
        'personal_situation',
        'operating_years_quantity',
        'employee_quantity',
        'description',
        'required_business_classification_scheme',
        'technical_evaluation_criterion',
        'financial_evaluation_criterion',
        'specific_tenderer_requirement',
        'economic_operator_role',
    ]

    def __init__(self,		company_legal_form_code: cbc.CompanyLegalFormCode = None,
                 company_legal_form: cbc.CompanyLegalForm = None,
                 personal_situation: List[cbc.PersonalSituation] = None,
                 operating_years_quantity: cbc.OperatingYearsQuantity = None,
                 employee_quantity: cbc.EmployeeQuantity = None,
                 description: List[cbc.Description] = None,
                 required_business_classification_scheme: List[
                     'RequiredBusinessClassificationScheme'] = None,
                 technical_evaluation_criterion: List['TechnicalEvaluationCriterion'] = None,
                 financial_evaluation_criterion: List['FinancialEvaluationCriterion'] = None,
                 specific_tenderer_requirement: List['SpecificTendererRequirement'] = None,
                 economic_operator_role: List['EconomicOperatorRole'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.company_legal_form_code = company_legal_form_code
        self.company_legal_form = company_legal_form
        self.personal_situation = personal_situation
        self.operating_years_quantity = operating_years_quantity
        self.employee_quantity = employee_quantity
        self.description = description
        self.required_business_classification_scheme = required_business_classification_scheme
        self.technical_evaluation_criterion = technical_evaluation_criterion
        self.financial_evaluation_criterion = financial_evaluation_criterion
        self.specific_tenderer_requirement = specific_tenderer_requirement
        self.economic_operator_role = economic_operator_role


class __TendererRequirementType(PrefixCAC, ComplexXMLParseableObject):
    name = None
    tenderer_requirement_type_code = None
    description = None
    legal_reference = None
    suggested_evidence = None
    order_list = [
        'name',
        'tenderer_requirement_type_code',
        'description',
        'legal_reference',
        'suggested_evidence',
    ]

    def __init__(self,		name: List[cbc.Name] = None,
                 tenderer_requirement_type_code: cbc.TendererRequirementTypeCode = None,
                 description: List[cbc.Description] = None,
                 legal_reference: cbc.LegalReference = None,
                 suggested_evidence: List['SuggestedEvidence'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.name = name
        self.tenderer_requirement_type_code = tenderer_requirement_type_code
        self.description = description
        self.legal_reference = legal_reference
        self.suggested_evidence = suggested_evidence


class __TenderingProcessType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    original_contracting_system_id = None
    description = None
    negotiation_description = None
    procedure_code = None
    urgency_code = None
    expense_code = None
    part_presentation_code = None
    contracting_system_code = None
    submission_method_code = None
    candidate_reduction_constraint_indicator = None
    government_agreement_constraint_indicator = None
    document_availability_period = None
    tender_submission_deadline_period = None
    invitation_submission_period = None
    participation_request_reception_period = None
    notice_document_reference = None
    additional_document_reference = None
    process_justification = None
    economic_operator_short_list = None
    open_tender_event = None
    auction_terms = None
    framework_agreement = None
    order_list = [
        'id_',
        'original_contracting_system_id',
        'description',
        'negotiation_description',
        'procedure_code',
        'urgency_code',
        'expense_code',
        'part_presentation_code',
        'contracting_system_code',
        'submission_method_code',
        'candidate_reduction_constraint_indicator',
        'government_agreement_constraint_indicator',
        'document_availability_period',
        'tender_submission_deadline_period',
        'invitation_submission_period',
        'participation_request_reception_period',
        'notice_document_reference',
        'additional_document_reference',
        'process_justification',
        'economic_operator_short_list',
        'open_tender_event',
        'auction_terms',
        'framework_agreement',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 original_contracting_system_id: cbc.OriginalContractingSystemID = None,
                 description: List[cbc.Description] = None,
                 negotiation_description: List[cbc.NegotiationDescription] = None,
                 procedure_code: cbc.ProcedureCode = None,
                 urgency_code: cbc.UrgencyCode = None,
                 expense_code: cbc.ExpenseCode = None,
                 part_presentation_code: cbc.PartPresentationCode = None,
                 contracting_system_code: cbc.ContractingSystemCode = None,
                 submission_method_code: cbc.SubmissionMethodCode = None,
                 candidate_reduction_constraint_indicator: cbc.CandidateReductionConstraintIndicator = None,
                 government_agreement_constraint_indicator: cbc.GovernmentAgreementConstraintIndicator = None,
                 document_availability_period: 'DocumentAvailabilityPeriod' = None,
                 tender_submission_deadline_period: 'TenderSubmissionDeadlinePeriod' = None,
                 invitation_submission_period: 'InvitationSubmissionPeriod' = None,
                 participation_request_reception_period: 'ParticipationRequestReceptionPeriod' = None,
                 notice_document_reference: List['NoticeDocumentReference'] = None,
                 additional_document_reference: List['AdditionalDocumentReference'] = None,
                 process_justification: List['ProcessJustification'] = None,
                 economic_operator_short_list: 'EconomicOperatorShortList' = None,
                 open_tender_event: List['OpenTenderEvent'] = None,
                 auction_terms: 'AuctionTerms' = None,
                 framework_agreement: 'FrameworkAgreement' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.original_contracting_system_id = original_contracting_system_id
        self.description = description
        self.negotiation_description = negotiation_description
        self.procedure_code = procedure_code
        self.urgency_code = urgency_code
        self.expense_code = expense_code
        self.part_presentation_code = part_presentation_code
        self.contracting_system_code = contracting_system_code
        self.submission_method_code = submission_method_code
        self.candidate_reduction_constraint_indicator = candidate_reduction_constraint_indicator
        self.government_agreement_constraint_indicator = government_agreement_constraint_indicator
        self.document_availability_period = document_availability_period
        self.tender_submission_deadline_period = tender_submission_deadline_period
        self.invitation_submission_period = invitation_submission_period
        self.participation_request_reception_period = participation_request_reception_period
        self.notice_document_reference = notice_document_reference
        self.additional_document_reference = additional_document_reference
        self.process_justification = process_justification
        self.economic_operator_short_list = economic_operator_short_list
        self.open_tender_event = open_tender_event
        self.auction_terms = auction_terms
        self.framework_agreement = framework_agreement


class __TenderingTermsType(PrefixCAC, ComplexXMLParseableObject):
    awarding_method_type_code = None
    price_evaluation_code = None
    maximum_variant_quantity = None
    variant_constraint_indicator = None
    accepted_variants_description = None
    price_revision_formula_description = None
    funding_program_code = None
    funding_program = None
    maximum_advertisement_amount = None
    note = None
    payment_frequency_code = None
    economic_operator_registry_uri = None
    required_curricula_indicator = None
    other_conditions_indicator = None
    additional_conditions = None
    latest_security_clearance_date = None
    documentation_fee_amount = None
    penalty_clause = None
    required_financial_guarantee = None
    procurement_legislation_document_reference = None
    fiscal_legislation_document_reference = None
    environmental_legislation_document_reference = None
    employment_legislation_document_reference = None
    contractual_document_reference = None
    call_for_tenders_document_reference = None
    warranty_validity_period = None
    payment_terms = None
    tenderer_qualification_request = None
    allowed_subcontract_terms = None
    tender_preparation = None
    contract_execution_requirement = None
    awarding_terms = None
    additional_information_party = None
    document_provider_party = None
    tender_recipient_party = None
    contract_responsible_party = None
    tender_evaluation_party = None
    tender_validity_period = None
    contract_acceptance_period = None
    appeal_terms = None
    language = None
    budget_account_line = None
    replaced_notice_document_reference = None
    order_list = [
        'awarding_method_type_code',
        'price_evaluation_code',
        'maximum_variant_quantity',
        'variant_constraint_indicator',
        'accepted_variants_description',
        'price_revision_formula_description',
        'funding_program_code',
        'funding_program',
        'maximum_advertisement_amount',
        'note',
        'payment_frequency_code',
        'economic_operator_registry_uri',
        'required_curricula_indicator',
        'other_conditions_indicator',
        'additional_conditions',
        'latest_security_clearance_date',
        'documentation_fee_amount',
        'penalty_clause',
        'required_financial_guarantee',
        'procurement_legislation_document_reference',
        'fiscal_legislation_document_reference',
        'environmental_legislation_document_reference',
        'employment_legislation_document_reference',
        'contractual_document_reference',
        'call_for_tenders_document_reference',
        'warranty_validity_period',
        'payment_terms',
        'tenderer_qualification_request',
        'allowed_subcontract_terms',
        'tender_preparation',
        'contract_execution_requirement',
        'awarding_terms',
        'additional_information_party',
        'document_provider_party',
        'tender_recipient_party',
        'contract_responsible_party',
        'tender_evaluation_party',
        'tender_validity_period',
        'contract_acceptance_period',
        'appeal_terms',
        'language',
        'budget_account_line',
        'replaced_notice_document_reference',
    ]

    def __init__(self,		awarding_method_type_code: cbc.AwardingMethodTypeCode = None,
                 price_evaluation_code: cbc.PriceEvaluationCode = None,
                 maximum_variant_quantity: cbc.MaximumVariantQuantity = None,
                 variant_constraint_indicator: cbc.VariantConstraintIndicator = None,
                 accepted_variants_description: List[cbc.AcceptedVariantsDescription] = None,
                 price_revision_formula_description: List[cbc.PriceRevisionFormulaDescription] = None,
                 funding_program_code: cbc.FundingProgramCode = None,
                 funding_program: List[cbc.FundingProgram] = None,
                 maximum_advertisement_amount: cbc.MaximumAdvertisementAmount = None,
                 note: List[cbc.Note] = None,
                 payment_frequency_code: cbc.PaymentFrequencyCode = None,
                 economic_operator_registry_uri: cbc.EconomicOperatorRegistryURI = None,
                 required_curricula_indicator: cbc.RequiredCurriculaIndicator = None,
                 other_conditions_indicator: cbc.OtherConditionsIndicator = None,
                 additional_conditions: List[cbc.AdditionalConditions] = None,
                 latest_security_clearance_date: cbc.LatestSecurityClearanceDate = None,
                 documentation_fee_amount: cbc.DocumentationFeeAmount = None,
                 penalty_clause: List['PenaltyClause'] = None,
                 required_financial_guarantee: List['RequiredFinancialGuarantee'] = None,
                 procurement_legislation_document_reference: 'ProcurementLegislationDocumentReference' = None,
                 fiscal_legislation_document_reference: 'FiscalLegislationDocumentReference' = None,
                 environmental_legislation_document_reference: 'EnvironmentalLegislationDocumentReference' = None,
                 employment_legislation_document_reference: 'EmploymentLegislationDocumentReference' = None,
                 contractual_document_reference: List['ContractualDocumentReference'] = None,
                 call_for_tenders_document_reference: 'CallForTendersDocumentReference' = None,
                 warranty_validity_period: 'WarrantyValidityPeriod' = None,
                 payment_terms: List['PaymentTerms'] = None,
                 tenderer_qualification_request: List['TendererQualificationRequest'] = None,
                 allowed_subcontract_terms: List['AllowedSubcontractTerms'] = None,
                 tender_preparation: List['TenderPreparation'] = None,
                 contract_execution_requirement: List['ContractExecutionRequirement'] = None,
                 awarding_terms: 'AwardingTerms' = None,
                 additional_information_party: 'AdditionalInformationParty' = None,
                 document_provider_party: 'DocumentProviderParty' = None,
                 tender_recipient_party: 'TenderRecipientParty' = None,
                 contract_responsible_party: 'ContractResponsibleParty' = None,
                 tender_evaluation_party: List['TenderEvaluationParty'] = None,
                 tender_validity_period: 'TenderValidityPeriod' = None,
                 contract_acceptance_period: 'ContractAcceptancePeriod' = None,
                 appeal_terms: 'AppealTerms' = None,
                 language: List['Language'] = None,
                 budget_account_line: List['BudgetAccountLine'] = None,
                 replaced_notice_document_reference: 'ReplacedNoticeDocumentReference' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.awarding_method_type_code = awarding_method_type_code
        self.price_evaluation_code = price_evaluation_code
        self.maximum_variant_quantity = maximum_variant_quantity
        self.variant_constraint_indicator = variant_constraint_indicator
        self.accepted_variants_description = accepted_variants_description
        self.price_revision_formula_description = price_revision_formula_description
        self.funding_program_code = funding_program_code
        self.funding_program = funding_program
        self.maximum_advertisement_amount = maximum_advertisement_amount
        self.note = note
        self.payment_frequency_code = payment_frequency_code
        self.economic_operator_registry_uri = economic_operator_registry_uri
        self.required_curricula_indicator = required_curricula_indicator
        self.other_conditions_indicator = other_conditions_indicator
        self.additional_conditions = additional_conditions
        self.latest_security_clearance_date = latest_security_clearance_date
        self.documentation_fee_amount = documentation_fee_amount
        self.penalty_clause = penalty_clause
        self.required_financial_guarantee = required_financial_guarantee
        self.procurement_legislation_document_reference = procurement_legislation_document_reference
        self.fiscal_legislation_document_reference = fiscal_legislation_document_reference
        self.environmental_legislation_document_reference = environmental_legislation_document_reference
        self.employment_legislation_document_reference = employment_legislation_document_reference
        self.contractual_document_reference = contractual_document_reference
        self.call_for_tenders_document_reference = call_for_tenders_document_reference
        self.warranty_validity_period = warranty_validity_period
        self.payment_terms = payment_terms
        self.tenderer_qualification_request = tenderer_qualification_request
        self.allowed_subcontract_terms = allowed_subcontract_terms
        self.tender_preparation = tender_preparation
        self.contract_execution_requirement = contract_execution_requirement
        self.awarding_terms = awarding_terms
        self.additional_information_party = additional_information_party
        self.document_provider_party = document_provider_party
        self.tender_recipient_party = tender_recipient_party
        self.contract_responsible_party = contract_responsible_party
        self.tender_evaluation_party = tender_evaluation_party
        self.tender_validity_period = tender_validity_period
        self.contract_acceptance_period = contract_acceptance_period
        self.appeal_terms = appeal_terms
        self.language = language
        self.budget_account_line = budget_account_line
        self.replaced_notice_document_reference = replaced_notice_document_reference


class __TradeFinancingType(PrefixCAC, ComplexXMLParseableObject):
    financing_party = None
    id_ = None
    financing_instrument_code = None
    contract_document_reference = None
    document_reference = None
    financing_financial_account = None
    clause = None
    order_list = [
        'id_',
        'financing_instrument_code',
        'contract_document_reference',
        'document_reference',
        'financing_party',
        'financing_financial_account',
        'clause',
    ]

    def __init__(self,		financing_party: 'FinancingParty',
                 id_: cbc.ID = None,
                 financing_instrument_code: cbc.FinancingInstrumentCode = None,
                 contract_document_reference: 'ContractDocumentReference' = None,
                 document_reference: List['DocumentReference'] = None,
                 financing_financial_account: 'FinancingFinancialAccount' = None,
                 clause: List['Clause'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.financing_party = financing_party
        self.id_ = id_
        self.financing_instrument_code = financing_instrument_code
        self.contract_document_reference = contract_document_reference
        self.document_reference = document_reference
        self.financing_financial_account = financing_financial_account
        self.clause = clause


class __TradingTermsType(PrefixCAC, ComplexXMLParseableObject):
    information = None
    reference = None
    applicable_address = None
    order_list = [
        'information',
        'reference',
        'applicable_address',
    ]

    def __init__(self,		information: List[cbc.Information] = None,
                 reference: cbc.Reference = None,
                 applicable_address: 'ApplicableAddress' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.information = information
        self.reference = reference
        self.applicable_address = applicable_address


class __TransactionConditionsType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    action_code = None
    description = None
    document_reference = None
    order_list = [
        'id_',
        'action_code',
        'description',
        'document_reference',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 action_code: cbc.ActionCode = None,
                 description: List[cbc.Description] = None,
                 document_reference: List['DocumentReference'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.action_code = action_code
        self.description = description
        self.document_reference = document_reference


class __TransportEquipmentType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    referenced_consignment_id = None
    transport_equipment_type_code = None
    provider_type_code = None
    owner_type_code = None
    size_type_code = None
    disposition_code = None
    fullness_indication_code = None
    refrigeration_on_indicator = None
    information = None
    returnability_indicator = None
    legal_status_indicator = None
    air_flow_percent = None
    humidity_percent = None
    animal_food_approved_indicator = None
    human_food_approved_indicator = None
    dangerous_goods_approved_indicator = None
    refrigerated_indicator = None
    characteristics = None
    damage_remarks = None
    description = None
    special_transport_requirements = None
    gross_weight_measure = None
    gross_volume_measure = None
    tare_weight_measure = None
    tracking_device_code = None
    power_indicator = None
    trace_id = None
    measurement_dimension = None
    transport_equipment_seal = None
    minimum_temperature = None
    maximum_temperature = None
    provider_party = None
    loading_proof_party = None
    supplier_party = None
    owner_party = None
    operating_party = None
    loading_location = None
    unloading_location = None
    storage_location = None
    positioning_transport_event = None
    quarantine_transport_event = None
    delivery_transport_event = None
    pickup_transport_event = None
    handling_transport_event = None
    loading_transport_event = None
    transport_event = None
    applicable_transport_means = None
    haulage_trading_terms = None
    hazardous_goods_transit = None
    packaged_transport_handling_unit = None
    service_allowance_charge = None
    freight_allowance_charge = None
    attached_transport_equipment = None
    delivery = None
    pickup = None
    despatch = None
    shipment_document_reference = None
    contained_in_transport_equipment = None
    package = None
    goods_item = None
    order_list = [
        'id_',
        'referenced_consignment_id',
        'transport_equipment_type_code',
        'provider_type_code',
        'owner_type_code',
        'size_type_code',
        'disposition_code',
        'fullness_indication_code',
        'refrigeration_on_indicator',
        'information',
        'returnability_indicator',
        'legal_status_indicator',
        'air_flow_percent',
        'humidity_percent',
        'animal_food_approved_indicator',
        'human_food_approved_indicator',
        'dangerous_goods_approved_indicator',
        'refrigerated_indicator',
        'characteristics',
        'damage_remarks',
        'description',
        'special_transport_requirements',
        'gross_weight_measure',
        'gross_volume_measure',
        'tare_weight_measure',
        'tracking_device_code',
        'power_indicator',
        'trace_id',
        'measurement_dimension',
        'transport_equipment_seal',
        'minimum_temperature',
        'maximum_temperature',
        'provider_party',
        'loading_proof_party',
        'supplier_party',
        'owner_party',
        'operating_party',
        'loading_location',
        'unloading_location',
        'storage_location',
        'positioning_transport_event',
        'quarantine_transport_event',
        'delivery_transport_event',
        'pickup_transport_event',
        'handling_transport_event',
        'loading_transport_event',
        'transport_event',
        'applicable_transport_means',
        'haulage_trading_terms',
        'hazardous_goods_transit',
        'packaged_transport_handling_unit',
        'service_allowance_charge',
        'freight_allowance_charge',
        'attached_transport_equipment',
        'delivery',
        'pickup',
        'despatch',
        'shipment_document_reference',
        'contained_in_transport_equipment',
        'package',
        'goods_item',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 referenced_consignment_id: List[cbc.ReferencedConsignmentID] = None,
                 transport_equipment_type_code: cbc.TransportEquipmentTypeCode = None,
                 provider_type_code: cbc.ProviderTypeCode = None,
                 owner_type_code: cbc.OwnerTypeCode = None,
                 size_type_code: cbc.SizeTypeCode = None,
                 disposition_code: cbc.DispositionCode = None,
                 fullness_indication_code: cbc.FullnessIndicationCode = None,
                 refrigeration_on_indicator: cbc.RefrigerationOnIndicator = None,
                 information: List[cbc.Information] = None,
                 returnability_indicator: cbc.ReturnabilityIndicator = None,
                 legal_status_indicator: cbc.LegalStatusIndicator = None,
                 air_flow_percent: cbc.AirFlowPercent = None,
                 humidity_percent: cbc.HumidityPercent = None,
                 animal_food_approved_indicator: cbc.AnimalFoodApprovedIndicator = None,
                 human_food_approved_indicator: cbc.HumanFoodApprovedIndicator = None,
                 dangerous_goods_approved_indicator: cbc.DangerousGoodsApprovedIndicator = None,
                 refrigerated_indicator: cbc.RefrigeratedIndicator = None,
                 characteristics: cbc.Characteristics = None,
                 damage_remarks: List[cbc.DamageRemarks] = None,
                 description: List[cbc.Description] = None,
                 special_transport_requirements: List[cbc.SpecialTransportRequirements] = None,
                 gross_weight_measure: cbc.GrossWeightMeasure = None,
                 gross_volume_measure: cbc.GrossVolumeMeasure = None,
                 tare_weight_measure: cbc.TareWeightMeasure = None,
                 tracking_device_code: cbc.TrackingDeviceCode = None,
                 power_indicator: cbc.PowerIndicator = None,
                 trace_id: cbc.TraceID = None,
                 measurement_dimension: List['MeasurementDimension'] = None,
                 transport_equipment_seal: List['TransportEquipmentSeal'] = None,
                 minimum_temperature: 'MinimumTemperature' = None,
                 maximum_temperature: 'MaximumTemperature' = None,
                 provider_party: 'ProviderParty' = None,
                 loading_proof_party: 'LoadingProofParty' = None,
                 supplier_party: 'SupplierParty' = None,
                 owner_party: 'OwnerParty' = None,
                 operating_party: 'OperatingParty' = None,
                 loading_location: 'LoadingLocation' = None,
                 unloading_location: 'UnloadingLocation' = None,
                 storage_location: 'StorageLocation' = None,
                 positioning_transport_event: List['PositioningTransportEvent'] = None,
                 quarantine_transport_event: List['QuarantineTransportEvent'] = None,
                 delivery_transport_event: List['DeliveryTransportEvent'] = None,
                 pickup_transport_event: List['PickupTransportEvent'] = None,
                 handling_transport_event: List['HandlingTransportEvent'] = None,
                 loading_transport_event: List['LoadingTransportEvent'] = None,
                 transport_event: List['TransportEvent'] = None,
                 applicable_transport_means: 'ApplicableTransportMeans' = None,
                 haulage_trading_terms: List['HaulageTradingTerms'] = None,
                 hazardous_goods_transit: List['HazardousGoodsTransit'] = None,
                 packaged_transport_handling_unit: List['PackagedTransportHandlingUnit'] = None,
                 service_allowance_charge: List['ServiceAllowanceCharge'] = None,
                 freight_allowance_charge: List['FreightAllowanceCharge'] = None,
                 attached_transport_equipment: List['AttachedTransportEquipment'] = None,
                 delivery: 'Delivery' = None,
                 pickup: 'Pickup' = None,
                 despatch: 'Despatch' = None,
                 shipment_document_reference: List['ShipmentDocumentReference'] = None,
                 contained_in_transport_equipment: List['ContainedInTransportEquipment'] = None,
                 package: List['Package'] = None,
                 goods_item: List['GoodsItem'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.referenced_consignment_id = referenced_consignment_id
        self.transport_equipment_type_code = transport_equipment_type_code
        self.provider_type_code = provider_type_code
        self.owner_type_code = owner_type_code
        self.size_type_code = size_type_code
        self.disposition_code = disposition_code
        self.fullness_indication_code = fullness_indication_code
        self.refrigeration_on_indicator = refrigeration_on_indicator
        self.information = information
        self.returnability_indicator = returnability_indicator
        self.legal_status_indicator = legal_status_indicator
        self.air_flow_percent = air_flow_percent
        self.humidity_percent = humidity_percent
        self.animal_food_approved_indicator = animal_food_approved_indicator
        self.human_food_approved_indicator = human_food_approved_indicator
        self.dangerous_goods_approved_indicator = dangerous_goods_approved_indicator
        self.refrigerated_indicator = refrigerated_indicator
        self.characteristics = characteristics
        self.damage_remarks = damage_remarks
        self.description = description
        self.special_transport_requirements = special_transport_requirements
        self.gross_weight_measure = gross_weight_measure
        self.gross_volume_measure = gross_volume_measure
        self.tare_weight_measure = tare_weight_measure
        self.tracking_device_code = tracking_device_code
        self.power_indicator = power_indicator
        self.trace_id = trace_id
        self.measurement_dimension = measurement_dimension
        self.transport_equipment_seal = transport_equipment_seal
        self.minimum_temperature = minimum_temperature
        self.maximum_temperature = maximum_temperature
        self.provider_party = provider_party
        self.loading_proof_party = loading_proof_party
        self.supplier_party = supplier_party
        self.owner_party = owner_party
        self.operating_party = operating_party
        self.loading_location = loading_location
        self.unloading_location = unloading_location
        self.storage_location = storage_location
        self.positioning_transport_event = positioning_transport_event
        self.quarantine_transport_event = quarantine_transport_event
        self.delivery_transport_event = delivery_transport_event
        self.pickup_transport_event = pickup_transport_event
        self.handling_transport_event = handling_transport_event
        self.loading_transport_event = loading_transport_event
        self.transport_event = transport_event
        self.applicable_transport_means = applicable_transport_means
        self.haulage_trading_terms = haulage_trading_terms
        self.hazardous_goods_transit = hazardous_goods_transit
        self.packaged_transport_handling_unit = packaged_transport_handling_unit
        self.service_allowance_charge = service_allowance_charge
        self.freight_allowance_charge = freight_allowance_charge
        self.attached_transport_equipment = attached_transport_equipment
        self.delivery = delivery
        self.pickup = pickup
        self.despatch = despatch
        self.shipment_document_reference = shipment_document_reference
        self.contained_in_transport_equipment = contained_in_transport_equipment
        self.package = package
        self.goods_item = goods_item


class __TransportEquipmentSealType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    seal_issuer_type_code = None
    condition = None
    seal_status_code = None
    sealing_party_type = None
    order_list = [
        'id_',
        'seal_issuer_type_code',
        'condition',
        'seal_status_code',
        'sealing_party_type',
    ]

    def __init__(self,		id_: cbc.ID,
                 seal_issuer_type_code: cbc.SealIssuerTypeCode = None,
                 condition: cbc.Condition = None,
                 seal_status_code: cbc.SealStatusCode = None,
                 sealing_party_type: cbc.SealingPartyType = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.seal_issuer_type_code = seal_issuer_type_code
        self.condition = condition
        self.seal_status_code = seal_status_code
        self.sealing_party_type = sealing_party_type


class __TransportEventType(PrefixCAC, ComplexXMLParseableObject):
    identification_id = None
    occurrence_date = None
    occurrence_time = None
    transport_event_type_code = None
    description = None
    completion_indicator = None
    reported_shipment = None
    current_status = None
    contact = None
    location = None
    signature = None
    period = None
    order_list = [
        'identification_id',
        'occurrence_date',
        'occurrence_time',
        'transport_event_type_code',
        'description',
        'completion_indicator',
        'reported_shipment',
        'current_status',
        'contact',
        'location',
        'signature',
        'period',
    ]

    def __init__(self,		identification_id: cbc.IdentificationID = None,
                 occurrence_date: cbc.OccurrenceDate = None,
                 occurrence_time: cbc.OccurrenceTime = None,
                 transport_event_type_code: cbc.TransportEventTypeCode = None,
                 description: List[cbc.Description] = None,
                 completion_indicator: cbc.CompletionIndicator = None,
                 reported_shipment: 'ReportedShipment' = None,
                 current_status: List['CurrentStatus'] = None,
                 contact: List['Contact'] = None,
                 location: 'Location' = None,
                 signature: 'Signature' = None,
                 period: List['Period'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.identification_id = identification_id
        self.occurrence_date = occurrence_date
        self.occurrence_time = occurrence_time
        self.transport_event_type_code = transport_event_type_code
        self.description = description
        self.completion_indicator = completion_indicator
        self.reported_shipment = reported_shipment
        self.current_status = current_status
        self.contact = contact
        self.location = location
        self.signature = signature
        self.period = period


class __TransportExecutionTermsType(PrefixCAC, ComplexXMLParseableObject):
    transport_user_special_terms = None
    transport_service_provider_special_terms = None
    change_conditions = None
    payment_terms = None
    delivery_terms = None
    bonus_payment_terms = None
    commission_payment_terms = None
    penalty_payment_terms = None
    environmental_emission = None
    notification_requirement = None
    service_charge_payment_terms = None
    order_list = [
        'transport_user_special_terms',
        'transport_service_provider_special_terms',
        'change_conditions',
        'payment_terms',
        'delivery_terms',
        'bonus_payment_terms',
        'commission_payment_terms',
        'penalty_payment_terms',
        'environmental_emission',
        'notification_requirement',
        'service_charge_payment_terms',
    ]

    def __init__(self,		transport_user_special_terms: List[cbc.TransportUserSpecialTerms] = None,
                 transport_service_provider_special_terms: List[
                     cbc.TransportServiceProviderSpecialTerms] = None,
                 change_conditions: List[cbc.ChangeConditions] = None,
                 payment_terms: List['PaymentTerms'] = None,
                 delivery_terms: List['DeliveryTerms'] = None,
                 bonus_payment_terms: 'BonusPaymentTerms' = None,
                 commission_payment_terms: 'CommissionPaymentTerms' = None,
                 penalty_payment_terms: 'PenaltyPaymentTerms' = None,
                 environmental_emission: List['EnvironmentalEmission'] = None,
                 notification_requirement: List['NotificationRequirement'] = None,
                 service_charge_payment_terms: 'ServiceChargePaymentTerms' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.transport_user_special_terms = transport_user_special_terms
        self.transport_service_provider_special_terms = transport_service_provider_special_terms
        self.change_conditions = change_conditions
        self.payment_terms = payment_terms
        self.delivery_terms = delivery_terms
        self.bonus_payment_terms = bonus_payment_terms
        self.commission_payment_terms = commission_payment_terms
        self.penalty_payment_terms = penalty_payment_terms
        self.environmental_emission = environmental_emission
        self.notification_requirement = notification_requirement
        self.service_charge_payment_terms = service_charge_payment_terms


class __TransportHandlingUnitType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    transport_handling_unit_type_code = None
    handling_code = None
    handling_instructions = None
    hazardous_risk_indicator = None
    total_goods_item_quantity = None
    total_package_quantity = None
    damage_remarks = None
    shipping_marks = None
    trace_id = None
    handling_unit_despatch_line = None
    actual_package = None
    received_handling_unit_receipt_line = None
    transport_equipment = None
    transport_means = None
    hazardous_goods_transit = None
    measurement_dimension = None
    minimum_temperature = None
    maximum_temperature = None
    goods_item = None
    floor_space_measurement_dimension = None
    pallet_space_measurement_dimension = None
    shipment_document_reference = None
    status = None
    customs_declaration = None
    referenced_shipment = None
    package = None
    order_list = [
        'id_',
        'transport_handling_unit_type_code',
        'handling_code',
        'handling_instructions',
        'hazardous_risk_indicator',
        'total_goods_item_quantity',
        'total_package_quantity',
        'damage_remarks',
        'shipping_marks',
        'trace_id',
        'handling_unit_despatch_line',
        'actual_package',
        'received_handling_unit_receipt_line',
        'transport_equipment',
        'transport_means',
        'hazardous_goods_transit',
        'measurement_dimension',
        'minimum_temperature',
        'maximum_temperature',
        'goods_item',
        'floor_space_measurement_dimension',
        'pallet_space_measurement_dimension',
        'shipment_document_reference',
        'status',
        'customs_declaration',
        'referenced_shipment',
        'package',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 transport_handling_unit_type_code: cbc.TransportHandlingUnitTypeCode = None,
                 handling_code: cbc.HandlingCode = None,
                 handling_instructions: List[cbc.HandlingInstructions] = None,
                 hazardous_risk_indicator: cbc.HazardousRiskIndicator = None,
                 total_goods_item_quantity: cbc.TotalGoodsItemQuantity = None,
                 total_package_quantity: cbc.TotalPackageQuantity = None,
                 damage_remarks: List[cbc.DamageRemarks] = None,
                 shipping_marks: List[cbc.ShippingMarks] = None,
                 trace_id: cbc.TraceID = None,
                 handling_unit_despatch_line: List['HandlingUnitDespatchLine'] = None,
                 actual_package: List['ActualPackage'] = None,
                 received_handling_unit_receipt_line: List['ReceivedHandlingUnitReceiptLine'] = None,
                 transport_equipment: List['TransportEquipment'] = None,
                 transport_means: List['TransportMeans'] = None,
                 hazardous_goods_transit: List['HazardousGoodsTransit'] = None,
                 measurement_dimension: List['MeasurementDimension'] = None,
                 minimum_temperature: 'MinimumTemperature' = None,
                 maximum_temperature: 'MaximumTemperature' = None,
                 goods_item: List['GoodsItem'] = None,
                 floor_space_measurement_dimension: 'FloorSpaceMeasurementDimension' = None,
                 pallet_space_measurement_dimension: 'PalletSpaceMeasurementDimension' = None,
                 shipment_document_reference: List['ShipmentDocumentReference'] = None,
                 status: List['Status'] = None,
                 customs_declaration: List['CustomsDeclaration'] = None,
                 referenced_shipment: List['ReferencedShipment'] = None,
                 package: List['Package'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.transport_handling_unit_type_code = transport_handling_unit_type_code
        self.handling_code = handling_code
        self.handling_instructions = handling_instructions
        self.hazardous_risk_indicator = hazardous_risk_indicator
        self.total_goods_item_quantity = total_goods_item_quantity
        self.total_package_quantity = total_package_quantity
        self.damage_remarks = damage_remarks
        self.shipping_marks = shipping_marks
        self.trace_id = trace_id
        self.handling_unit_despatch_line = handling_unit_despatch_line
        self.actual_package = actual_package
        self.received_handling_unit_receipt_line = received_handling_unit_receipt_line
        self.transport_equipment = transport_equipment
        self.transport_means = transport_means
        self.hazardous_goods_transit = hazardous_goods_transit
        self.measurement_dimension = measurement_dimension
        self.minimum_temperature = minimum_temperature
        self.maximum_temperature = maximum_temperature
        self.goods_item = goods_item
        self.floor_space_measurement_dimension = floor_space_measurement_dimension
        self.pallet_space_measurement_dimension = pallet_space_measurement_dimension
        self.shipment_document_reference = shipment_document_reference
        self.status = status
        self.customs_declaration = customs_declaration
        self.referenced_shipment = referenced_shipment
        self.package = package


class __TransportMeansType(PrefixCAC, ComplexXMLParseableObject):
    journey_id = None
    registration_nationality_id = None
    registration_nationality = None
    direction_code = None
    transport_means_type_code = None
    trade_service_code = None
    stowage = None
    air_transport = None
    road_transport = None
    rail_transport = None
    maritime_transport = None
    owner_party = None
    measurement_dimension = None
    order_list = [
        'journey_id',
        'registration_nationality_id',
        'registration_nationality',
        'direction_code',
        'transport_means_type_code',
        'trade_service_code',
        'stowage',
        'air_transport',
        'road_transport',
        'rail_transport',
        'maritime_transport',
        'owner_party',
        'measurement_dimension',
    ]

    def __init__(self,		journey_id: cbc.JourneyID = None,
                 registration_nationality_id: cbc.RegistrationNationalityID = None,
                 registration_nationality: List[cbc.RegistrationNationality] = None,
                 direction_code: cbc.DirectionCode = None,
                 transport_means_type_code: cbc.TransportMeansTypeCode = None,
                 trade_service_code: cbc.TradeServiceCode = None,
                 stowage: 'Stowage' = None,
                 air_transport: 'AirTransport' = None,
                 road_transport: 'RoadTransport' = None,
                 rail_transport: 'RailTransport' = None,
                 maritime_transport: 'MaritimeTransport' = None,
                 owner_party: 'OwnerParty' = None,
                 measurement_dimension: List['MeasurementDimension'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.journey_id = journey_id
        self.registration_nationality_id = registration_nationality_id
        self.registration_nationality = registration_nationality
        self.direction_code = direction_code
        self.transport_means_type_code = transport_means_type_code
        self.trade_service_code = trade_service_code
        self.stowage = stowage
        self.air_transport = air_transport
        self.road_transport = road_transport
        self.rail_transport = rail_transport
        self.maritime_transport = maritime_transport
        self.owner_party = owner_party
        self.measurement_dimension = measurement_dimension


class __TransportScheduleType(PrefixCAC, ComplexXMLParseableObject):
    sequence_numeric = None
    status_location = None
    reference_date = None
    reference_time = None
    reliability_percent = None
    remarks = None
    actual_arrival_transport_event = None
    actual_departure_transport_event = None
    estimated_departure_transport_event = None
    estimated_arrival_transport_event = None
    planned_departure_transport_event = None
    planned_arrival_transport_event = None
    order_list = [
        'sequence_numeric',
        'reference_date',
        'reference_time',
        'reliability_percent',
        'remarks',
        'status_location',
        'actual_arrival_transport_event',
        'actual_departure_transport_event',
        'estimated_departure_transport_event',
        'estimated_arrival_transport_event',
        'planned_departure_transport_event',
        'planned_arrival_transport_event',
    ]

    def __init__(self,		sequence_numeric: cbc.SequenceNumeric,
                 status_location: 'StatusLocation',
                 reference_date: cbc.ReferenceDate = None,
                 reference_time: cbc.ReferenceTime = None,
                 reliability_percent: cbc.ReliabilityPercent = None,
                 remarks: List[cbc.Remarks] = None,
                 actual_arrival_transport_event: 'ActualArrivalTransportEvent' = None,
                 actual_departure_transport_event: 'ActualDepartureTransportEvent' = None,
                 estimated_departure_transport_event: 'EstimatedDepartureTransportEvent' = None,
                 estimated_arrival_transport_event: 'EstimatedArrivalTransportEvent' = None,
                 planned_departure_transport_event: 'PlannedDepartureTransportEvent' = None,
                 planned_arrival_transport_event: 'PlannedArrivalTransportEvent' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.sequence_numeric = sequence_numeric
        self.status_location = status_location
        self.reference_date = reference_date
        self.reference_time = reference_time
        self.reliability_percent = reliability_percent
        self.remarks = remarks
        self.actual_arrival_transport_event = actual_arrival_transport_event
        self.actual_departure_transport_event = actual_departure_transport_event
        self.estimated_departure_transport_event = estimated_departure_transport_event
        self.estimated_arrival_transport_event = estimated_arrival_transport_event
        self.planned_departure_transport_event = planned_departure_transport_event
        self.planned_arrival_transport_event = planned_arrival_transport_event


class __TransportationSegmentType(PrefixCAC, ComplexXMLParseableObject):
    sequence_numeric = None
    transportation_service = None
    transport_service_provider_party = None
    transport_execution_plan_reference_id = None
    referenced_consignment = None
    shipment_stage = None
    order_list = [
        'sequence_numeric',
        'transport_execution_plan_reference_id',
        'transportation_service',
        'transport_service_provider_party',
        'referenced_consignment',
        'shipment_stage',
    ]

    def __init__(self,		sequence_numeric: cbc.SequenceNumeric,
                 transportation_service: 'TransportationService',
                 transport_service_provider_party: 'TransportServiceProviderParty',
                 transport_execution_plan_reference_id: cbc.TransportExecutionPlanReferenceID = None,
                 referenced_consignment: 'ReferencedConsignment' = None,
                 shipment_stage: List['ShipmentStage'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.sequence_numeric = sequence_numeric
        self.transportation_service = transportation_service
        self.transport_service_provider_party = transport_service_provider_party
        self.transport_execution_plan_reference_id = transport_execution_plan_reference_id
        self.referenced_consignment = referenced_consignment
        self.shipment_stage = shipment_stage


class __TransportationServiceType(PrefixCAC, ComplexXMLParseableObject):
    transport_service_code = None
    tariff_class_code = None
    priority = None
    freight_rate_class_code = None
    transportation_service_description = None
    transportation_service_details_uri = None
    nomination_date = None
    nomination_time = None
    name = None
    sequence_numeric = None
    transport_equipment = None
    supported_transport_equipment = None
    unsupported_transport_equipment = None
    commodity_classification = None
    supported_commodity_classification = None
    unsupported_commodity_classification = None
    total_capacity_dimension = None
    shipment_stage = None
    transport_event = None
    responsible_transport_service_provider_party = None
    environmental_emission = None
    estimated_duration_period = None
    scheduled_service_frequency = None
    order_list = [
        'transport_service_code',
        'tariff_class_code',
        'priority',
        'freight_rate_class_code',
        'transportation_service_description',
        'transportation_service_details_uri',
        'nomination_date',
        'nomination_time',
        'name',
        'sequence_numeric',
        'transport_equipment',
        'supported_transport_equipment',
        'unsupported_transport_equipment',
        'commodity_classification',
        'supported_commodity_classification',
        'unsupported_commodity_classification',
        'total_capacity_dimension',
        'shipment_stage',
        'transport_event',
        'responsible_transport_service_provider_party',
        'environmental_emission',
        'estimated_duration_period',
        'scheduled_service_frequency',
    ]

    def __init__(self,		transport_service_code: cbc.TransportServiceCode,
                 tariff_class_code: cbc.TariffClassCode = None,
                 priority: cbc.Priority = None,
                 freight_rate_class_code: cbc.FreightRateClassCode = None,
                 transportation_service_description: List[cbc.TransportationServiceDescription] = None,
                 transportation_service_details_uri: cbc.TransportationServiceDetailsURI = None,
                 nomination_date: cbc.NominationDate = None,
                 nomination_time: cbc.NominationTime = None,
                 name: cbc.Name = None,
                 sequence_numeric: cbc.SequenceNumeric = None,
                 transport_equipment: List['TransportEquipment'] = None,
                 supported_transport_equipment: List['SupportedTransportEquipment'] = None,
                 unsupported_transport_equipment: List['UnsupportedTransportEquipment'] = None,
                 commodity_classification: List['CommodityClassification'] = None,
                 supported_commodity_classification: List['SupportedCommodityClassification'] = None,
                 unsupported_commodity_classification: List['UnsupportedCommodityClassification'] = None,
                 total_capacity_dimension: 'TotalCapacityDimension' = None,
                 shipment_stage: List['ShipmentStage'] = None,
                 transport_event: List['TransportEvent'] = None,
                 responsible_transport_service_provider_party: 'ResponsibleTransportServiceProviderParty' = None,
                 environmental_emission: List['EnvironmentalEmission'] = None,
                 estimated_duration_period: 'EstimatedDurationPeriod' = None,
                 scheduled_service_frequency: List['ScheduledServiceFrequency'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.transport_service_code = transport_service_code
        self.tariff_class_code = tariff_class_code
        self.priority = priority
        self.freight_rate_class_code = freight_rate_class_code
        self.transportation_service_description = transportation_service_description
        self.transportation_service_details_uri = transportation_service_details_uri
        self.nomination_date = nomination_date
        self.nomination_time = nomination_time
        self.name = name
        self.sequence_numeric = sequence_numeric
        self.transport_equipment = transport_equipment
        self.supported_transport_equipment = supported_transport_equipment
        self.unsupported_transport_equipment = unsupported_transport_equipment
        self.commodity_classification = commodity_classification
        self.supported_commodity_classification = supported_commodity_classification
        self.unsupported_commodity_classification = unsupported_commodity_classification
        self.total_capacity_dimension = total_capacity_dimension
        self.shipment_stage = shipment_stage
        self.transport_event = transport_event
        self.responsible_transport_service_provider_party = responsible_transport_service_provider_party
        self.environmental_emission = environmental_emission
        self.estimated_duration_period = estimated_duration_period
        self.scheduled_service_frequency = scheduled_service_frequency


class __UnstructuredPriceType(PrefixCAC, ComplexXMLParseableObject):
    price_amount = None
    time_amount = None
    order_list = [
        'price_amount',
        'time_amount',
    ]
    def __init__(self,		price_amount: cbc.PriceAmount = None,
                 time_amount: cbc.TimeAmount = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.price_amount = price_amount
        self.time_amount = time_amount


class __UtilityItemType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    subscriber_id = None
    subscriber_type = None
    subscriber_type_code = None
    description = None
    pack_quantity = None
    pack_size_numeric = None
    consumption_type = None
    consumption_type_code = None
    current_charge_type = None
    current_charge_type_code = None
    one_time_charge_type = None
    one_time_charge_type_code = None
    tax_category = None
    contract = None
    order_list = [
        'id_',
        'subscriber_id',
        'subscriber_type',
        'subscriber_type_code',
        'description',
        'pack_quantity',
        'pack_size_numeric',
        'consumption_type',
        'consumption_type_code',
        'current_charge_type',
        'current_charge_type_code',
        'one_time_charge_type',
        'one_time_charge_type_code',
        'tax_category',
        'contract',
    ]

    def __init__(self,		id_: cbc.ID,
                 subscriber_id: cbc.SubscriberID = None,
                 subscriber_type: cbc.SubscriberType = None,
                 subscriber_type_code: cbc.SubscriberTypeCode = None,
                 description: List[cbc.Description] = None,
                 pack_quantity: cbc.PackQuantity = None,
                 pack_size_numeric: cbc.PackSizeNumeric = None,
                 consumption_type: cbc.ConsumptionType = None,
                 consumption_type_code: cbc.ConsumptionTypeCode = None,
                 current_charge_type: cbc.CurrentChargeType = None,
                 current_charge_type_code: cbc.CurrentChargeTypeCode = None,
                 one_time_charge_type: cbc.OneTimeChargeType = None,
                 one_time_charge_type_code: cbc.OneTimeChargeTypeCode = None,
                 tax_category: 'TaxCategory' = None,
                 contract: 'Contract' = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.subscriber_id = subscriber_id
        self.subscriber_type = subscriber_type
        self.subscriber_type_code = subscriber_type_code
        self.description = description
        self.pack_quantity = pack_quantity
        self.pack_size_numeric = pack_size_numeric
        self.consumption_type = consumption_type
        self.consumption_type_code = consumption_type_code
        self.current_charge_type = current_charge_type
        self.current_charge_type_code = current_charge_type_code
        self.one_time_charge_type = one_time_charge_type
        self.one_time_charge_type_code = one_time_charge_type_code
        self.tax_category = tax_category
        self.contract = contract


class __WebSiteAccessType(PrefixCAC, ComplexXMLParseableObject):
    password = None
    login = None
    uri = None
    order_list = [
        'uri',
        'password',
        'login',
    ]

    def __init__(self,		password: cbc.Password,
                 login: cbc.Login,
                 uri: cbc.URI = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.password = password
        self.login = login
        self.uri = uri


class __WinningPartyType(PrefixCAC, ComplexXMLParseableObject):
    party = None
    rank = None
    order_list = [
        'rank',
        'party',
    ]
    def __init__(self,		party: 'Party',
                 rank: cbc.Rank = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.party = party
        self.rank = rank


class __WorkPhaseReferenceType(PrefixCAC, ComplexXMLParseableObject):
    id_ = None
    work_phase_code = None
    work_phase = None
    progress_percent = None
    start_date = None
    end_date = None
    work_order_document_reference = None
    order_list = [
        'id_',
        'work_phase_code',
        'work_phase',
        'progress_percent',
        'start_date',
        'end_date',
        'work_order_document_reference',
    ]

    def __init__(self,		id_: cbc.ID = None,
                 work_phase_code: cbc.WorkPhaseCode = None,
                 work_phase: List[cbc.WorkPhase] = None,
                 progress_percent: cbc.ProgressPercent = None,
                 start_date: cbc.StartDate = None,
                 end_date: cbc.EndDate = None,
                 work_order_document_reference: List['WorkOrderDocumentReference'] = None, xml_namespaces=None):
        super().__init__(xml_namespaces)
        self.id_ = id_
        self.work_phase_code = work_phase_code
        self.work_phase = work_phase
        self.progress_percent = progress_percent
        self.start_date = start_date
        self.end_date = end_date
        self.work_order_document_reference = work_order_document_reference
