from ublib21.common import cbc
from ublib21.validation.validation import CommonBasicComponentValidator

class TestAcceptedVariantsDescription:

    def test_value(self):
        class AcceptedVariantsDescription(cbc.AcceptedVariantsDescription):
            prefix = ''
        namespaces = [
            'xmlns="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"'
        ]
        a = AcceptedVariantsDescription("HOLAS", "es", xml_namespaces=namespaces)
        assert CommonBasicComponentValidator.validate(str(a)) == True