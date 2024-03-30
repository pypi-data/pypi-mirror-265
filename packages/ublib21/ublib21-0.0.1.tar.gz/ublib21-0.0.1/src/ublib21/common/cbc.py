from ublib21.common.udt import IndicatorType
from ublib21.common.udt import TextType
from ublib21.common.udt import CodeType
from ublib21.common.udt import IdentifierType
from ublib21.common.udt import DateType
from ublib21.common.udt import TimeType
from ublib21.common.udt import QuantityType
from ublib21.common.udt import NameType
from ublib21.common.udt import AmountType
from ublib21.common.udt import PercentType
from ublib21.common.udt import MeasureType
from ublib21.common.udt import RateType
from ublib21.common.udt import NumericType
from ublib21.common.udt import BinaryObjectType

class PrefixCBC:
    prefix = 'cbc'


class AcceptedIndicator(PrefixCBC,IndicatorType):
    pass


class AcceptedVariantsDescription(PrefixCBC,TextType):
    pass


class AccountFormatCode(PrefixCBC,CodeType):
    pass


class AccountID(PrefixCBC,IdentifierType):
    pass


class AccountTypeCode(PrefixCBC,CodeType):
    pass


class AccountingCostCode(PrefixCBC,CodeType):
    pass


class AccountingCost(PrefixCBC,TextType):
    pass


class ActionCode(PrefixCBC,CodeType):
    pass


class ActivityTypeCode(PrefixCBC,CodeType):
    pass


class ActivityType(PrefixCBC,TextType):
    pass


class ActualDeliveryDate(PrefixCBC,DateType):
    pass


class ActualDeliveryTime(PrefixCBC,TimeType):
    pass


class ActualDespatchDate(PrefixCBC,DateType):
    pass


class ActualDespatchTime(PrefixCBC,TimeType):
    pass


class ActualPickupDate(PrefixCBC,DateType):
    pass


class ActualPickupTime(PrefixCBC,TimeType):
    pass


class ActualTemperatureReductionQuantity(PrefixCBC,QuantityType):
    pass


class AdValoremIndicator(PrefixCBC,IndicatorType):
    pass


class AdditionalAccountID(PrefixCBC,IdentifierType):
    pass


class AdditionalConditions(PrefixCBC,TextType):
    pass


class AdditionalInformation(PrefixCBC,TextType):
    pass


class AdditionalStreetName(PrefixCBC,NameType):
    pass


class AddressFormatCode(PrefixCBC,CodeType):
    pass


class AddressTypeCode(PrefixCBC,CodeType):
    pass


class AdjustmentReasonCode(PrefixCBC,CodeType):
    pass


class AdmissionCode(PrefixCBC,CodeType):
    pass


class AdvertisementAmount(PrefixCBC,AmountType):
    pass


class AgencyID(PrefixCBC,IdentifierType):
    pass


class AgencyName(PrefixCBC,TextType):
    pass


class AirFlowPercent(PrefixCBC,PercentType):
    pass


class AircraftID(PrefixCBC,IdentifierType):
    pass


class AliasName(PrefixCBC,NameType):
    pass


class AllowanceChargeReasonCode(PrefixCBC,CodeType):
    pass


class AllowanceChargeReason(PrefixCBC,TextType):
    pass


class AllowanceTotalAmount(PrefixCBC,AmountType):
    pass


class AltitudeMeasure(PrefixCBC,MeasureType):
    pass


class AmountRate(PrefixCBC,RateType):
    pass


class Amount(PrefixCBC,AmountType):
    pass


class AnimalFoodApprovedIndicator(PrefixCBC,IndicatorType):
    pass


class AnimalFoodIndicator(PrefixCBC,IndicatorType):
    pass


class AnnualAverageAmount(PrefixCBC,AmountType):
    pass


class ApplicationStatusCode(PrefixCBC,CodeType):
    pass


class ApprovalDate(PrefixCBC,DateType):
    pass


class ApprovalStatus(PrefixCBC,TextType):
    pass


class AttributeID(PrefixCBC,IdentifierType):
    pass


class AuctionConstraintIndicator(PrefixCBC,IndicatorType):
    pass


class AuctionURI(PrefixCBC,IdentifierType):
    pass


class AvailabilityDate(PrefixCBC,DateType):
    pass


class AvailabilityStatusCode(PrefixCBC,CodeType):
    pass


class AverageAmount(PrefixCBC,AmountType):
    pass


class AverageSubsequentContractAmount(PrefixCBC,AmountType):
    pass


class AwardDate(PrefixCBC,DateType):
    pass


class AwardTime(PrefixCBC,TimeType):
    pass


class AwardingCriterionDescription(PrefixCBC,TextType):
    pass


class AwardingCriterionID(PrefixCBC,IdentifierType):
    pass


class AwardingCriterionTypeCode(PrefixCBC,CodeType):
    pass


class AwardingMethodTypeCode(PrefixCBC,CodeType):
    pass


class BackOrderAllowedIndicator(PrefixCBC,IndicatorType):
    pass


class BackorderQuantity(PrefixCBC,QuantityType):
    pass


class BackorderReason(PrefixCBC,TextType):
    pass


class BalanceAmount(PrefixCBC,AmountType):
    pass


class BalanceBroughtForwardIndicator(PrefixCBC,IndicatorType):
    pass


class BarcodeSymbologyID(PrefixCBC,IdentifierType):
    pass


class BaseAmount(PrefixCBC,AmountType):
    pass


class BaseQuantity(PrefixCBC,QuantityType):
    pass


class BaseUnitMeasure(PrefixCBC,MeasureType):
    pass


class BasedOnConsensusIndicator(PrefixCBC,IndicatorType):
    pass


class BasicConsumedQuantity(PrefixCBC,QuantityType):
    pass


class BatchQuantity(PrefixCBC,QuantityType):
    pass


class BestBeforeDate(PrefixCBC,DateType):
    pass


class BindingOnBuyerIndicator(PrefixCBC,IndicatorType):
    pass


class BirthDate(PrefixCBC,DateType):
    pass


class BirthplaceName(PrefixCBC,TextType):
    pass


class BlockName(PrefixCBC,NameType):
    pass


class BrandName(PrefixCBC,NameType):
    pass


class BrokerAssignedID(PrefixCBC,IdentifierType):
    pass


class BudgetYearNumeric(PrefixCBC,NumericType):
    pass


class BuildingName(PrefixCBC,NameType):
    pass


class BuildingNumber(PrefixCBC,TextType):
    pass


class BulkCargoIndicator(PrefixCBC,IndicatorType):
    pass


class BusinessClassificationEvidenceID(PrefixCBC,IdentifierType):
    pass


class BusinessIdentityEvidenceID(PrefixCBC,IdentifierType):
    pass


class BuyerEventID(PrefixCBC,IdentifierType):
    pass


class BuyerProfileURI(PrefixCBC,IdentifierType):
    pass


class BuyerReference(PrefixCBC,TextType):
    pass


class CV2ID(PrefixCBC,IdentifierType):
    pass


class CalculationExpressionCode(PrefixCBC,CodeType):
    pass


class CalculationExpression(PrefixCBC,TextType):
    pass


class CalculationMethodCode(PrefixCBC,CodeType):
    pass


class CalculationRate(PrefixCBC,RateType):
    pass


class CalculationSequenceNumeric(PrefixCBC,NumericType):
    pass


class CallBaseAmount(PrefixCBC,AmountType):
    pass


class CallDate(PrefixCBC,DateType):
    pass


class CallExtensionAmount(PrefixCBC,AmountType):
    pass


class CallTime(PrefixCBC,TimeType):
    pass


class CancellationNote(PrefixCBC,TextType):
    pass


class CandidateReductionConstraintIndicator(PrefixCBC,IndicatorType):
    pass


class CandidateStatement(PrefixCBC,TextType):
    pass


class CanonicalizationMethod(PrefixCBC,TextType):
    pass


