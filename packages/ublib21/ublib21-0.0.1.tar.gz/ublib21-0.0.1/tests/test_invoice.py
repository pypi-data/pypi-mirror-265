import profile
import time
from ublib21.common import cbc, cac
from ublib21.validation.validation import InvoiceValidator
from ublib21.documents.invoice import Invoice

class TestAcceptedVariantsDescription:

    def test_value(self):
        ubl_version_id = cbc.UBLVersionID('UBL 2.1')
        customization_id = cbc.CustomizationID('05')
        profile_id = cbc.ProfileID('DIAN 2.1')
        profile_execution_id = cbc.ProfileExecutionID('2')
        id_ = cbc.ID('SETP990000002')
        uuid = cbc.UUID('941cf36af62dbbc06f105d2a80e9bfe683a90e84960eae4d351cc3afbe8f848c26c39bac4fbc80fa254824c6369ea694', scheme_id='2', scheme_name='CUFE-SHA384')
        issue_date = cbc.IssueDate('2019-03-20')
        issue_time = cbc.IssueTime('09:15:23-05:00')
        invoice_type_code = cbc.InvoiceTypeCode('01')
        note = cbc.Note('SETP9900000022019-06-2009:15:23-05:0012600.06012424.01040.00030.0014024.07900508908900108281fc8eac422eba16e22ffd8c6f94b3f40a6e38162c2')
        document_currency_code = cbc.DocumentCurrencyCode('COP', list_agency_id='6', list_agency_name='United Nations Economic Commission for Europe', list_id='ISO 4217 Alpha')
        line_count_numeric = cbc.LineCountNumeric('2')
        invoice_period = cac.InvoicePeriod(start_date=cbc.StartDate('2019-05-01'), end_date=cbc.EndDate('2019-05-30'))
        invoice_document_reference_1 = cac.InvoiceDocumentReference(
            id_ = cbc.ID('SFR3123856'),
            uuid = cbc.UUID('a675432fecc1d537361dcdbdfbd08d6e5283f2bc', scheme_name='CUFE-SHA1'),
            issue_date = cbc.IssueDate('2018-09-29'),
            document_description = cbc.DocumentDescription('Prepago recibido')
        )
        invoice_document_reference_2 = cac.InvoiceDocumentReference(
            id_ = cbc.ID('SETP990000101'),
            uuid = cbc.UUID('1dc661228f152332d876e1f1cd2042ecdea1804ed0da78f84dc9ee0938d69f17037dc53f97778ed2721d65c1fc3c73ac', scheme_name='CUFE-SHA384'),
            issue_date = cbc.IssueDate('2018-09-29'),
            document_description = cbc.DocumentDescription('Factura anterior')
        )
        billing_references = [
            cac.BillingReference(invoice_document_reference=invoice_document_reference_1),
            cac.BillingReference(invoice_document_reference=invoice_document_reference_2)
        ]
        

        accounting_supplier_party = cac.AccountingSupplierParty(
            additional_account_id=[cbc.AdditionalAccountID('1')],
            party = cac.Party(
                party_name = [
                    cac.PartyName(name=cbc.Name('Nombre Tienda')),
                    cac.PartyName(name=cbc.Name('Establecimiento Principal')),
                    cac.PartyName(name=cbc.Name('DIAN')),
                ],
                physical_location= cac.PhysicalLocation(
                    address = cac.Address(
                        id_ = cbc.ID('11001'),
                        city_name = cbc.CityName('Bogotá, D.c. '),
                        country_subentity= cbc.CountrySubentity('Bogotá'),
                        country_subentity_code= cbc.CountrySubentityCode('11'),
                        address_line=[cac.AddressLine(cbc.Line('Av. #97 - 13'))],
                        country=cac.Country(cbc.IdentificationCode('CO'), cbc.Name('Colombia', language_id='es'))
                    )
                ),
                party_tax_scheme=cac.PartyTaxScheme(
                    tax_scheme=cac.TaxScheme(cbc.ID('01'), cbc.Name('IVA')),
                    registration_name = cbc.RegistrationName('DIAN'),
                    company_id=cbc.CompanyID(
                        value='800197268', 
                        scheme_id='4', 
                        scheme_agency_id='195', 
                        scheme_agency_name='CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)',
                        scheme_name='31'
                    ),
                    tax_level_code = cbc.TaxLevelCode('0-99', list_name='05'),
                    registration_address= cac.RegistrationAddress(
                        id_ = cbc.ID('11001'),
                        city_name = cbc.CityName('Bogotá, D.c. '),
                        country_subentity= cbc.CountrySubentity('Bogotá'),
                        country_subentity_code= cbc.CountrySubentityCode('11'),
                        address_line=[cac.AddressLine(cbc.Line('Av. Jiménez #7 - 13'))],
                        country=cac.Country(cbc.IdentificationCode('CO'), cbc.Name('Colombia', language_id='es'))
                    )
                ),
                party_legal_entity=cac.PartyLegalEntity(
                    registration_name = cbc.RegistrationName('DIAN'),
                    company_id=cbc.CompanyID(
                        value='800197268', 
                        scheme_id='9', 
                        scheme_agency_id='195', 
                        scheme_agency_name='CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)',
                        scheme_name='31'
                    ),
                    corporate_registration_scheme=cac.CorporateRegistrationScheme(
                        id_=cbc.ID('SETP'),
                        name=cbc.Name('10181')
                    ),
                ),
                contact = cac.Contact(
                    name = cbc.Name('Eric Valencia'),
                    telephone= cbc.Telephone('6111111'),
                    electronic_mail= cbc.ElectronicMail('eric.valencia@ket.co'),
                    note= cbc.Note('Test descripcion contacto')
                )
            ),
        )

        accounting_customer_party = cac.AccountingCustomerParty(
            additional_account_id=[cbc.AdditionalAccountID('1')],
            party = cac.Party(
                party_name = [
                    cac.PartyName(name=cbc.Name('OPTICAS GMO COLOMBIA S A S'))
                ],
                physical_location= cac.PhysicalLocation(
                    address = cac.Address(
                        id_ = cbc.ID('11001'),
                        city_name = cbc.CityName('Bogotá, D.c. '),
                        country_subentity= cbc.CountrySubentity('Bogotá'),
                        country_subentity_code= cbc.CountrySubentityCode('11'),
                        address_line=[cac.AddressLine(cbc.Line('CARRERA 8 No 20-14/40'))],
                        country=cac.Country(cbc.IdentificationCode('CO'), cbc.Name('Colombia', language_id='es'))
                    )
                ),
                party_tax_scheme=cac.PartyTaxScheme(
                    tax_scheme=cac.TaxScheme(cbc.ID('01'), cbc.Name('IVA')),
                    registration_name = cbc.RegistrationName('OPTICAS GMO COLOMBIA S A S'),
                    company_id=cbc.CompanyID(
                        value='900108281', 
                        scheme_id='3', 
                        scheme_agency_id='195', 
                        scheme_agency_name='CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)',
                        scheme_name='31'
                    ),
                    tax_level_code = cbc.TaxLevelCode('0-99', list_name='04'),
                    registration_address= cac.RegistrationAddress(
                        id_ = cbc.ID('11001'),
                        city_name = cbc.CityName('Bogotá, D.c. '),
                        country_subentity= cbc.CountrySubentity('Bogotá'),
                        country_subentity_code= cbc.CountrySubentityCode('11'),
                        address_line=[cac.AddressLine(cbc.Line('CR 9 A N0 99 - 07 OF 802'))],
                        country=cac.Country(cbc.IdentificationCode('CO'), cbc.Name('Colombia', language_id='es'))
                    )
                ),
                party_legal_entity=cac.PartyLegalEntity(
                    registration_name = cbc.RegistrationName('OPTICAS GMO COLOMBIA S A S'),
                    company_id=cbc.CompanyID(
                        value='900108281', 
                        scheme_id='3', 
                        scheme_agency_id='195', 
                        scheme_agency_name='CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)',
                        scheme_name='31'
                    ),
                    corporate_registration_scheme=cac.CorporateRegistrationScheme(
                        name=cbc.Name('90518')
                    ),
                ),
                contact = cac.Contact(
                    name = cbc.Name('Diana Cruz'),
                    telephone= cbc.Telephone('31031031089'),
                    electronic_mail= cbc.ElectronicMail('dcruz@empresa.org'),
                )
            ),
        )
        legal_monetary_total = cac.LegalMonetaryTotal(
            payable_amount = cbc.PayableAmount(15024.07, 'COP'),
            line_extension_amount= cbc.LineExtensionAmount(12600.06, 'COP'),
            tax_exclusive_amount= cbc.TaxExclusiveAmount(12787.56, 'COP'),
            tax_inclusive_amount= cbc.TaxInclusiveAmount(15024.07, 'COP'),
            prepaid_amount= cbc.PrepaidAmount(1000.00, 'COP'),
        )
        invoice_lines = [
            cac.InvoiceLine(
                id_=cbc.ID('1'),
                invoiced_quantity=cbc.InvoicedQuantity('1.000000', unit_code='EA'),
                line_extension_amount=cbc.LineExtensionAmount(12600.06, currency_id='COP'),
                item = cac.Item(
                    description=cbc.Description('AV OASYS -2.25 (8.4) LENTE DE CONTATO'),
                    sellers_item_identification=cac.SellersItemIdentification(id_=cbc.ID('AOHV84-225')),
                    additional_item_identification=cac.AdditionalItemIdentification(id_=cbc.ID('6543542313534', scheme_id='99', scheme_name='EAN13'))
                ),
                price=cac.Price(
                    price_amount=cbc.PriceAmount(18900.00, 'COP'),
                    base_quantity=cbc.BaseQuantity('1.000000', unit_code='EA')
                    
                )
                
            )
        ]

        a = Invoice(
                id_=id_, 
                issue_date=issue_date, 
                accounting_supplier_party=accounting_supplier_party,
                accounting_customer_party=accounting_customer_party,
                legal_monetary_total=legal_monetary_total,
                invoice_line=invoice_lines,
                ubl_version_id=ubl_version_id,
                customization_id=customization_id,
                document_currency_code=document_currency_code,
                profile_id=profile_id,
                profile_execution_id=profile_execution_id,
                uuid=uuid,
                issue_time=issue_time,
                invoice_type_code=invoice_type_code,
                note=note,
                line_count_numeric=line_count_numeric,
                invoice_period=invoice_period
            )

        assert InvoiceValidator.validate(str(a))==True