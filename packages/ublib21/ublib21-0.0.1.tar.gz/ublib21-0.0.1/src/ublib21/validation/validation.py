import pathlib

from lxml import etree

# from ublib21.exceptions import ImproperlyConfiguredException


class ImproperlyConfiguredException(Exception):
    pass


class BaseStringValidator:
    package_dir = pathlib.Path(__file__).absolute().parent
    schema_file = None

    @classmethod
    def validate(cls, xml):
        if cls.schema_file is None:
            raise ImproperlyConfiguredException(
                "Missing schema file configuration")
        try:
            # Parse XML string
            xml_tree = etree.fromstring(xml)

            # Load XSD schema
            with open(cls.package_dir / cls.schema_file, 'rb') as xsd_file:
                xsd_tree = etree.parse(xsd_file)

            # Create XML schema validator
            xml_validator = etree.XMLSchema(xsd_tree)

            # Validate XML against XSD
            is_valid = xml_validator.validate(xml_tree)

            if is_valid:
                print("XML is valid against the XSD schema.")
                return True
            else:
                print("XML is NOT valid against the XSD schema.")
                print(xml_validator.error_log)
                return False

        except etree.XMLSyntaxError as e:
            print(f"XML syntax error: {e}")
            return False
        except etree.XMLSchemaParseError as e:
            print(f"XSD schema parse error: {e}")
            return False
        except etree.XMLSchemaValidateError as e:
            print(f"XML validation error: {e}")
            return False


class CommonAggregateComponentValidator(BaseStringValidator):
    schema_file = "./schemes/common/UBL-CommonAggregateComponents-2.1.xsd"


class CommonBasicComponentValidator(BaseStringValidator):
    schema_file = "./schemes/common/UBL-CommonBasicComponents-2.1.xsd"


class InvoiceValidator(BaseStringValidator):
    schema_file = "./schemes/maindoc/UBL-Invoice-2.1.xsd"

# xml_string = '<Shipment xmlns="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"><cbc:ID>SHIP_123</cbc:ID><cbc:HandlingCode>123ABC</cbc:HandlingCode><cbc:HandlingInstructions>Deliver to Cnel Olmedo</cbc:HandlingInstructions><cbc:HandlingInstructions>Fragile</cbc:HandlingInstructions><cbc:HandlingInstructions>Max stack 6</cbc:HandlingInstructions></Shipment>'


# CommonAggregateComponentValidator.validate(xml_string)