class CapabilityTypeCode(PrefixCBC,CodeType):
    pass


class CardChipCode(PrefixCBC,CodeType):
    pass


class CardTypeCode(PrefixCBC,CodeType):
    pass


class CargoTypeCode(PrefixCBC,CodeType):
    pass


class CarrierAssignedID(PrefixCBC,IdentifierType):
    pass


class CarrierServiceInstructions(PrefixCBC,TextType):
    pass


class CatalogueIndicator(PrefixCBC,IndicatorType):
    pass


class CategoryName(PrefixCBC,NameType):
    pass


class CertificateTypeCode(PrefixCBC,CodeType):
    pass


class CertificateType(PrefixCBC,TextType):
    pass


class ChangeConditions(PrefixCBC,TextType):
    pass


class ChannelCode(PrefixCBC,CodeType):
    pass


class Channel(PrefixCBC,TextType):
    pass


class CharacterSetCode(PrefixCBC,CodeType):
    pass


class Characteristics(PrefixCBC,TextType):
    pass


class ChargeIndicator(PrefixCBC,IndicatorType):
    pass


class ChargeTotalAmount(PrefixCBC,AmountType):
    pass


class ChargeableQuantity(PrefixCBC,QuantityType):
    pass


class ChargeableWeightMeasure(PrefixCBC,MeasureType):
    pass


class ChildConsignmentQuantity(PrefixCBC,QuantityType):
    pass


class ChipApplicationID(PrefixCBC,IdentifierType):
    pass


class CityName(PrefixCBC,NameType):
    pass


class CitySubdivisionName(PrefixCBC,NameType):
    pass


class CodeValue(PrefixCBC,TextType):
    pass


class CollaborationPriorityCode(PrefixCBC,CodeType):
    pass


class Comment(PrefixCBC,TextType):
    pass


class CommodityCode(PrefixCBC,CodeType):
    pass


class CompanyID(PrefixCBC,IdentifierType):
    pass


class CompanyLegalFormCode(PrefixCBC,CodeType):
    pass


class CompanyLegalForm(PrefixCBC,TextType):
    pass


class CompanyLiquidationStatusCode(PrefixCBC,CodeType):
    pass


class ComparedValueMeasure(PrefixCBC,MeasureType):
    pass


class ComparisonDataCode(PrefixCBC,CodeType):
    pass


class ComparisonDataSourceCode(PrefixCBC,CodeType):
    pass


class ComparisonForecastIssueDate(PrefixCBC,DateType):
    pass


class ComparisonForecastIssueTime(PrefixCBC,TimeType):
    pass


class CompletionIndicator(PrefixCBC,IndicatorType):
    pass


class ConditionCode(PrefixCBC,CodeType):
    pass


class Condition(PrefixCBC,TextType):
    pass


class ConditionsDescription(PrefixCBC,TextType):
    pass


class Conditions(PrefixCBC,TextType):
    pass


class ConsigneeAssignedID(PrefixCBC,IdentifierType):
    pass


class ConsignmentQuantity(PrefixCBC,QuantityType):
    pass


class ConsignorAssignedID(PrefixCBC,IdentifierType):
    pass


class ConsolidatableIndicator(PrefixCBC,IndicatorType):
    pass


class ConstitutionCode(PrefixCBC,CodeType):
    pass


class ConsumerIncentiveTacticTypeCode(PrefixCBC,CodeType):
    pass


class ConsumerUnitQuantity(PrefixCBC,QuantityType):
    pass


class ConsumersEnergyLevelCode(PrefixCBC,CodeType):
    pass


class ConsumersEnergyLevel(PrefixCBC,TextType):
    pass


class ConsumptionEnergyQuantity(PrefixCBC,QuantityType):
    pass


class ConsumptionID(PrefixCBC,IdentifierType):
    pass


class ConsumptionLevelCode(PrefixCBC,CodeType):
    pass


class ConsumptionLevel(PrefixCBC,TextType):
    pass


class ConsumptionReportID(PrefixCBC,IdentifierType):
    pass


class ConsumptionTypeCode(PrefixCBC,CodeType):
    pass


class ConsumptionType(PrefixCBC,TextType):
    pass


class ConsumptionWaterQuantity(PrefixCBC,QuantityType):
    pass


class ContainerizedIndicator(PrefixCBC,IndicatorType):
    pass


class Content(PrefixCBC,TextType):
    pass


class ContentUnitQuantity(PrefixCBC,QuantityType):
    pass


class ContractFolderID(PrefixCBC,IdentifierType):
    pass


class ContractName(PrefixCBC,TextType):
    pass


class ContractSubdivision(PrefixCBC,TextType):
    pass


class ContractTypeCode(PrefixCBC,CodeType):
    pass


class ContractType(PrefixCBC,TextType):
    pass


class ContractedCarrierAssignedID(PrefixCBC,IdentifierType):
    pass


class ContractingSystemCode(PrefixCBC,CodeType):
    pass


class CoordinateSystemCode(PrefixCBC,CodeType):
    pass


class CopyIndicator(PrefixCBC,IndicatorType):
    pass


class CorporateRegistrationTypeCode(PrefixCBC,CodeType):
    pass


class CorporateStockAmount(PrefixCBC,AmountType):
    pass


class CorrectionAmount(PrefixCBC,AmountType):
    pass


class CorrectionTypeCode(PrefixCBC,CodeType):
    pass


class CorrectionType(PrefixCBC,TextType):
    pass


class CorrectionUnitAmount(PrefixCBC,AmountType):
    pass


class CountrySubentityCode(PrefixCBC,CodeType):
    pass


class CountrySubentity(PrefixCBC,TextType):
    pass


class CreditLineAmount(PrefixCBC,AmountType):
    pass


class CreditNoteTypeCode(PrefixCBC,CodeType):
    pass


class CreditedQuantity(PrefixCBC,QuantityType):
    pass


class CrewQuantity(PrefixCBC,QuantityType):
    pass


class CurrencyCode(PrefixCBC,CodeType):
    pass


class CurrentChargeTypeCode(PrefixCBC,CodeType):
    pass


class CurrentChargeType(PrefixCBC,TextType):
    pass


class CustomerAssignedAccountID(PrefixCBC,IdentifierType):
    pass


class CustomerReference(PrefixCBC,TextType):
    pass


class CustomizationID(PrefixCBC,IdentifierType):
    pass


class CustomsClearanceServiceInstructions(PrefixCBC,TextType):
    pass


class CustomsImportClassifiedIndicator(PrefixCBC,IndicatorType):
    pass


class CustomsStatusCode(PrefixCBC,CodeType):
    pass


class CustomsTariffQuantity(PrefixCBC,QuantityType):
    pass


class DamageRemarks(PrefixCBC,TextType):
    pass


class DangerousGoodsApprovedIndicator(PrefixCBC,IndicatorType):
    pass


class DataSendingCapability(PrefixCBC,TextType):
    pass


class DataSourceCode(PrefixCBC,CodeType):
    pass


class Date(PrefixCBC,DateType):
    pass


class DebitLineAmount(PrefixCBC,AmountType):
    pass


class DebitedQuantity(PrefixCBC,QuantityType):
    pass


class DeclarationTypeCode(PrefixCBC,CodeType):
    pass


class DeclaredCarriageValueAmount(PrefixCBC,AmountType):
    pass


class DeclaredCustomsValueAmount(PrefixCBC,AmountType):
    pass


class DeclaredForCarriageValueAmount(PrefixCBC,AmountType):
    pass


class DeclaredStatisticsValueAmount(PrefixCBC,AmountType):
    pass


class DeliveredQuantity(PrefixCBC,QuantityType):
    pass


class DeliveryInstructions(PrefixCBC,TextType):
    pass


class DemurrageInstructions(PrefixCBC,TextType):
    pass


class Department(PrefixCBC,TextType):
    pass


class DescriptionCode(PrefixCBC,CodeType):
    pass


class Description(PrefixCBC,TextType):
    pass


