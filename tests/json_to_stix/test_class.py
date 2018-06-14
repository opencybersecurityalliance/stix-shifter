from stix_shifter.src.json_to_stix import json_to_stix_translator
from stix_shifter.src import transformers


class TestTransform(object):
    def test_common_prop(self):
        datasource = {'id': '123', 'name': 'sourcename'}
        map_data = {"time": {
            "key": "created",
            "type": "value"
        }}
        transformer = None
        options = {}
        data = {"time": "2018-03-20T13:54:59.952Z"}
        x = json_to_stix_translator.DataSourceObjToStixObj(
            datasource, map_data, transformer, options)
        result = x.transform(data)
        assert(result is not None)
        assert('created' in result)
        assert(result['created'] == data["time"])
        assert(result['type'] == "observed-data")
        assert('x_com_ibm_uds_datasource' in result)
        assert(result['x_com_ibm_uds_datasource']
               ['id'] == datasource['id'])
        assert(result['x_com_ibm_uds_datasource']
               ['name'] == datasource['name'])

    def test_observation_prop(self):
        datasource = {'id': '123', 'name': 'sourcename'}
        map_data = {"time": {
            "key": "first_observed",
            "type": "value"
        }}
        transformer = None
        options = {}
        data = {"time": "2018-03-20T13:54:59.952Z"}
        x = json_to_stix_translator.DataSourceObjToStixObj(
            datasource, map_data, transformer, options)
        result = x.transform(data)
        assert(result is not None)
        assert('first_observed' in result)
        assert(result['first_observed'] == data["time"])
        assert(result['type'] == "observed-data")
        assert('x_com_ibm_uds_datasource' in result)
        assert(result['x_com_ibm_uds_datasource']
               ['id'] == datasource['id'])
        assert(result['x_com_ibm_uds_datasource']
               ['name'] == datasource['name'])

    def test_simple_props(self):
        datasource = {'id': '123', 'name': 'sourcename'}
        map_data = {"ip": {
            "key": "ipv4-addr.value",
            "type": "value"
        }, "url": {"key": "url.value",
                   "type": "value"},
            "domain": {
            "key": "domain-name.value",
            "type": "value"
        }
        }
        transformer = None
        options = {}
        data = {"ip": "127.0.0.1", "url": "https://example.com",
                "domain": "example.com"}
        x = json_to_stix_translator.DataSourceObjToStixObj(
            datasource, map_data, transformer, options)
        result = x.transform(data)
        assert(result is not None)
        assert('objects' in result)
        objects = result['objects']
        assert('0' in objects)
        object0 = objects['0']
        assert(object0['type'] == 'ipv4-addr')
        assert(object0['value'] == "127.0.0.1")
        assert('1' in objects)
        object1 = objects['1']
        assert(object1['type'] == 'url')
        assert(object1['value'] == "https://example.com")
        assert('2' in objects)
        object2 = objects['2']
        assert(object2['type'] == 'domain-name')
        assert(object2['value'] == "example.com")

    def test_custom_props(self):
        datasource = {'id': '123', 'name': 'sourcename'}
        map_data = {"protocolid": {
            "key": "x-com-ibm-ariel.protocol_id",
            "type": "value",
            "linked": "ariel"
        }, "logsourceid": {
            "key": "x-com-ibm-ariel.log_source_id",
            "type": "value",
            "linked": "ariel"
        }, "qid": {
            "key": "x-com-ibm-ariel.qid",
            "type": "value",
            "linked": "ariel"
        }, "magnitude": {
            "key": "x-com-ibm-ariel.magnitude",
            "type": "value",
            "linked": "ariel"
        }, "identityip": {
            "key": "x-com-ibm-ariel.identity_ip",
            "type": "value",
            "linked": "ariel"
        }, "test_linked_value_1": {
            "key": "x-com-ibm-test-linked-value.value_one",
            "type": "value",
            "linked": "testlinked"
        }, "test_linked_value_2": {
            "key": "x-com-ibm-test-linked-value.value_two",
            "type": "value",
            "linked": "testlinked"
        }}
        transformer = None
        options = {}
        data = {"protocolid": 255, "logsourceid": 126, "qid": 55500004,
                "identityip": "0.0.0.0", "magnitude": 4, "test_linked_value_1": 1, "test_linked_value_2": 2}
        x = json_to_stix_translator.DataSourceObjToStixObj(
            datasource, map_data, transformer, options)
        result = x.transform(data)
        assert(result is not None)
        assert('x_com_ibm_ariel' in result)
        attributes = result['x_com_ibm_ariel']
        assert(attributes['identity_ip'] == '0.0.0.0')
        assert(attributes['log_source_id'] == 126)
        assert(attributes['qid'] == 55500004)
        assert(attributes['magnitude'] == 4)
        assert(attributes['protocol_id'] == 255)

        assert('x_com_ibm_test_linked_value' in result)
        attributes = result['x_com_ibm_test_linked_value']
        assert(attributes['value_one'] == 1)
        assert(attributes['value_two'] == 2)

    def test_to_integer_transformer(self):
        datasource = {'id': '123', 'name': 'sourcename'}
        map_data = {
            "eventCount": {
                "key": "number_observed",
                "type": "value",
                "transformer": "ToInteger"
            },
        }
        options = {}
        data = [{"eventCount": "5"}]
        result = json_to_stix_translator.convert_to_stix(
            datasource, map_data, data, transformers.get_all_transformers(), options)[0]
        assert(result is not None)
        assert('objects' in result)
        objects = result['objects']
        assert(len(objects) == 0)
        assert('number_observed' in result)
        assert(result['number_observed'] == 5)

    def test_to_integer_transformer_error(self):
        datasource = {'id': '123', 'name': 'sourcename'}
        map_data = {
            "eventCount": {
                "key": "number_observed",
                "type": "value",
                "transformer": "ToInteger"
            },
        }
        options = {}
        data = [{"eventCount": "notaValidNumber"}]
        result = json_to_stix_translator.convert_to_stix(
            datasource, map_data, data, transformers.get_all_transformers(), options)[0]
        assert(result is not None)
        assert('number_observed' not in result)

    def test_to_string_transformer(self):
        datasource = {'id': '123', 'name': 'sourcename'}
        map_data = {
            "destinationip": [
                {
                    "key": "ipv4-addr.value",
                    "type": "value"
                },
                {
                    "key": "ipv6-addr.value",
                    "type": "value"
                },
                {
                    "key": "network-traffic.dst_ref",
                    "type": "reference",
                    "linked": "nt",
                    "transformer": "ToString"
                }
            ],
            "sourceip": [
                {
                    "key": "ipv4-addr.value",
                    "type": "value"
                },
                {
                    "key": "ipv6-addr.value",
                    "type": "value"
                },
                {
                    "key": "network-traffic.src_ref",
                    "type": "reference",
                    "linked": "nt",
                    "transformer": "ToString"
                }
            ]
        }
        options = {}
        data = [{"sourceip": "1.1.1.1", "destinationip": "2.2.2.2"}]
        result = json_to_stix_translator.convert_to_stix(
            datasource, map_data, data, transformers.get_all_transformers(), options)[0]
        assert(result is not None)
        assert('objects' in result)
        objects = result['objects']
        assert(len(objects) == 3)

        assert('0' in objects)  # destinationip
        object0 = objects['0']
        assert(object0['type'] == 'ipv4-addr')
        assert(object0['value'] == "2.2.2.2")

        assert('1' in objects)  # sourceip
        object1 = objects['1']
        assert(object1['type'] == 'ipv4-addr')
        assert(object1['value'] == "1.1.1.1")

        assert('2' in objects)
        object2 = objects['2']
        assert(object2['dst_ref'] == '0')
        assert(object2['src_ref'] == '1')
        assert(object2['type'] == 'network-traffic')
