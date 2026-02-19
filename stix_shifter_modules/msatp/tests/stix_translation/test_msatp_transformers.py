import unittest

from stix_shifter_modules.msatp.stix_translation.transformers import MsatpToTimestamp, MsatpToRegistryValue, \
    FormatMacList, IfValidUrl, GetDomainName, ToFileName, ToDirectory, ToMSATPDirectoryPath, SeverityToNumericVal, \
    Alert, JsonToString


class TestMsatpTransformers(unittest.TestCase):

    def test_transform_msatp_to_timestamp(self):
        val = MsatpToTimestamp.transform('2023-03-12T21:56:34.0646516Z')
        assert val == '2023-03-12T21:56:34.064Z'

    def test_msatp_to_registry_value(self):
        data = [{"RegistryValueType": "Binary",
                 "RegistryValueName": "FailureActions",
                 "RegistryValueData": ""}]
        values = MsatpToRegistryValue.transform(data)
        assert len(values) == 1
        val = values[0]
        assert val.get("name") == "FailureActions"
        assert val.get("data") == ""
        assert val.get("data_type") == "REG_BINARY"

    def test_format_mac_list(self):
        data = ['B0-4F-13-0F-E1-7B']
        macs = FormatMacList.transform(data)
        assert len(macs) == 1
        assert macs[0] == 'b0:4f:13:0f:e1:7b'

    def test_multiple_format_mac_list(self):
        data = ['11-22-33-44-55-66', '11-22-AA-BB-CC-DD']
        macs = FormatMacList.transform(data)
        assert len(macs) == 2
        assert macs[0] == '11:22:33:44:55:66'
        assert macs[1] == '11:22:aa:bb:cc:dd'

    def test_is_valid_url(self):
        assert IfValidUrl.transform("ibm.com") == ""
        assert IfValidUrl.transform("http://ibm.com") == "http://ibm.com"
        assert IfValidUrl.transform("https://ibm.com") == "https://ibm.com"
        assert IfValidUrl.transform("http://ibm.com/a/a/a?a=a") == "http://ibm.com/a/a/a?a=a"
        assert IfValidUrl.transform("ibm.com/a/a/a?a=a") == ""

    def test_get_domain_name(self):
        assert GetDomainName.transform("ibm.com") == "ibm.com"
        assert GetDomainName.transform("www.ibm.com") == "www.ibm.com"
        assert GetDomainName.transform("http://ibm.com") == "ibm.com"
        assert GetDomainName.transform("https://ibm.com/a/a/a?a=a") == "ibm.com"
        assert GetDomainName.transform("http://xn--diseolatinoamericano-66b.com/") == "xn--diseolatinoamericano-66b.com"

    def test_to_file_name(self):
        assert ToFileName.transform("c:\\a\\a\\a.exe") == "a.exe"

    def test_to_directory(self):
        assert ToDirectory.transform("c:\\a\\a\\a.exe") == "c:\\a\\a"

    def test_to_msatp_directory(self):
        assert ToMSATPDirectoryPath.transform("c:\\a\\a\\a.exe") == "c:\\a\\a"

    def test_severity_to_numeric_val(self):
        assert SeverityToNumericVal.transform("high") == 99
        assert SeverityToNumericVal.transform("medium") == 66
        assert SeverityToNumericVal.transform("low") == 33

    def test_alert(self):
        assert Alert.transform("") == "alert"

    def test_json_to_string(self):
        assert JsonToString.transform("{") == "{"
        assert JsonToString.transform('{ "a": 1, "b": 2 }') == "a: 1, b: 2"
