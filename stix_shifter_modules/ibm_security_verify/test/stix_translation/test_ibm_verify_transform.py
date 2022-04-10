import json
import logging
import unittest
from unicodedata import category

from stix_shifter.stix_translation import stix_translation
from stix_shifter_modules.ibm_security_verify.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import (
    get_module_transformers,
)

translation = stix_translation.StixTranslation()
# config_file = open('stix_shifter_modules/verify_event/configuration/config.json').read()
# from_stix_file = open('stix_shifter_modules/verify_event/stix_translation/json/from_stix_map.json').read()
# to_stix_file = open('stix_shifter_modules/verify_event/stix_translation/json/to_stix_map.json').read()
# OPTIONS = json.loads(from_stix_file)

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger()
MODULE = "ibm_security_verify"
RESULTS = "results"
TRANSFORMERS = get_module_transformers(MODULE)
epoch_to_timestamp_class = TRANSFORMERS.get("EpochToTimestamp")
entry_point = EntryPoint()
MAP_DATA = entry_point.get_results_translator().map_data


DATA_SOURCE = {
    "type": "identity",
    "id": "32a23267-52fb-4e82-859b-0a15d6a2d334",
    "name": "verify",
    "identity_class": "events",
}
OPTION = json.dumps(DATA_SOURCE)


class TestTransformQuery(unittest.TestCase, object):
    @staticmethod
    def get_first(itr, constraint):
        return next((obj for obj in itr if constraint(obj)), None)

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestTransformQuery.get_first(
            itr, lambda o: type(o) == dict and o.get("type") == typ
        )

    @staticmethod
    def get_object_keys(objects):
        for k, v in objects.items():
            if k == "type":
                yield v
            elif isinstance(v, dict):
                for id_val in TestTransformQuery.get_object_keys(v):
                    yield id_val

    def test_oca_event(self):
        data = [
            {
                "continent_name": "Asia",
                "city_name": "Kolkata",
                "country_iso_code": "IN",
                "ip": "47.15.98.56",
                "country_name": "India",
                "region_name": "West Bengal",
                "location": {"lon": "88.3697", "lat": "22.5697"},
                "result": "success",
                "subtype": "saml",
                "providerid": "https://portal.baneandox.org:443/SAML20/SP",
                "origin": "47.15.98.56",
                "realm": "www.ibm.com",
                "applicationid": "6773634223410562472",
                "userid": "652001LT0R",
                "applicationtype": "Custom Application",
                "devicetype": "PAN GlobalProtect/5.2.4-21 (Microsoft Windows 10 Enterprise , 64-bit) Mozilla/5.0 (Windows NT 6.2; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
                "username": "dinepal1@in.ibm.com",
                "applicationname": "Bane & Ox VPN",
                "year": 2022,
                "billingid": "12345",
                "mdmismanaged": "true",
                "mdmiscompliant": "true",
                "deviceid": "abc_device",
                "@metadata": {
                    "group_id": "event-transform-prod-eu01a-prod-eu01a-01",
                    "source_dc": "prod-eu01a",
                },
                "event_type": "sso",
                "month": 1,
                "indexed_at": 1642413142906,
                "@processing_time": 1012,
                "tenantid": "c92ce528-293f-4e84-8307-c4fe188b9461",
                "tenantname": "isrras.ice.ibmcloud.com",
                "correlationid": "CORR_ID-a134f569-8d73-45ac-8d44-2457448c9101",
                "servicename": "saml_runtime",
                "id": "dc4523e6-6260-4349-83f8-3320365a5f25",
                "time": 1642413141894,
                "day": 17,
            }
        ]

        user_ref = "2"
        category = "sso"
        domain_ref = "3"
        module = "saml_runtime"
        extensions_user_id = "652001LT0R"
        result_bundle = entry_point.translate_results(
            json.dumps(DATA_SOURCE), json.dumps(data)
        )
        observed_data = result_bundle["objects"][1]
        objects = observed_data["objects"]

        event = TestTransformQuery.get_first_of_type(objects.values(), "x-oca-event")

        assert (event["type"]) == "x-oca-event"
        assert event["user_ref"] == user_ref
        assert event["category"] == category
        assert event["domain_ref"] == domain_ref
        assert event["module"] == module
        assert event["category"] == category
        assert event["extensions"]["x-iam-ext"]["is_device_managed"] == "true"
        assert event["extensions"]["x-iam-ext"]["mdm_customerid"] == "12345"
        assert event["extensions"]["x-iam-ext"]["is_device_compliant"] == "true"
        assert event["extensions"]["x-iam-ext"]["deviceid"] == "abc_device"