class DespatchAdviceTypeCode(PrefixCBC,CodeType):
    pass


class DifferenceTemperatureReductionQuantity(PrefixCBC,QuantityType):
    pass


class DirectionCode(PrefixCBC,CodeType):
    pass


class DisplayTacticTypeCode(PrefixCBC,CodeType):
    pass


class DispositionCode(PrefixCBC,CodeType):
    pass


class District(PrefixCBC,TextType):
    pass


class DocumentCurrencyCode(PrefixCBC,CodeType):
    pass


class DocumentDescription(PrefixCBC,TextType):
    pass


class DocumentHash(PrefixCBC,TextType):
    pass


class DocumentID(PrefixCBC,IdentifierType):
    pass


class DocumentStatusCode(PrefixCBC,CodeType):
    pass


class DocumentStatusReasonCode(PrefixCBC,CodeType):
    pass


class DocumentStatusReasonDescription(PrefixCBC,TextType):
    pass


class DocumentTypeCode(PrefixCBC,CodeType):
    pass


class DocumentType(PrefixCBC,TextType):
    pass


class DocumentationFeeAmount(PrefixCBC,AmountType):
    pass


class DueDate(PrefixCBC,DateType):
    pass


class DurationMeasure(PrefixCBC,MeasureType):
    pass


class DutyCode(PrefixCBC,CodeType):
    pass


class Duty(PrefixCBC,TextType):
    pass


class EarliestPickupDate(PrefixCBC,DateType):
    pass


class EarliestPickupTime(PrefixCBC,TimeType):
    pass


class EconomicOperatorRegistryURI(PrefixCBC,IdentifierType):
    pass


class EffectiveDate(PrefixCBC,DateType):
    pass


class EffectiveTime(PrefixCBC,TimeType):
    pass


class ElectronicDeviceDescription(PrefixCBC,TextType):
    pass


class ElectronicMail(PrefixCBC,TextType):
    pass


class EmbeddedDocumentBinaryObject(PrefixCBC,BinaryObjectType):
    pass


class EmergencyProceduresCode(PrefixCBC,CodeType):
    pass


class EmployeeQuantity(PrefixCBC,QuantityType):
    pass


class EncodingCode(PrefixCBC,CodeType):
    pass


class EndDate(PrefixCBC,DateType):
    pass


class EndTime(PrefixCBC,TimeType):
    pass


class EndpointID(PrefixCBC,IdentifierType):
    pass


class EnvironmentalEmissionTypeCode(PrefixCBC,CodeType):
    pass


class EstimatedAmount(PrefixCBC,AmountType):
    pass


class EstimatedConsumedQuantity(PrefixCBC,QuantityType):
    pass


class EstimatedDeliveryDate(PrefixCBC,DateType):
    pass


class EstimatedDeliveryTime(PrefixCBC,TimeType):
    pass


class EstimatedDespatchDate(PrefixCBC,DateType):
    pass


class EstimatedDespatchTime(PrefixCBC,TimeType):
    pass


class EstimatedOverallContractAmount(PrefixCBC,AmountType):
    pass


class EstimatedOverallContractQuantity(PrefixCBC,QuantityType):
    pass


class EvaluationCriterionTypeCode(PrefixCBC,CodeType):
    pass


class EvidenceTypeCode(PrefixCBC,CodeType):
    pass


class ExceptionResolutionCode(PrefixCBC,CodeType):
    pass


class ExceptionStatusCode(PrefixCBC,CodeType):
    pass


class ExchangeMarketID(PrefixCBC,IdentifierType):
    pass


class ExclusionReason(PrefixCBC,TextType):
    pass


class ExecutionRequirementCode(PrefixCBC,CodeType):
    pass


class ExemptionReasonCode(PrefixCBC,CodeType):
    pass


class ExemptionReason(PrefixCBC,TextType):
    pass


class ExpectedOperatorQuantity(PrefixCBC,QuantityType):
    pass


class ExpectedQuantity(PrefixCBC,QuantityType):
    pass


class ExpenseCode(PrefixCBC,CodeType):
    pass


class ExpiryDate(PrefixCBC,DateType):
    pass


class ExpiryTime(PrefixCBC,TimeType):
    pass


class ExpressionCode(PrefixCBC,CodeType):
    pass


class Expression(PrefixCBC,TextType):
    pass


class ExtendedID(PrefixCBC,IdentifierType):
    pass


class Extension(PrefixCBC,TextType):
    pass


class FaceValueAmount(PrefixCBC,AmountType):
    pass


class FamilyName(PrefixCBC,NameType):
    pass


class FeatureTacticTypeCode(PrefixCBC,CodeType):
    pass


class FeeAmount(PrefixCBC,AmountType):
    pass


class FeeDescription(PrefixCBC,TextType):
    pass


class FileName(PrefixCBC,NameType):
    pass


class FinancingInstrumentCode(PrefixCBC,CodeType):
    pass


class FirstName(PrefixCBC,NameType):
    pass


class FirstShipmentAvailibilityDate(PrefixCBC,DateType):
    pass


class Floor(PrefixCBC,TextType):
    pass


class FollowupContractIndicator(PrefixCBC,IndicatorType):
    pass


class ForecastPurposeCode(PrefixCBC,CodeType):
    pass


class ForecastTypeCode(PrefixCBC,CodeType):
    pass


class FormatCode(PrefixCBC,CodeType):
    pass


class ForwarderServiceInstructions(PrefixCBC,TextType):
    pass


class FreeOfChargeIndicator(PrefixCBC,IndicatorType):
    pass


class FreeOnBoardValueAmount(PrefixCBC,AmountType):
    pass


class FreightForwarderAssignedID(PrefixCBC,IdentifierType):
    pass


class FreightRateClassCode(PrefixCBC,CodeType):
    pass


class Frequency(PrefixCBC,TextType):
    pass


class FrozenDocumentIndicator(PrefixCBC,IndicatorType):
    pass


class FrozenPeriodDaysNumeric(PrefixCBC,NumericType):
    pass


class FullnessIndicationCode(PrefixCBC,CodeType):
    pass


class FullyPaidSharesIndicator(PrefixCBC,IndicatorType):
    pass


class FundingProgramCode(PrefixCBC,CodeType):
    pass


class FundingProgram(PrefixCBC,TextType):
    pass


class GasPressureQuantity(PrefixCBC,QuantityType):
    pass


class GenderCode(PrefixCBC,CodeType):
    pass


class GeneralCargoIndicator(PrefixCBC,IndicatorType):
    pass


class GovernmentAgreementConstraintIndicator(PrefixCBC,IndicatorType):
    pass


class GrossTonnageMeasure(PrefixCBC,MeasureType):
    pass


class GrossVolumeMeasure(PrefixCBC,MeasureType):
    pass


class GrossWeightMeasure(PrefixCBC,MeasureType):
    pass


class GuaranteeTypeCode(PrefixCBC,CodeType):
    pass


class GuaranteedDespatchDate(PrefixCBC,DateType):
    pass


class GuaranteedDespatchTime(PrefixCBC,TimeType):
    pass


class HandlingCode(PrefixCBC,CodeType):
    pass


class HandlingInstructions(PrefixCBC,TextType):
    pass


class HashAlgorithmMethod(PrefixCBC,TextType):
    pass


class HaulageInstructions(PrefixCBC,TextType):
    pass


class HazardClassID(PrefixCBC,IdentifierType):
    pass


class HazardousCategoryCode(PrefixCBC,CodeType):
    pass


class HazardousRegulationCode(PrefixCBC,CodeType):
    pass


class HazardousRiskIndicator(PrefixCBC,IndicatorType):
    pass


class HeatingTypeCode(PrefixCBC,CodeType):
    pass


class HeatingType(PrefixCBC,TextType):
    pass


class HigherTenderAmount(PrefixCBC,AmountType):
    pass


class HolderName(PrefixCBC,NameType):
    pass


class HumanFoodApprovedIndicator(PrefixCBC,IndicatorType):
    pass


