from typing import Any, List
from ublib21.exceptions import JustOneElementAllowed
from ublib21.exceptions import ListMustNotBeEmptyException
from ublib21.base import BasicXMLParseableObject
from ublib21.base import ComplexXMLParseableObject
from ublib21.common import udt
from ublib21.common import cbc



class ExtensionAgencyID(udt.IdentifierType):
    pass


class ExtensionAgencyName(udt.TextType):
    pass


class ExtensionAgencyURI(udt.IdentifierType):
    pass


class ExtensionReason(udt.TextType):
    pass


class ExtensionReasonCode(udt.CodeType):
    pass


class ExtensionURI(udt.IdentifierType):
    pass


class ExtensionVersionID(udt.IdentifierType):
    pass


class ExtensionContent(BasicXMLParseableObject):

    def __init__(self, value:Any, xml_namespaces=None) -> None:
        if isinstance(value, list):
            raise JustOneElementAllowed("ExtensionContent should have only 1 element")
        super().__init__(value, xml_namespaces)


class UBLExtension(ComplexXMLParseableObject):
    extension_content = None
    id = None
    name = None
    extension_agency_id = None
    extension_agency_name = None
    extension_version_id = None
    extension_agency_uri = None
    extension_uri = None
    extension_reason_code = None
    extension_reason = None
    order_list = [
        "id",
        "name",
        "extension_agency_id",
        "extension_agency_name",
        "extension_version_id",
        "extension_agency_uri",
        "extension_uri",
        "extension_reason_code",
        "extension_reason",
        "extension_content"
    ]

    def __init__(self, extension_content: ExtensionContent,
                 id_: cbc.ID = None,
                 name: cbc.Name = None,
                 extension_agency_id: ExtensionAgencyID = None,
                 extension_agency_name: ExtensionAgencyName = None,
                 extension_version_id: ExtensionVersionID = None,
                 extension_agency_uri: ExtensionAgencyURI = None,
                 extension_uri: ExtensionURI = None,
                 extension_reason_code: ExtensionReasonCode = None,
                 extension_reason: ExtensionReason = None, xml_namespaces=None) -> None:
        super().__init__(xml_namespaces)
        self.extension_content = extension_content
        self.id = id_
        self.name = name
        self.extension_agency_id = extension_agency_id
        self.extension_agency_name = extension_agency_name
        self.extension_version_id = extension_version_id
        self.extension_agency_uri = extension_agency_uri
        self.extension_uri = extension_uri
        self.extension_reason_code = extension_reason_code
        self.extension_reason = extension_reason


class UBLExtensions(ComplexXMLParseableObject):
    ubl_extensions = None
    order_list = [
        'ubl_extensions'
    ]

    def __init__(self, ubl_extensions:List[UBLExtension] = None, xml_namespaces=None) -> None:
        super().__init__(xml_namespaces)

        if not ubl_extensions:
            raise ListMustNotBeEmptyException('ubl_extensions')

        self.ubl_extensions = ubl_extensions