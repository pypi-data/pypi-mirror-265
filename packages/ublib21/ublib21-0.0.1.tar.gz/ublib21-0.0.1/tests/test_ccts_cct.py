from ublib21.common.ccts_cct import AmountType as AmountType_

class AmountType(AmountType_):
        prefix = ''

class TestAmountType:
    

    def test_no_attrs(self):
        a = AmountType(100)
        assert str(a) == "<Amount>100</Amount>"

    def test_currency_id(self):
        a = AmountType(100, 'USD')
        assert str(a) == '<Amount currencyID="USD">100</Amount>'

    def test_currency_code_list_version_id(self):
        a = AmountType(100, 'USD', '1')
        assert str(a) == '<Amount currencyID="USD" currencyCodeListVersionID="1">100</Amount>'