class HumanFoodIndicator(PrefixCBC,IndicatorType):
    pass


class HumidityPercent(PrefixCBC,PercentType):
    pass


class ID(PrefixCBC,IdentifierType):
    pass


class IdentificationCode(PrefixCBC,CodeType):
    pass


class IdentificationID(PrefixCBC,IdentifierType):
    pass


class ImmobilizationCertificateID(PrefixCBC,IdentifierType):
    pass


class ImportanceCode(PrefixCBC,CodeType):
    pass


class IndicationIndicator(PrefixCBC,IndicatorType):
    pass


class IndustryClassificationCode(PrefixCBC,CodeType):
    pass


class Information(PrefixCBC,TextType):
    pass


class InformationURI(PrefixCBC,IdentifierType):
    pass


class InhalationToxicityZoneCode(PrefixCBC,CodeType):
    pass


class InhouseMail(PrefixCBC,TextType):
    pass


class InspectionMethodCode(PrefixCBC,CodeType):
    pass


class InstallmentDueDate(PrefixCBC,DateType):
    pass


class InstructionID(PrefixCBC,IdentifierType):
    pass


class InstructionNote(PrefixCBC,TextType):
    pass


class Instructions(PrefixCBC,TextType):
    pass


class InsurancePremiumAmount(PrefixCBC,AmountType):
    pass


class InsuranceValueAmount(PrefixCBC,AmountType):
    pass


class InventoryValueAmount(PrefixCBC,AmountType):
    pass


class InvoiceTypeCode(PrefixCBC,CodeType):
    pass


class InvoicedQuantity(PrefixCBC,QuantityType):
    pass


class InvoicingPartyReference(PrefixCBC,TextType):
    pass


class IssueDate(PrefixCBC,DateType):
    pass


class IssueNumberID(PrefixCBC,IdentifierType):
    pass


class IssueTime(PrefixCBC,TimeType):
    pass


class IssuerID(PrefixCBC,IdentifierType):
    pass


class ItemClassificationCode(PrefixCBC,CodeType):
    pass


class ItemUpdateRequestIndicator(PrefixCBC,IndicatorType):
    pass


class JobTitle(PrefixCBC,TextType):
    pass


class JourneyID(PrefixCBC,IdentifierType):
    pass


class JustificationDescription(PrefixCBC,TextType):
    pass


class Justification(PrefixCBC,TextType):
    pass


class Keyword(PrefixCBC,TextType):
    pass


class LanguageID(PrefixCBC,IdentifierType):
    pass


class LastRevisionDate(PrefixCBC,DateType):
    pass


class LastRevisionTime(PrefixCBC,TimeType):
    pass


class LatestDeliveryDate(PrefixCBC,DateType):
    pass


class LatestDeliveryTime(PrefixCBC,TimeType):
    pass


class LatestMeterQuantity(PrefixCBC,QuantityType):
    pass


class LatestMeterReadingDate(PrefixCBC,DateType):
    pass


class LatestMeterReadingMethodCode(PrefixCBC,CodeType):
    pass


class LatestMeterReadingMethod(PrefixCBC,TextType):
    pass


class LatestPickupDate(PrefixCBC,DateType):
    pass


class LatestPickupTime(PrefixCBC,TimeType):
    pass


class LatestProposalAcceptanceDate(PrefixCBC,DateType):
    pass


class LatestSecurityClearanceDate(PrefixCBC,DateType):
    pass


class LatitudeDegreesMeasure(PrefixCBC,MeasureType):
    pass


class LatitudeDirectionCode(PrefixCBC,CodeType):
    pass


class LatitudeMinutesMeasure(PrefixCBC,MeasureType):
    pass


class LeadTimeMeasure(PrefixCBC,MeasureType):
    pass


class LegalReference(PrefixCBC,TextType):
    pass


class LegalStatusIndicator(PrefixCBC,IndicatorType):
    pass


class LiabilityAmount(PrefixCBC,AmountType):
    pass


class LicensePlateID(PrefixCBC,IdentifierType):
    pass


class LifeCycleStatusCode(PrefixCBC,CodeType):
    pass


class LimitationDescription(PrefixCBC,TextType):
    pass


class LineCountNumeric(PrefixCBC,NumericType):
    pass


class LineExtensionAmount(PrefixCBC,AmountType):
    pass


class LineID(PrefixCBC,IdentifierType):
    pass


class LineNumberNumeric(PrefixCBC,NumericType):
    pass


class LineStatusCode(PrefixCBC,CodeType):
    pass


class Line(PrefixCBC,TextType):
    pass


class ListValue(PrefixCBC,TextType):
    pass


class LivestockIndicator(PrefixCBC,IndicatorType):
    pass


class LoadingLengthMeasure(PrefixCBC,MeasureType):
    pass


class LoadingSequenceID(PrefixCBC,IdentifierType):
    pass


class LocaleCode(PrefixCBC,CodeType):
    pass


class LocationID(PrefixCBC,IdentifierType):
    pass


class Location(PrefixCBC,TextType):
    pass


class LocationTypeCode(PrefixCBC,CodeType):
    pass


class Login(PrefixCBC,TextType):
    pass


class LogoReferenceID(PrefixCBC,IdentifierType):
    pass


class LongitudeDegreesMeasure(PrefixCBC,MeasureType):
    pass


class LongitudeDirectionCode(PrefixCBC,CodeType):
    pass


class LongitudeMinutesMeasure(PrefixCBC,MeasureType):
    pass


class LossRiskResponsibilityCode(PrefixCBC,CodeType):
    pass


class LossRisk(PrefixCBC,TextType):
    pass


class LotNumberID(PrefixCBC,IdentifierType):
    pass


class LowTendersDescription(PrefixCBC,TextType):
    pass


class LowerOrangeHazardPlacardID(PrefixCBC,IdentifierType):
    pass


class LowerTenderAmount(PrefixCBC,AmountType):
    pass


class MandateTypeCode(PrefixCBC,CodeType):
    pass


class ManufactureDate(PrefixCBC,DateType):
    pass


class ManufactureTime(PrefixCBC,TimeType):
    pass


class MarkAttentionIndicator(PrefixCBC,IndicatorType):
    pass


class MarkAttention(PrefixCBC,TextType):
    pass


class MarkCareIndicator(PrefixCBC,IndicatorType):
    pass


class MarkCare(PrefixCBC,TextType):
    pass


class MarketValueAmount(PrefixCBC,AmountType):
    pass


class MarkingID(PrefixCBC,IdentifierType):
    pass


class MathematicOperatorCode(PrefixCBC,CodeType):
    pass


class MaximumAdvertisementAmount(PrefixCBC,AmountType):
    pass


class MaximumAmount(PrefixCBC,AmountType):
    pass


class MaximumBackorderQuantity(PrefixCBC,QuantityType):
    pass


class MaximumCopiesNumeric(PrefixCBC,NumericType):
    pass


class MaximumMeasure(PrefixCBC,MeasureType):
    pass


class MaximumNumberNumeric(PrefixCBC,NumericType):
    pass


class MaximumOperatorQuantity(PrefixCBC,QuantityType):
    pass


class MaximumOrderQuantity(PrefixCBC,QuantityType):
    pass


class MaximumPaidAmount(PrefixCBC,AmountType):
    pass


class MaximumPaymentInstructionsNumeric(PrefixCBC,NumericType):
    pass


class MaximumPercent(PrefixCBC,PercentType):
    pass


class MaximumQuantity(PrefixCBC,QuantityType):
    pass


class MaximumValue(PrefixCBC,TextType):
    pass


class MaximumVariantQuantity(PrefixCBC,QuantityType):
    pass


class Measure(PrefixCBC,MeasureType):
    pass


class MedicalFirstAidGuideCode(PrefixCBC,CodeType):
    pass


class MeterConstantCode(PrefixCBC,CodeType):
    pass


class MeterConstant(PrefixCBC,TextType):
    pass


