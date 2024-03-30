from ublib21.common import cbc, cac
from ublib21.validation.validation import CommonAggregateComponentValidator

class TestAcceptedVariantsDescription:

    def test_value(self):
        class Shipment(cac.Shipment):
            prefix = ''
        
        namespaces = [
            'xmlns="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"',
            'xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"'
        ]
        shipment_id = cbc.ID('SHIP_123')
        handling_code = cbc.HandlingCode('123ABC')
        instructions = [
            cbc.HandlingInstructions('Deliver to Cnel Olmedo'),
            cbc.HandlingInstructions('Fragile'),
            cbc.HandlingInstructions('Max stack 6'),
        ]
        a = Shipment(shipment_id, handling_code=handling_code, handling_instructions=instructions, xml_namespaces = namespaces)
        assert CommonAggregateComponentValidator.validate(str(a))==True