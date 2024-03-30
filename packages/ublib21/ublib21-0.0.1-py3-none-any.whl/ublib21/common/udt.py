"""
This schema fragment implements UBL unqualified datatypes using core
component types with all supplementary components as described in
CCTS 2.01 http://www.unece.org/cefact/ebxml/CCTS_V2-01_Final.pdf tables
8-1, 8-2 and 8-3.
"""

from ublib21.common.ccts_cct import AmountType as AmountType_
from ublib21.common.ccts_cct import BinaryObjectType as BinaryObjectType_
from ublib21.common.ccts_cct import CodeType as CodeType_
from ublib21.common.ccts_cct import DateTimeType as DateTimeType_
from ublib21.common.ccts_cct import IdentifierType as IdentifierType_
from ublib21.common.ccts_cct import MeasureType as MeasureType_
from ublib21.common.ccts_cct import NumericType as NumericType_
from ublib21.common.ccts_cct import QuantityType as QuantityType_
from ublib21.common.ccts_cct import TextType as TextType_

from ublib21.base import BasicXMLParseableObject


class AmountType(AmountType_):
    """
    A number of monetary units specified using a given unit of currency.
    """
    prefix = 'udt'

    def __init__(self, value: float, currency_id: str, currency_code_list_version_id: str = None):
        super().__init__(value, currency_id, currency_code_list_version_id)


class BinaryObjectType(BinaryObjectType_):
    """
    A set of finite-length sequences of binary octets.
    """
    prefix = 'udt'

    def __init__(self, value, mime_code, format_=None, encoding=None,
                 character_set_code=None, uri=None, filename=None):
        super().__init__(value, format_, mime_code,
                         encoding, character_set_code, uri, filename)


class GraphicType(BinaryObjectType):
    """
    A diagram, graph, mathematical curve, or similar representation.
    """
    prefix = 'udt'
    pass


class PictureType(BinaryObjectType):
    """
    A diagram, graph, mathematical curve, or similar representation.
    """
    prefix = 'udt'
    pass


class SoundType(BinaryObjectType):
    """
    An audio representation.
    """
    prefix = 'udt'
    pass


class VideoType(BinaryObjectType):
    """
    A video representation.
    """
    prefix = 'udt'
    pass


class CodeType(CodeType_):
    """
    A character string (letters, figures, or symbols) 
    that for brevity and/or language independence may be used to represent 
    or replace a definitive value or text of an attribute, 
    together with relevant supplementary information.
    """
    prefix = 'udt'
    pass


class DateTimeType(DateTimeType_):
    """
    A particular point in the progression of time, together with relevant supplementary information.
    """
    prefix = 'udt'
    pass


class DateType(BasicXMLParseableObject):
    """
    One calendar day according the Gregorian calendar.
    """
    prefix = 'udt'

    def __init__(self, value) -> None:
        self.value = value
        # TODO: Check what to do with attribute mappings
        # if self.attr_names_mapping is None:
        #     raise MissingAttributeNamesMappingException(f"{self.__class__.__name__}")


class TimeType(BasicXMLParseableObject):
    """
    An instance of time that occurs every day.
    """
    prefix = 'udt'

    def __init__(self, value) -> None:
        self.value = value
        # TODO: Check what to do with attribute mappings
        # if self.attr_names_mapping is None:
        #     raise MissingAttributeNamesMappingException(f"{self.__class__.__name__}")


class IdentifierType(IdentifierType_):
    """
    A character string to identify and uniquely  distinguish one instance of an object 
    in an identification scheme from all other objects in the same scheme, together with relevant 
    supplementary information.
    """
    prefix = 'udt'
    pass


class IndicatorType(BasicXMLParseableObject):
    """
    A list of two mutually exclusive Boolean values that express the only possible states of a property.
    """
    prefix = 'udt'

    def __init__(self, value) -> None:
        self.value = value
        # TODO: Check what to do with attribute mappings
        # if self.attr_names_mapping is None:
        #     raise MissingAttributeNamesMappingException(f"{self.__class__.__name__}")


class MeasureType(MeasureType_):
    """
    A numeric value determined by measuring an object using a specified unit of measure.
    """
    prefix = 'udt'

    def __init__(self, value, unit_code, unit_code_list_version_id=None):
        super().__init__(value, unit_code, unit_code_list_version_id)


class NumericType(NumericType_):
    """
    Numeric information that is assigned or is determined by calculation, counting,
      or sequencing. It does not require a unit of quantity or unit of measure.
    """
    prefix = 'udt'
    pass


class ValueType(NumericType_):
    """
    Numeric information that is assigned or is determined by calculation, counting, or 
    sequencing. It does not require a unit of quantity or unit of measure.
    """
    prefix = 'udt'
    pass


class PercentType(NumericType_):
    """
    Numeric information that is assigned or is determined by calculation, counting, 
    or sequencing and is expressed as a percentage. It does not require a unit of quantity or unit of measure.
    """
    prefix = 'udt'
    pass


class RateType(NumericType_):
    """
    A numeric expression of a rate that is assigned or is determined by calculation, counting, or
      sequencing. It does not require a unit of quantity or unit of measure.
    """
    prefix = 'udt'
    pass


class QuantityType(QuantityType_):
    """
    A counted number of non-monetary units, possibly including a fractional part.
    """
    prefix = 'udt'
    pass


class TextType(TextType_):
    """
    A character string (i.e. a finite set of characters), generally in the form of words of a language.
    """
    prefix = 'udt'
    pass


class NameType(TextType_):
    """
    A character string that constitutes the distinctive designation of a person, place, thing or concept.
    """
    prefix = 'udt'
    pass