class MeterName(PrefixCBC,TextType):
    pass


class MeterNumber(PrefixCBC,TextType):
    pass


class MeterReadingComments(PrefixCBC,TextType):
    pass


class MeterReadingTypeCode(PrefixCBC,CodeType):
    pass


class MeterReadingType(PrefixCBC,TextType):
    pass


class MiddleName(PrefixCBC,NameType):
    pass


class MimeCode(PrefixCBC,CodeType):
    pass


class MinimumAmount(PrefixCBC,AmountType):
    pass


class MinimumBackorderQuantity(PrefixCBC,QuantityType):
    pass


class MinimumImprovementBid(PrefixCBC,TextType):
    pass


class MinimumInventoryQuantity(PrefixCBC,QuantityType):
    pass


class MinimumMeasure(PrefixCBC,MeasureType):
    pass


class MinimumNumberNumeric(PrefixCBC,NumericType):
    pass


class MinimumOrderQuantity(PrefixCBC,QuantityType):
    pass


class MinimumPercent(PrefixCBC,PercentType):
    pass


class MinimumQuantity(PrefixCBC,QuantityType):
    pass


class MinimumValue(PrefixCBC,TextType):
    pass


class MiscellaneousEventTypeCode(PrefixCBC,CodeType):
    pass


class ModelName(PrefixCBC,NameType):
    pass


class MonetaryScope(PrefixCBC,TextType):
    pass


class MovieTitle(PrefixCBC,TextType):
    pass


class MultipleOrderQuantity(PrefixCBC,QuantityType):
    pass


class MultiplierFactorNumeric(PrefixCBC,NumericType):
    pass


class NameCode(PrefixCBC,CodeType):
    pass


class NameSuffix(PrefixCBC,TextType):
    pass


class Name(PrefixCBC,NameType):
    pass


class NationalityID(PrefixCBC,IdentifierType):
    pass


class NatureCode(PrefixCBC,CodeType):
    pass


class NegotiationDescription(PrefixCBC,TextType):
    pass


class NetNetWeightMeasure(PrefixCBC,MeasureType):
    pass


class NetTonnageMeasure(PrefixCBC,MeasureType):
    pass


class NetVolumeMeasure(PrefixCBC,MeasureType):
    pass


class NetWeightMeasure(PrefixCBC,MeasureType):
    pass


class NetworkID(PrefixCBC,IdentifierType):
    pass


class NominationDate(PrefixCBC,DateType):
    pass


class NominationTime(PrefixCBC,TimeType):
    pass


class NormalTemperatureReductionQuantity(PrefixCBC,QuantityType):
    pass


class Note(PrefixCBC,TextType):
    pass


class NotificationTypeCode(PrefixCBC,CodeType):
    pass


class OccurrenceDate(PrefixCBC,DateType):
    pass


class OccurrenceTime(PrefixCBC,TimeType):
    pass


class OnCarriageIndicator(PrefixCBC,IndicatorType):
    pass


class OneTimeChargeTypeCode(PrefixCBC,CodeType):
    pass


class OneTimeChargeType(PrefixCBC,TextType):
    pass


class OntologyURI(PrefixCBC,IdentifierType):
    pass


class OpenTenderID(PrefixCBC,IdentifierType):
    pass


class OperatingYearsQuantity(PrefixCBC,QuantityType):
    pass


class OptionalLineItemIndicator(PrefixCBC,IndicatorType):
    pass


class OptionsDescription(PrefixCBC,TextType):
    pass


class OrderIntervalDaysNumeric(PrefixCBC,NumericType):
    pass


class OrderQuantityIncrementNumeric(PrefixCBC,NumericType):
    pass


class OrderResponseCode(PrefixCBC,CodeType):
    pass


class OrderTypeCode(PrefixCBC,CodeType):
    pass


class OrderableIndicator(PrefixCBC,IndicatorType):
    pass


class OrderableUnitFactorRate(PrefixCBC,RateType):
    pass


class OrderableUnit(PrefixCBC,TextType):
    pass


class OrganizationDepartment(PrefixCBC,TextType):
    pass


class OriginalContractingSystemID(PrefixCBC,IdentifierType):
    pass


class OriginalJobID(PrefixCBC,IdentifierType):
    pass


class OtherConditionsIndicator(PrefixCBC,IndicatorType):
    pass


class OtherInstruction(PrefixCBC,TextType):
    pass


class OtherName(PrefixCBC,NameType):
    pass


class OutstandingQuantity(PrefixCBC,QuantityType):
    pass


class OutstandingReason(PrefixCBC,TextType):
    pass


class OversupplyQuantity(PrefixCBC,QuantityType):
    pass


class OwnerTypeCode(PrefixCBC,CodeType):
    pass


class PackLevelCode(PrefixCBC,CodeType):
    pass


class PackQuantity(PrefixCBC,QuantityType):
    pass


class PackSizeNumeric(PrefixCBC,NumericType):
    pass


class PackageLevelCode(PrefixCBC,CodeType):
    pass


class PackagingTypeCode(PrefixCBC,CodeType):
    pass


class PackingCriteriaCode(PrefixCBC,CodeType):
    pass


class PackingMaterial(PrefixCBC,TextType):
    pass


class PaidAmount(PrefixCBC,AmountType):
    pass


class PaidDate(PrefixCBC,DateType):
    pass


class PaidTime(PrefixCBC,TimeType):
    pass


class ParentDocumentID(PrefixCBC,IdentifierType):
    pass


class ParentDocumentLineReferenceID(PrefixCBC,IdentifierType):
    pass


class ParentDocumentTypeCode(PrefixCBC,CodeType):
    pass


class ParentDocumentVersionID(PrefixCBC,IdentifierType):
    pass


class PartPresentationCode(PrefixCBC,CodeType):
    pass


class PartecipationPercent(PrefixCBC,PercentType):
    pass


class PartialDeliveryIndicator(PrefixCBC,IndicatorType):
    pass


class ParticipationPercent(PrefixCBC,PercentType):
    pass


class PartyCapacityAmount(PrefixCBC,AmountType):
    pass


class PartyTypeCode(PrefixCBC,CodeType):
    pass


class PartyType(PrefixCBC,TextType):
    pass


class PassengerQuantity(PrefixCBC,QuantityType):
    pass


class Password(PrefixCBC,TextType):
    pass


class PayPerView(PrefixCBC,TextType):
    pass


class PayableAlternativeAmount(PrefixCBC,AmountType):
    pass


class PayableAmount(PrefixCBC,AmountType):
    pass


class PayableRoundingAmount(PrefixCBC,AmountType):
    pass


class PayerReference(PrefixCBC,TextType):
    pass


class PaymentAlternativeCurrencyCode(PrefixCBC,CodeType):
    pass


class PaymentChannelCode(PrefixCBC,CodeType):
    pass


class PaymentCurrencyCode(PrefixCBC,CodeType):
    pass


class PaymentDescription(PrefixCBC,TextType):
    pass


class PaymentDueDate(PrefixCBC,DateType):
    pass


class PaymentFrequencyCode(PrefixCBC,CodeType):
    pass


class PaymentID(PrefixCBC,IdentifierType):
    pass


class PaymentMeansCode(PrefixCBC,CodeType):
    pass


class PaymentMeansID(PrefixCBC,IdentifierType):
    pass


class PaymentNote(PrefixCBC,TextType):
    pass


class PaymentOrderReference(PrefixCBC,TextType):
    pass


class PaymentPercent(PrefixCBC,PercentType):
    pass


class PaymentPurposeCode(PrefixCBC,CodeType):
    pass


class PaymentTermsDetailsURI(PrefixCBC,IdentifierType):
    pass


class PenaltyAmount(PrefixCBC,AmountType):
    pass


class PenaltySurchargePercent(PrefixCBC,PercentType):
    pass


class PerUnitAmount(PrefixCBC,AmountType):
    pass


class Percent(PrefixCBC,PercentType):
    pass


