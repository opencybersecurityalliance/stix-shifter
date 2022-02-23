import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.alertflex.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "alertflex"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "Alertflex",
    "identity_class": "events"
}
options = {}


class TestAlertflexResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for alertflex translate results
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
        return TestAlertflexResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def test_common_property():
        """
        to test the common stix object properties
        """
        data = {'severity': 2,
                'srcip': '0.0.0.0',
                'agent': 'alertflex',
                'create_time': 1597867109000,
                'dstport': 0,
                'description': 'Integrity checksum changed.',
                'source': 'Wazuh',
                'type': 'FILE',
                'sha1': '6232e4a0f37b583182aad75d18b3a4147a54f85b',
                'node': 'test01',
                'protocol': 'ip',
                'file': '/etc/altprobe/altprobe.yaml',
                'srcport': 0,
                'dstip': '0.0.0.0',
                'event': '550',
                'category': 'ossec, syscheck, pci_dss_11.5, hipaa_164.312.c.1, hipaa_164.312.c.2, gdpr_II_5.1.f, nist_800_53_SI.7',
                'user': 'indef',
                'info': 'File /etc/altprobe/altprobe.yaml',
                'md5': '7d351ff6fea9e9dc100b7deb0e03fd35'}
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
    def test_stix_property():
        """
        to test the common stix object properties
        """
        data = {'severity': 2,
                'srcip': '0.0.0.0',
                'agent': 'alertflex',
                'create_time': 1597867109000,
                'dstport': 0,
                'description': 'Integrity checksum changed.',
                'source': 'Wazuh',
                'type': 'FILE',
                'sha1': '6232e4a0f37b583182aad75d18b3a4147a54f85b',
                'node': 'test01',
                'protocol': 'ip',
                'file': '/etc/altprobe/altprobe.yaml',
                'srcport': 0,
                'dstip': '0.0.0.0',
                'event': '550',
                'category': 'ossec, syscheck, pci_dss_11.5, hipaa_164.312.c.1, hipaa_164.312.c.2, gdpr_II_5.1.f, nist_800_53_SI.7',
                'user': 'indef',
                'info': 'File /etc/altprobe/altprobe.yaml',
                'md5': '7d351ff6fea9e9dc100b7deb0e03fd35'}
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
        objects_data = observed_data['objects']

        ipv4_addr_data = objects_data['1']
        assert ipv4_addr_data['type'] == "ipv4-addr"
        assert ipv4_addr_data['value'] == "0.0.0.0"

        ipv4_addr_data = objects_data['2']
        assert ipv4_addr_data['type'] == "network-traffic"
        assert ipv4_addr_data['src_ref'] == '1'
        assert ipv4_addr_data['src_port'] == 0
        assert ipv4_addr_data['dst_ref'] == '4'
        assert ipv4_addr_data['dst_port'] == 0

        file_data = objects_data['3']
        assert file_data['type'] == "file"
        assert file_data['name'] == "/etc/altprobe/altprobe.yaml"
        hashes_data = file_data['hashes']
        assert hashes_data['SHA-1'] == '6232e4a0f37b583182aad75d18b3a4147a54f85b'
        assert hashes_data['MD5'] == '7d351ff6fea9e9dc100b7deb0e03fd35'

        ipv4_addr_data = objects_data['4']
        assert ipv4_addr_data['type'] == "ipv4-addr"
        assert ipv4_addr_data['value'] == "0.0.0.0"

        user_data = objects_data['5']
        assert user_data['type'] == "user-account"
        assert user_data['user_id'] == "indef"


    @staticmethod
    def test_custom_property():
        """
        to test the custom stix object properties
        """
        data = {'severity': 2,
                'srcip': '0.0.0.0',
                'agent': 'alertflex',
                'create_time': 1597867109000,
                'dstport': 0,
                'description': 'Integrity checksum changed.',
                'source': 'Wazuh',
                'type': 'FILE',
                'sha1': '6232e4a0f37b583182aad75d18b3a4147a54f85b',
                'node': 'test01',
                'protocol': 'ip',
                'file': '/etc/altprobe/altprobe.yaml',
                'srcport': 0,
                'dstip': '0.0.0.0',
                'event': '550',
                'category': 'ossec, syscheck, pci_dss_11.5, hipaa_164.312.c.1, hipaa_164.312.c.2, gdpr_II_5.1.f, nist_800_53_SI.7',
                'user': 'indef',
                'info': 'File /etc/altprobe/altprobe.yaml',
                'md5': '7d351ff6fea9e9dc100b7deb0e03fd35'}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        observed_data = result_bundle_objects[1]

        objects = observed_data['objects']
        alert_flex_obj = TestAlertflexResultsToStix.get_first_of_type(objects.values(), 'x-org-alertflex')
        assert alert_flex_obj is not None, 'x-org-alertflex object type not found'
        assert alert_flex_obj.keys() == {'severity', 'agent', 'description', 'source', 'type', 'node', 'event', 'category', 'info', 'finding_type'}
        assert alert_flex_obj['severity'] == 2
        assert alert_flex_obj['agent'] == 'alertflex'
        assert alert_flex_obj['description'] == 'Integrity checksum changed.'
        assert alert_flex_obj['source'] == 'Wazuh'
        assert alert_flex_obj['finding_type'] == 'FILE'
        assert alert_flex_obj['node'] == 'test01'
        assert alert_flex_obj['event'] == '550'
        assert alert_flex_obj['category'] == 'ossec, syscheck, pci_dss_11.5, hipaa_164.312.c.1, hipaa_164.312.c.2, gdpr_II_5.1.f, nist_800_53_SI.7'
        assert alert_flex_obj['info'] == 'File /etc/altprobe/altprobe.yaml'

    @staticmethod
    def test_unmapped_attribute_alone():
        data = {"unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']
        assert objects == {}
