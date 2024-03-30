"""
CCTS Core Component Type Schema Module
"""

from ublib21.base import BasicXMLParseableObject


class AmountType(BasicXMLParseableObject):
    """
    A number of monetary units specified in a currency where the unit of the 
    currency is explicit or implied.
    """
    prefix = 'ccts'
    
    attr_names_mapping = {
        'currency_id': 'currencyID',
        'currency_code_list_version_id': 'currencyCodeListVersionID'
    }

    def __init__(self, value, currency_id=None,
                 currency_code_list_version_id=None):
        """
        :param float value: The amount itself.
        :param str currency_id: The currency of the amount
        :param str currency_code_list_version_id: The VersionID of the 
        UN/ECE Rec9 code list
        """
        super().__init__(value)
        # TODO: Validate attributes
        self.currency_id = currency_id
        self.currency_code_list_version_id = currency_code_list_version_id


class BinaryObjectType(BasicXMLParseableObject):
    """
    A set of finite-length sequences of binary octets.
    """
    prefix = 'ccts'

    attr_names_mapping = {
        "format": "format",
        "mime_code": "mimeCode",
        "encoding_code": "encodingCode",
        "character_set_code": "characterSetCode",
        "uri": "uri",
        "filename": "filename"
    }

    def __init__(self, value, format_=None, mime_code=None, encoding=None,
                 character_set_code=None, uri=None, filename=None):
        super().__init__(value)
        # TODO: Validate attributes
        self.format = format_
        self.mime_code = mime_code
        self.encoding_code = encoding
        self.character_set_code = character_set_code
        self.uri = uri
        self.filename = filename


class CodeType(BasicXMLParseableObject):
    """
    A character string (letters, figures, or symbols) that for brevity and/or 
    languange independence may be used to represent or replace a definitive value 
    or text of an attribute together with relevant supplementary information.
    """
    prefix = 'ccts'

    attr_names_mapping = {
        "list_id": "listID",
        "list_agency_id": "listAgencyID",
        "list_agency_name": "listAgencyName",
        "list_name": "listName",
        "list_version_id": "listVersionID",
        "name": "name",
        "language_id": "languageID",
        "list_uri": "listURI",
        "list_scheme_uri": "listSchemeURI"
    }

    def __init__(self, value, list_id=None, list_agency_id=None, list_agency_name=None, list_name=None,
                 list_version_id=None, name=None, language_id=None, list_uri=None, list_scheme_uri=None):
        super().__init__(value)

        self.list_id = list_id
        self.list_agency_id = list_agency_id
        self.list_agency_name = list_agency_name
        self.list_name = list_name
        self.list_name = list_name
        self.list_version_id = list_version_id
        self.name = name
        self.language_id = language_id
        self.list_uri = list_uri
        self.list_scheme_uri = list_scheme_uri

#


class DateTimeType(BasicXMLParseableObject):
    """
    A particular point in the progression of time together with the relevant supplementary information.
    """
    prefix = 'ccts'

    attr_names_mapping = {
        "format": "format",

    }

    def __init__(self, value, format=None):
        super().__init__(value)

        self.format = format


class IdentifierType(BasicXMLParseableObject):
    """
    A character string to identify and distinguish uniquely, one instance of an object in an identification 
    scheme from all other objects in the same scheme together with relevant supplementary information.    
    """
    prefix = 'ccts'

    attr_names_mapping = {
        "scheme_id": "schemeID",
        "scheme_name": "schemeName",
        "scheme_agency_id": "schemeAgencyID",
        "scheme_agency_name": "schemeAgencyName",
        "scheme_version_id": "schemeVersionID",
        "scheme_data_uri": "schemeDataURI",
        "scheme_uri": "schemeURI",
    }

    def __init__(self, value, scheme_id=None, scheme_name=None, scheme_agency_id=None, scheme_agency_name=None,
                 scheme_version_id=None, scheme_data_uri=None, scheme_uri=None):
        super().__init__(value)

        self.scheme_id = scheme_id
        self.scheme_name = scheme_name
        self.scheme_agency_id = scheme_agency_id
        self.scheme_agency_name = scheme_agency_name
        self.scheme_version_id = scheme_version_id
        self.scheme_data_uri = scheme_data_uri
        self.scheme_uri = scheme_uri


class IndicatorType(BasicXMLParseableObject):
    """
    A list of two mutually exclusive Boolean values that express the only possible states of a Property
    """
    prefix = 'ccts'

    attr_names_mapping = {
        "format": "format",

    }

    def __init__(self, value, format=None):
        super().__init__(value)

        self.format = format


class MeasureType(BasicXMLParseableObject):
    """
    A numeric value determined by measuring an object along with the specified unit of measure.   
    """
    prefix = 'ccts'

    attr_names_mapping = {
        "unit_code": "unitCode",
        "unit_code_list_version_id": "unitCodeListVersionID",
    }

    def __init__(self, value, unit_code=None, unit_code_list_version_id=None):
        super().__init__(value)

        self.unit_code = unit_code
        self.unit_code_list_version_id = unit_code_list_version_id


class NumericType(BasicXMLParseableObject):
    """
    Numeric information that is assigned or is determined by calculation, counting, or sequencing.
    It does not require a unit of quantity or unit of measure.
    """
    prefix = 'ccts'

    attr_names_mapping = {
        "format": "format",

    }

    def __init__(self, value, format=None):
        super().__init__(value)

        self.format = format


class QuantityType(BasicXMLParseableObject):
    """
    A counted number of non-monetary units possibly including fractions.
    """
    prefix = 'ccts'

    attr_names_mapping = {
        "unit_code": "unitCode",
        "unit_code_list_id": "unitCodeListID",
        "unit_code_list_agency_id": "unitCodeListAgencyID",
        "unit_code_list_agency_name": "unitCodeListAgencyName",

    }

    def __init__(self, value, unit_code=None, unit_code_list_id=None,  unit_code_list_agency_id=None,
                 unit_code_list_agency_name=None):
        super().__init__(value)

        self.unit_code = unit_code
        self.unit_code_list_id = unit_code_list_id
        self.unit_code_list_agency_id = unit_code_list_agency_id
        self.unit_code_list_agency_name = unit_code_list_agency_name


class TextType(BasicXMLParseableObject):
    """
    A character string (i.e. a finite set of characters) generally in the form of words of a language.
    """
    prefix = 'ccts'

    attr_names_mapping = {
        "language_id": "languageID",
        "language_locale_id": "languageLocaleID",

    }

    def __init__(self, value, language_id=None, language_locale_id=None, xml_namespaces = None):
        super().__init__(value, xml_namespaces=xml_namespaces)

        self.language_id = language_id
        self.language_locale_id = language_locale_id