class PerformanceMetricTypeCode(PrefixCBC,CodeType):
    pass


class PerformanceValueQuantity(PrefixCBC,QuantityType):
    pass


class PerformingCarrierAssignedID(PrefixCBC,IdentifierType):
    pass


class PersonalSituation(PrefixCBC,TextType):
    pass


class PhoneNumber(PrefixCBC,TextType):
    pass


class PlacardEndorsement(PrefixCBC,TextType):
    pass


class PlacardNotation(PrefixCBC,TextType):
    pass


class PlannedDate(PrefixCBC,DateType):
    pass


class PlotIdentification(PrefixCBC,TextType):
    pass


class PositionCode(PrefixCBC,CodeType):
    pass


class PostEventNotificationDurationMeasure(PrefixCBC,MeasureType):
    pass


class PostalZone(PrefixCBC,TextType):
    pass


class Postbox(PrefixCBC,TextType):
    pass


class PowerIndicator(PrefixCBC,IndicatorType):
    pass


class PreCarriageIndicator(PrefixCBC,IndicatorType):
    pass


class PreEventNotificationDurationMeasure(PrefixCBC,MeasureType):
    pass


class PreferenceCriterionCode(PrefixCBC,CodeType):
    pass


class PrepaidAmount(PrefixCBC,AmountType):
    pass


class PrepaidIndicator(PrefixCBC,IndicatorType):
    pass


class PrepaidPaymentReferenceID(PrefixCBC,IdentifierType):
    pass


class PreviousCancellationReasonCode(PrefixCBC,CodeType):
    pass


class PreviousJobID(PrefixCBC,IdentifierType):
    pass


class PreviousMeterQuantity(PrefixCBC,QuantityType):
    pass


class PreviousMeterReadingDate(PrefixCBC,DateType):
    pass


class PreviousMeterReadingMethodCode(PrefixCBC,CodeType):
    pass


class PreviousMeterReadingMethod(PrefixCBC,TextType):
    pass


class PreviousVersionID(PrefixCBC,IdentifierType):
    pass


class PriceAmount(PrefixCBC,AmountType):
    pass


class PriceChangeReason(PrefixCBC,TextType):
    pass


class PriceEvaluationCode(PrefixCBC,CodeType):
    pass


class PriceRevisionFormulaDescription(PrefixCBC,TextType):
    pass


class PriceTypeCode(PrefixCBC,CodeType):
    pass


class PriceType(PrefixCBC,TextType):
    pass


class PricingCurrencyCode(PrefixCBC,CodeType):
    pass


class PricingUpdateRequestIndicator(PrefixCBC,IndicatorType):
    pass


class PrimaryAccountNumberID(PrefixCBC,IdentifierType):
    pass


class PrintQualifier(PrefixCBC,TextType):
    pass


class Priority(PrefixCBC,TextType):
    pass


class PrivacyCode(PrefixCBC,CodeType):
    pass


class PrizeDescription(PrefixCBC,TextType):
    pass


class PrizeIndicator(PrefixCBC,IndicatorType):
    pass


class ProcedureCode(PrefixCBC,CodeType):
    pass


class ProcessDescription(PrefixCBC,TextType):
    pass


class ProcessReasonCode(PrefixCBC,CodeType):
    pass


class ProcessReason(PrefixCBC,TextType):
    pass


class ProcurementSubTypeCode(PrefixCBC,CodeType):
    pass


class ProcurementTypeCode(PrefixCBC,CodeType):
    pass


class ProductTraceID(PrefixCBC,IdentifierType):
    pass


class ProfileExecutionID(PrefixCBC,IdentifierType):
    pass


class ProfileID(PrefixCBC,IdentifierType):
    pass


class ProfileStatusCode(PrefixCBC,CodeType):
    pass


class ProgressPercent(PrefixCBC,PercentType):
    pass


class PromotionalEventTypeCode(PrefixCBC,CodeType):
    pass


class ProviderTypeCode(PrefixCBC,CodeType):
    pass


class PublishAwardIndicator(PrefixCBC,IndicatorType):
    pass


class PurposeCode(PrefixCBC,CodeType):
    pass


class Purpose(PrefixCBC,TextType):
    pass


class QualityControlCode(PrefixCBC,CodeType):
    pass


class QuantityDiscrepancyCode(PrefixCBC,CodeType):
    pass


class Quantity(PrefixCBC,QuantityType):
    pass


class RadioCallSignID(PrefixCBC,IdentifierType):
    pass


class RailCarID(PrefixCBC,IdentifierType):
    pass


class Rank(PrefixCBC,TextType):
    pass


class Rate(PrefixCBC,RateType):
    pass


class ReceiptAdviceTypeCode(PrefixCBC,CodeType):
    pass


class ReceivedDate(PrefixCBC,DateType):
    pass


class ReceivedElectronicTenderQuantity(PrefixCBC,QuantityType):
    pass


class ReceivedForeignTenderQuantity(PrefixCBC,QuantityType):
    pass


class ReceivedQuantity(PrefixCBC,QuantityType):
    pass


class ReceivedTenderQuantity(PrefixCBC,QuantityType):
    pass


class ReferenceDate(PrefixCBC,DateType):
    pass


class ReferenceEventCode(PrefixCBC,CodeType):
    pass


class ReferenceID(PrefixCBC,IdentifierType):
    pass


class ReferenceTime(PrefixCBC,TimeType):
    pass


class Reference(PrefixCBC,TextType):
    pass


class ReferencedConsignmentID(PrefixCBC,IdentifierType):
    pass


class RefrigeratedIndicator(PrefixCBC,IndicatorType):
    pass


class RefrigerationOnIndicator(PrefixCBC,IndicatorType):
    pass


class Region(PrefixCBC,TextType):
    pass


class RegisteredDate(PrefixCBC,DateType):
    pass


class RegisteredTime(PrefixCBC,TimeType):
    pass


class RegistrationDate(PrefixCBC,DateType):
    pass


class RegistrationExpirationDate(PrefixCBC,DateType):
    pass


class RegistrationID(PrefixCBC,IdentifierType):
    pass


class RegistrationName(PrefixCBC,NameType):
    pass


class RegistrationNationalityID(PrefixCBC,IdentifierType):
    pass


class RegistrationNationality(PrefixCBC,TextType):
    pass


class RegulatoryDomain(PrefixCBC,TextType):
    pass


class RejectActionCode(PrefixCBC,CodeType):
    pass


class RejectReasonCode(PrefixCBC,CodeType):
    pass


class RejectReason(PrefixCBC,TextType):
    pass


class RejectedQuantity(PrefixCBC,QuantityType):
    pass


class RejectionNote(PrefixCBC,TextType):
    pass


class ReleaseID(PrefixCBC,IdentifierType):
    pass


class ReliabilityPercent(PrefixCBC,PercentType):
    pass


class Remarks(PrefixCBC,TextType):
    pass


class ReminderSequenceNumeric(PrefixCBC,NumericType):
    pass


class ReminderTypeCode(PrefixCBC,CodeType):
    pass


class ReplenishmentOwnerDescription(PrefixCBC,TextType):
    pass


class RequestForQuotationLineID(PrefixCBC,IdentifierType):
    pass


class RequestedDeliveryDate(PrefixCBC,DateType):
    pass


class RequestedDespatchDate(PrefixCBC,DateType):
    pass


class RequestedDespatchTime(PrefixCBC,TimeType):
    pass


class RequestedInvoiceCurrencyCode(PrefixCBC,CodeType):
    pass


class RequestedPublicationDate(PrefixCBC,DateType):
    pass


class RequiredCurriculaIndicator(PrefixCBC,IndicatorType):
    pass


class RequiredCustomsID(PrefixCBC,IdentifierType):
    pass


class RequiredDeliveryDate(PrefixCBC,DateType):
    pass


class RequiredDeliveryTime(PrefixCBC,TimeType):
    pass


class RequiredFeeAmount(PrefixCBC,AmountType):
    pass


