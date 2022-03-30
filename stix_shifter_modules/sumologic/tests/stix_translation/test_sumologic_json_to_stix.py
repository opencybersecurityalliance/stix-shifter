import json
import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.sumologic.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "sumologic"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "sumologic",
    "identity_class": "events"
}
options = {}


class TestSumoLogicResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for sumologic translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """
        return the obj in the itr if constraint is true
        """
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        """
        to check whether the object belongs to respective stix object
        """
        return TestSumoLogicResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def test_common_prop():
        """
        to test the common stix object properties
        """
        data = {
            "_blockid": "919015073006647296",
            "_messagetime": "1632634146000",
            "_raw": "Sep 26 05:29:06 sumologic NetworkManager[677]: <info>  [1632614346.1075] dhcp4 (eth0):   address 10.35.38.184",
            "_collectorid": "100695732",
            "_signature": "$DATE sumologic NetworkManager[677]: <info>  [*.*] dhcp4 (eth0):   nameserver '*.*.*.*'",
            "_tags": "",
            "_sourceid": "103458456",
            "_collector": "sumologic.gslab.com",
            "_messagecount": "2",
            "_sourcehost": "sumologic.gslab.com",
            "_rawnodate": "$DATE sumologic NetworkManager[677]: <info>  [1632614346.1075] dhcp4 (eth0):   address 10.35.38.184",
            "_messageid": "919015073006647298",
            "_sourcename": "/var/log/messages",
            "_size": "109",
            "_signatureid": "-7078046322786406611",
            "_view": "",
            "_receipttime": "1632614350987",
            "_sourcecategory": "linux/system",
            "_format": "t:cache:o:0:l:15:p:MMM dd HH:mm:ss",
            "_source": "Linux System_3",
            "firstName": "Ismail",
            "lastName": "Memon",
            "email": "ismail.memon@gslab.com",
            "roleIds": [
                "000000000002E875"
            ],
            "createdAt": "2021-09-23T11:34:07.255Z",
            "createdBy": "FFFFFFFFFFFFFD66",
            "modifiedAt": "2021-10-08T10:14:34.911Z",
            "modifiedBy": "000000000001F46E",
            "id": "000000000001F46E",
            "isActive": True,
            "isLocked": False,
            "isMfaEnabled": False,
            "lastLoginTimestamp": "2021-10-08T10:14:34.902Z",
            "displayName": "Ismail Memon"
        }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        assert result_bundle_identity['id'] == data_source['id']
        assert result_bundle_identity['name'] == data_source['name']
        assert result_bundle_identity['identity_class'] == data_source['identity_class']

        observed_data = result_bundle_objects[1]
        assert observed_data['id'] is not None
        assert observed_data['type'] == "observed-data"
        assert observed_data['created_by_ref'] == result_bundle_identity['id']

        assert observed_data['modified'] is not None
        assert observed_data['created'] is not None
        assert observed_data['first_observed'] is not None
        assert observed_data['last_observed'] is not None
        assert observed_data['number_observed'] is not None

    @staticmethod
    def test_custom_property():
        """
        to test the custom stix object properties
        """
        data = {
            "_blockid": "919015073006647296",
            "_messagetime": "1632634146000",
            "_raw": "Sep 26 05:29:06 sumologic NetworkManager[677]: <info>  [1632614346.1075] dhcp4 (eth0):   address 10.35.38.184",
            "_collectorid": "100695732",
            "_signature": "$DATE sumologic NetworkManager[677]: <info>  [*.*] dhcp4 (eth0):   nameserver '*.*.*.*'",
            "_tags": "",
            "_sourceid": "103458456",
            "_collector": "sumologic.gslab.com",
            "_messagecount": "2",
            "_sourcehost": "sumologic.gslab.com",
            "_rawnodate": "$DATE sumologic NetworkManager[677]: <info>  [1632614346.1075] dhcp4 (eth0):   address 10.35.38.184",
            "_messageid": "919015073006647298",
            "_sourcename": "/var/log/messages",
            "_size": "109",
            "_signatureid": "-7078046322786406611",
            "_view": "",
            "_receipttime": "1632614350987",
            "_sourcecategory": "linux/system",
            "_format": "t:cache:o:0:l:15:p:MMM dd HH:mm:ss",
            "_source": "Linux System_3",
            "firstName": "Ismail",
            "lastName": "Memon",
            "email": "ismail.memon@gslab.com",
            "roleIds": [
                "000000000002E875"
            ],
            "createdAt": "2021-09-23T11:34:07.255Z",
            "createdBy": "FFFFFFFFFFFFFD66",
            "modifiedAt": "2021-10-08T10:14:34.911Z",
            "modifiedBy": "000000000001F46E",
            "id": "000000000001F46E",
            "isActive": True,
            "isLocked": False,
            "isMfaEnabled": False,
            "lastLoginTimestamp": "2021-10-08T10:14:34.902Z",
            "displayName": "Ismail Memon"
        }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)

        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        custom_object_1 = TestSumoLogicResultsToStix.get_first_of_type(objects.values(), 'x-sumologic-source')

        assert custom_object_1 is not None, 'Custom object type not found'
        assert custom_object_1.keys() == {'type', 'collectorid', 'sourcename'}
        assert custom_object_1['collectorid'] == "100695732"
        assert custom_object_1['sourcename'] == "/var/log/messages"