class ResidenceTypeCode(PrefixCBC,CodeType):
    pass


class ResidenceType(PrefixCBC,TextType):
    pass


class ResidentOccupantsNumeric(PrefixCBC,NumericType):
    pass


class ResolutionCode(PrefixCBC,CodeType):
    pass


class ResolutionDate(PrefixCBC,DateType):
    pass


class ResolutionTime(PrefixCBC,TimeType):
    pass


class Resolution(PrefixCBC,TextType):
    pass


class ResponseCode(PrefixCBC,CodeType):
    pass


class ResponseDate(PrefixCBC,DateType):
    pass


class ResponseTime(PrefixCBC,TimeType):
    pass


class RetailEventName(PrefixCBC,NameType):
    pass


class RetailEventStatusCode(PrefixCBC,CodeType):
    pass


class ReturnabilityIndicator(PrefixCBC,IndicatorType):
    pass


class ReturnableMaterialIndicator(PrefixCBC,IndicatorType):
    pass


class ReturnableQuantity(PrefixCBC,QuantityType):
    pass


class RevisedForecastLineID(PrefixCBC,IdentifierType):
    pass


class RevisionDate(PrefixCBC,DateType):
    pass


class RevisionStatusCode(PrefixCBC,CodeType):
    pass


class RevisionTime(PrefixCBC,TimeType):
    pass


class RoamingPartnerName(PrefixCBC,NameType):
    pass


class RoleCode(PrefixCBC,CodeType):
    pass


class RoleDescription(PrefixCBC,TextType):
    pass


class Room(PrefixCBC,TextType):
    pass


class RoundingAmount(PrefixCBC,AmountType):
    pass


class SalesOrderID(PrefixCBC,IdentifierType):
    pass


class SalesOrderLineID(PrefixCBC,IdentifierType):
    pass


class SchemeURI(PrefixCBC,IdentifierType):
    pass


class SealIssuerTypeCode(PrefixCBC,CodeType):
    pass


class SealStatusCode(PrefixCBC,CodeType):
    pass


class SealingPartyType(PrefixCBC,TextType):
    pass


class SecurityClassificationCode(PrefixCBC,CodeType):
    pass


class SecurityID(PrefixCBC,IdentifierType):
    pass


class SellerEventID(PrefixCBC,IdentifierType):
    pass


class SequenceID(PrefixCBC,IdentifierType):
    pass


class SequenceNumberID(PrefixCBC,IdentifierType):
    pass


class SequenceNumeric(PrefixCBC,NumericType):
    pass


class SerialID(PrefixCBC,IdentifierType):
    pass


class ServiceInformationPreferenceCode(PrefixCBC,CodeType):
    pass


class ServiceName(PrefixCBC,NameType):
    pass


class ServiceNumberCalled(PrefixCBC,TextType):
    pass


class ServiceTypeCode(PrefixCBC,CodeType):
    pass


class ServiceType(PrefixCBC,TextType):
    pass


class SettlementDiscountAmount(PrefixCBC,AmountType):
    pass


class SettlementDiscountPercent(PrefixCBC,PercentType):
    pass


class SharesNumberQuantity(PrefixCBC,QuantityType):
    pass


class ShippingMarks(PrefixCBC,TextType):
    pass


class ShippingOrderID(PrefixCBC,IdentifierType):
    pass


class ShippingPriorityLevelCode(PrefixCBC,CodeType):
    pass


class ShipsRequirements(PrefixCBC,TextType):
    pass


class ShortQuantity(PrefixCBC,QuantityType):
    pass


class ShortageActionCode(PrefixCBC,CodeType):
    pass


class SignatureID(PrefixCBC,IdentifierType):
    pass


class SignatureMethod(PrefixCBC,TextType):
    pass


class SizeTypeCode(PrefixCBC,CodeType):
    pass


class SoleProprietorshipIndicator(PrefixCBC,IndicatorType):
    pass


class SourceCurrencyBaseRate(PrefixCBC,RateType):
    pass


class SourceCurrencyCode(PrefixCBC,CodeType):
    pass


class SourceForecastIssueDate(PrefixCBC,DateType):
    pass


class SourceForecastIssueTime(PrefixCBC,TimeType):
    pass


class SourceValueMeasure(PrefixCBC,MeasureType):
    pass


class SpecialInstructions(PrefixCBC,TextType):
    pass


class SpecialSecurityIndicator(PrefixCBC,IndicatorType):
    pass


class SpecialServiceInstructions(PrefixCBC,TextType):
    pass


class SpecialTerms(PrefixCBC,TextType):
    pass


class SpecialTransportRequirements(PrefixCBC,TextType):
    pass


class SpecificationID(PrefixCBC,IdentifierType):
    pass


class SpecificationTypeCode(PrefixCBC,CodeType):
    pass


class SplitConsignmentIndicator(PrefixCBC,IndicatorType):
    pass


class StartDate(PrefixCBC,DateType):
    pass


class StartTime(PrefixCBC,TimeType):
    pass


class StatementTypeCode(PrefixCBC,CodeType):
    pass


class StatusAvailableIndicator(PrefixCBC,IndicatorType):
    pass


class StatusCode(PrefixCBC,CodeType):
    pass


class StatusReasonCode(PrefixCBC,CodeType):
    pass


class StatusReason(PrefixCBC,TextType):
    pass


class StreetName(PrefixCBC,NameType):
    pass


class SubcontractingConditionsCode(PrefixCBC,CodeType):
    pass


class SubmissionDate(PrefixCBC,DateType):
    pass


class SubmissionDueDate(PrefixCBC,DateType):
    pass


class SubmissionMethodCode(PrefixCBC,CodeType):
    pass


class SubscriberID(PrefixCBC,IdentifierType):
    pass


class SubscriberTypeCode(PrefixCBC,CodeType):
    pass


class SubscriberType(PrefixCBC,TextType):
    pass


class SubstitutionStatusCode(PrefixCBC,CodeType):
    pass


class SuccessiveSequenceID(PrefixCBC,IdentifierType):
    pass


class SummaryDescription(PrefixCBC,TextType):
    pass


class SupplierAssignedAccountID(PrefixCBC,IdentifierType):
    pass


class SupplyChainActivityTypeCode(PrefixCBC,CodeType):
    pass


class TareWeightMeasure(PrefixCBC,MeasureType):
    pass


class TargetCurrencyBaseRate(PrefixCBC,RateType):
    pass


class TargetCurrencyCode(PrefixCBC,CodeType):
    pass


class TargetInventoryQuantity(PrefixCBC,QuantityType):
    pass


class TargetServicePercent(PrefixCBC,PercentType):
    pass


class TariffClassCode(PrefixCBC,CodeType):
    pass


class TariffCode(PrefixCBC,CodeType):
    pass


class TariffDescription(PrefixCBC,TextType):
    pass


class TaxAmount(PrefixCBC,AmountType):
    pass


class TaxCurrencyCode(PrefixCBC,CodeType):
    pass


class TaxEnergyAmount(PrefixCBC,AmountType):
    pass


class TaxEnergyBalanceAmount(PrefixCBC,AmountType):
    pass


class TaxEnergyOnAccountAmount(PrefixCBC,AmountType):
    pass


class TaxEvidenceIndicator(PrefixCBC,IndicatorType):
    pass


class TaxExclusiveAmount(PrefixCBC,AmountType):
    pass


class TaxExemptionReasonCode(PrefixCBC,CodeType):
    pass


class TaxExemptionReason(PrefixCBC,TextType):
    pass


class TaxIncludedIndicator(PrefixCBC,IndicatorType):
    pass


class TaxInclusiveAmount(PrefixCBC,AmountType):
    pass


class TaxLevelCode(PrefixCBC,CodeType):
    pass


class TaxPointDate(PrefixCBC,DateType):
    pass


class TaxTypeCode(PrefixCBC,CodeType):
    pass


class TaxableAmount(PrefixCBC,AmountType):
    pass


class TechnicalCommitteeDescription(PrefixCBC,TextType):
    pass


class TechnicalName(PrefixCBC,NameType):
    pass


class TelecommunicationsServiceCallCode(PrefixCBC,CodeType):
    pass


class TelecommunicationsServiceCall(PrefixCBC,TextType):
    pass


class TelecommunicationsServiceCategoryCode(PrefixCBC,CodeType):
    pass


class TelecommunicationsServiceCategory(PrefixCBC,TextType):
    pass


class TelecommunicationsSupplyTypeCode(PrefixCBC,CodeType):
    pass


class TelecommunicationsSupplyType(PrefixCBC,TextType):
    pass


class Telefax(PrefixCBC,TextType):
    pass


class Telephone(PrefixCBC,TextType):
    pass


class TenderEnvelopeID(PrefixCBC,IdentifierType):
    pass


class TenderEnvelopeTypeCode(PrefixCBC,CodeType):
    pass


class TenderResultCode(PrefixCBC,CodeType):
    pass


class TenderTypeCode(PrefixCBC,CodeType):
    pass


class TendererRequirementTypeCode(PrefixCBC,CodeType):
    pass


class TendererRoleCode(PrefixCBC,CodeType):
    pass


class TestMethod(PrefixCBC,TextType):
    pass


class Text(PrefixCBC,TextType):
    pass


class ThirdPartyPayerIndicator(PrefixCBC,IndicatorType):
    pass


class ThresholdAmount(PrefixCBC,AmountType):
    pass


class ThresholdQuantity(PrefixCBC,QuantityType):
    pass


class ThresholdValueComparisonCode(PrefixCBC,CodeType):
    pass


class TierRange(PrefixCBC,TextType):
    pass


class TierRatePercent(PrefixCBC,PercentType):
    pass


class TimeAmount(PrefixCBC,TextType):
    pass


class TimeDeltaDaysQuantity(PrefixCBC,QuantityType):
    pass


class TimeFrequencyCode(PrefixCBC,CodeType):
    pass


class TimezoneOffset(PrefixCBC,TextType):
    pass


class TimingComplaintCode(PrefixCBC,CodeType):
    pass


class TimingComplaint(PrefixCBC,TextType):
    pass


class Title(PrefixCBC,TextType):
    pass


class ToOrderIndicator(PrefixCBC,IndicatorType):
    pass


class TotalAmount(PrefixCBC,AmountType):
    pass


class TotalBalanceAmount(PrefixCBC,AmountType):
    pass


class TotalConsumedQuantity(PrefixCBC,QuantityType):
    pass


class TotalCreditAmount(PrefixCBC,AmountType):
    pass


class TotalDebitAmount(PrefixCBC,AmountType):
    pass


class TotalDeliveredQuantity(PrefixCBC,QuantityType):
    pass


class TotalGoodsItemQuantity(PrefixCBC,QuantityType):
    pass


class TotalInvoiceAmount(PrefixCBC,AmountType):
    pass


class TotalMeteredQuantity(PrefixCBC,QuantityType):
    pass


class TotalPackageQuantity(PrefixCBC,QuantityType):
    pass


class TotalPackagesQuantity(PrefixCBC,QuantityType):
    pass


class TotalPaymentAmount(PrefixCBC,AmountType):
    pass


class TotalTaskAmount(PrefixCBC,AmountType):
    pass


class TotalTaxAmount(PrefixCBC,AmountType):
    pass


class TotalTransportHandlingUnitQuantity(PrefixCBC,QuantityType):
    pass


class TraceID(PrefixCBC,IdentifierType):
    pass


class TrackingDeviceCode(PrefixCBC,CodeType):
    pass


class TrackingID(PrefixCBC,IdentifierType):
    pass


class TradeItemPackingLabelingTypeCode(PrefixCBC,CodeType):
    pass


class TradeServiceCode(PrefixCBC,CodeType):
    pass


class TradingRestrictions(PrefixCBC,TextType):
    pass


class TrainID(PrefixCBC,IdentifierType):
    pass


class TransactionCurrencyTaxAmount(PrefixCBC,AmountType):
    pass


class TransitDirectionCode(PrefixCBC,CodeType):
    pass


class TransportAuthorizationCode(PrefixCBC,CodeType):
    pass


class TransportEmergencyCardCode(PrefixCBC,CodeType):
    pass


class TransportEquipmentTypeCode(PrefixCBC,CodeType):
    pass


class TransportEventTypeCode(PrefixCBC,CodeType):
    pass


class TransportExecutionPlanReferenceID(PrefixCBC,IdentifierType):
    pass


class TransportExecutionStatusCode(PrefixCBC,CodeType):
    pass


class TransportHandlingUnitTypeCode(PrefixCBC,CodeType):
    pass


class TransportMeansTypeCode(PrefixCBC,CodeType):
    pass


class TransportModeCode(PrefixCBC,CodeType):
    pass


class TransportServiceCode(PrefixCBC,CodeType):
    pass


class TransportServiceProviderRemarks(PrefixCBC,TextType):
    pass


class TransportServiceProviderSpecialTerms(PrefixCBC,TextType):
    pass


class TransportUserRemarks(PrefixCBC,TextType):
    pass


class TransportUserSpecialTerms(PrefixCBC,TextType):
    pass


class TransportationServiceDescription(PrefixCBC,TextType):
    pass


class TransportationServiceDetailsURI(PrefixCBC,IdentifierType):
    pass


class TransportationStatusTypeCode(PrefixCBC,CodeType):
    pass


class TypeCode(PrefixCBC,CodeType):
    pass


class UBLVersionID(PrefixCBC,IdentifierType):
    pass


class UNDGCode(PrefixCBC,CodeType):
    pass


class URI(PrefixCBC,IdentifierType):
    pass


class UUID(PrefixCBC,IdentifierType):
    pass


class UnknownPriceIndicator(PrefixCBC,IndicatorType):
    pass


class UpperOrangeHazardPlacardID(PrefixCBC,IdentifierType):
    pass


class UrgencyCode(PrefixCBC,CodeType):
    pass


class UtilityStatementTypeCode(PrefixCBC,CodeType):
    pass


class ValidateProcess(PrefixCBC,TextType):
    pass


class ValidateTool(PrefixCBC,TextType):
    pass


class ValidateToolVersion(PrefixCBC,TextType):
    pass


class ValidationDate(PrefixCBC,DateType):
    pass


class ValidationResultCode(PrefixCBC,CodeType):
    pass


class ValidationTime(PrefixCBC,TimeType):
    pass


class ValidatorID(PrefixCBC,IdentifierType):
    pass


class ValidityStartDate(PrefixCBC,DateType):
    pass


class ValueAmount(PrefixCBC,AmountType):
    pass


class ValueMeasure(PrefixCBC,MeasureType):
    pass


class ValueQualifier(PrefixCBC,TextType):
    pass


class ValueQuantity(PrefixCBC,QuantityType):
    pass


class Value(PrefixCBC,TextType):
    pass


class VarianceQuantity(PrefixCBC,QuantityType):
    pass


class VariantConstraintIndicator(PrefixCBC,IndicatorType):
    pass


class VariantID(PrefixCBC,IdentifierType):
    pass


class VersionID(PrefixCBC,IdentifierType):
    pass


class VesselID(PrefixCBC,IdentifierType):
    pass


class VesselName(PrefixCBC,NameType):
    pass


class WarrantyInformation(PrefixCBC,TextType):
    pass


class WebsiteURI(PrefixCBC,IdentifierType):
    pass


class WeekDayCode(PrefixCBC,CodeType):
    pass


class WeightNumeric(PrefixCBC,NumericType):
    pass


class Weight(PrefixCBC,TextType):
    pass


class WeightingAlgorithmCode(PrefixCBC,CodeType):
    pass


class WorkPhaseCode(PrefixCBC,CodeType):
    pass


class WorkPhase(PrefixCBC,TextType):
    pass


class XPath(PrefixCBC,TextType):
    pass
