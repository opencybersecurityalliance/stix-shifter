from stix_shifter.src.json_to_stix import json_to_stix_translator
from stix_shifter.src import transformers
from stix_shifter.src.modules.qradar import qradar_translator
import json

interface = qradar_translator.Translator()
map_file = open(interface.mapping_filepath).read()
map_data = json.loads(map_file)


class TestTransform(object):

    def test_common_prop(self):
        data_source = {'id': '123', 'name': 'sourcename', 'type': 'sourcetype'}
        transformer = None
        options = {}
        data = {"time": "2018-03-20T13:54:59.952Z"}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert(result_bundle is not None)
        assert(result_bundle['type'] == 'bundle')

    def test_simple_props(self):
        data_source = {
            'id': '123',
            'name': 'sourcename',
            'type': 'sourcetype'
        }
        transformer = None
        options = {}
        payload = "SomeBase64Payload"
        url = "https://example.com"
        domain = "example.com"
        source_ip = "127.0.0.1"
        data = {"sourceip": source_ip, "url": url,
                "domain": domain, "payload": payload, "starttime": 1531169112}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)

        assert(result_bundle is not None)
        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        assert(result_bundle_objects is not None)

        result_bundle_identity = result_bundle_objects[0]
        assert(result_bundle_identity['type'] == 'identity')
        assert(result_bundle_identity['id'] ==
               'identity--' + data_source['id'])
        assert(result_bundle_identity['name'] == data_source['name'])
        assert(result_bundle_identity['identity_class'] == data_source['type'])

        observed_data = result_bundle_objects[1]
        assert(observed_data is not None)
        assert(observed_data['created'] is not None)
        assert(observed_data['type'] == "observed-data")
        assert(observed_data['created_by_ref'] == result_bundle_identity['id'])

        assert('objects' in observed_data)
        objects = observed_data['objects']

        for key, value in objects.items():
            assert(int(key) in list(range(0, len(objects))))
            if(value['type'] == 'ipv4-addr'):
                assert(
                    value['value'] == source_ip), "Wrong value returned " + key + ":" + str(value)
            elif(value['type'] == 'url'):
                assert(value['value'] == url), "Wrong value returned " + \
                    key + ":" + str(value)
            elif(value['type'] == 'domain-name'):
                assert(
                    value['value'] == domain), "Wrong value returned " + key + ":" + str(value)
            elif(value['type'] == 'artifact'):
                assert(
                    value['payload_bin'] == payload), "Wrong value returned " + key + ":" + str(value)
            # should not be returned, still needs to be fixed in logic
            elif(value['type'] == 'ipv6-addr'):
                assert(
                    value['value'] == source_ip), "Wrong value returned " + key + ":" + str(value)
            elif(value['type'] == 'network-traffic'):
                assert(int(value['src_ref']) in list(
                    range(0, len(objects)))), "Wrong value returned " + key + ":" + str(value)
            else:
                assert(False), "Returned a non-mapped value " + \
                    key + ":" + str(value)

        assert(result_bundle_identity['name'] == data_source['name'])
        assert(result_bundle_identity['identity_class'] == data_source['type'])

    # def test_to_string_transformer(self):
    #     data_source = {'id': '123', 'name': 'sourcename'}
    #     map_data = {
    #         "sourceip": [
    #             {
    #                 "key": "ipv4-addr.value",
    #                 "cybox": "true",
    #                 "type": "value"
    #             },
    #             {
    #                 "key": "ipv6-addr.value",
    #                 "cybox": "true",
    #                 "type": "value"
    #             },
    #             {
    #                 "key": "network-traffic.src_ref",
    #                 "type": "reference",
    #                 "references": "ipv4-addr",
    #                 "cybox": "true",
    #                 "linked": "network-traffic",
    #                 "transformer": "ToString"
    #             }
    #         ],
    #         "destinationip": [
    #             {
    #                 "key": "ipv4-addr.value",
    #                 "cybox": "true",
    #                 "type": "value"
    #             },
    #             {
    #                 "key": "ipv6-addr.value",
    #                 "cybox": "true",
    #                 "type": "value"
    #             },
    #             {
    #                 "key": "network-traffic.dst_ref",
    #                 "type": "reference",
    #                 "references": "ipv6-addr",
    #                 "cybox": "true",
    #                 "linked": "network-traffic",
    #                 "transformer": "ToString"
    #             }
    #         ]
    #     }
    #     options = {}
    #     data = [{"sourceip": "1.1.1.1", "destinationip": "2.2.2.2"}]
    #     result = json_to_stix_translator.convert_to_stix(
    #         data_source, map_data, data, transformers.get_all_transformers(), options)[0]
    #     assert(result is not None)
    #     assert('objects' in result)
    #     objects = result['objects']
    #     assert(len(objects) == 3)

    #     result = json_to_stix_translator.convert_to_stix(
    #         data_source, map_data, data, transformers.get_all_transformers(), options)['objects'][1]

        # assert('1' in objects)  # sourceip
        # object1 = objects['1']
        # assert(object1['type'] == 'ipv6-addr')
        # assert(object1['value'] == "2.2.2.2")

        # assert('2' in objects)
        # object2 = objects['2']
        # assert(object2['src_ref'] == '0')
        # assert(object2['dst_ref'] == '1')
        # assert(object2['type'] == 'network-traffic')

    # def test_custom_props(self):
    #     # data_source = {'id': '123', 'name': 'sourcename', 'type': 'sourcetype'}
    #     map_data = {"protocolid": {
    #         "key": "x-com-ibm-ariel.protocol_id",
    #         "type": "value",
    #         "linked": "ariel"
    #     }, "logsourceid": {
    #         "key": "x-com-ibm-ariel.log_source_id",
    #         "type": "value",
    #         "linked": "ariel"
    #     }, "qid": {
    #         "key": "x-com-ibm-ariel.qid",
    #         "type": "value",
    #         "linked": "ariel"
    #     }, "magnitude": {
    #         "key": "x-com-ibm-ariel.magnitude",
    #         "type": "value",
    #         "linked": "ariel"
    #     }, "identityip": {
    #         "key": "x-com-ibm-ariel.identity_ip",
    #         "type": "value",
    #         "linked": "ariel"
    #     }, "test_linked_value_1": {
    #         "key": "x-com-ibm-test-linked-value.value_one",
    #         "type": "value",
    #         "linked": "testlinked"
    #     }, "test_linked_value_2": {
    #         "key": "x-com-ibm-test-linked-value.value_two",
    #         "type": "value",
    #         "linked": "testlinked"
    #     }}
    #     transformer = None
    #     options = {}
    #     data = {"protocolid": 255, "logsourceid": 126, "qid": 55500004,
    #             "identityip": "0.0.0.0", "magnitude": 4, "test_linked_value_1": 1, "test_linked_value_2": 2}
    #     x = json_to_stix_translator.DataSourceObjToStixObj(
    #         map_data, transformer, options)
    #     result = x.transform(data)
    #     assert(result is not None)
    #     assert('x_com_ibm_ariel' in result)
    #     attributes = result['x_com_ibm_ariel']
    #     assert(attributes['identity_ip'] == '0.0.0.0')
    #     assert(attributes['log_source_id'] == 126)
    #     assert(attributes['qid'] == 55500004)
    #     assert(attributes['magnitude'] == 4)
    #     assert(attributes['protocol_id'] == 255)

    #     assert('x_com_ibm_test_linked_value' in result)
    #     attributes = result['x_com_ibm_test_linked_value']
    #     assert(attributes['value_one'] == 1)
    #     assert(attributes['value_two'] == 2)

    # def test_to_integer_transformer(self):
    #     data_source = {'id': '123', 'name': 'sourcename', 'type': 'sourcetype'}
    #     map_data = {
    #         "eventCount": {
    #             "key": "number_observed",
    #             "type": "value",
    #             "transformer": "ToInteger"
    #         },
    #     }
    #     options = {}
    #     data = [{"eventCount": "5"}]
    #     result = json_to_stix_translator.convert_to_stix(
    #         data_source, map_data, data, transformers.get_all_transformers(), options)['objects'][1]
    #     assert(result is not None)
    #     assert('objects' in result)
    #     objects = result['objects']
    #     assert(len(objects) == 0)
    #     assert('number_observed' in result)
    #     assert(result['number_observed'] == 5)

    # def test_to_integer_transformer_error(self):
    #     data_source = {'id': '123', 'name': 'sourcename', 'type': 'sourcetype'}
    #     map_data = {
    #         "eventCount": {
    #             "key": "number_observed",
    #             "type": "value",
    #             "transformer": "ToInteger"
    #         },
    #     }
    #     options = {}
    #     data = [{"eventCount": "notaValidNumber"}]
    #     result = json_to_stix_translator.convert_to_stix(
    #         data_source, map_data, data, transformers.get_all_transformers(), options)['objects'][1]
    #     assert(result is not None)
    #     assert('number_observed' not in result)

    # def test_to_string_transformer(self):
    #     data_source = {'id': '123', 'name': 'sourcename', 'type': 'sourcetype'}
    #     map_data = {
    #         "destinationip": [
    #             {
    #                 "key": "ipv4-addr.value",
    #                 "type": "value"
    #             },
    #             {
    #                 "key": "ipv6-addr.value",
    #                 "type": "value"
    #             },
    #             {
    #                 "key": "network-traffic.dst_ref",
    #                 "type": "reference",
    #                 "linked": "nt",
    #                 "transformer": "ToString"
    #             }
    #         ],
    #         "sourceip": [
    #             {
    #                 "key": "ipv4-addr.value",
    #                 "type": "value"
    #             },
    #             {
    #                 "key": "ipv6-addr.value",
    #                 "type": "value"
    #             },
    #             {
    #                 "key": "network-traffic.src_ref",
    #                 "type": "reference",
    #                 "linked": "nt",
    #                 "transformer": "ToString"
    #             }
    #         ]
    #     }
    #     options = {}
    #     data = [{"sourceip": "1.1.1.1", "destinationip": "2.2.2.2"}]
    #     result = json_to_stix_translator.convert_to_stix(
    #         data_source, map_data, data, transformers.get_all_transformers(), options)['objects'][1]
    #     assert(result is not None)
    #     assert('objects' in result)
    #     objects = result['objects']
    #     assert(len(objects) == 3)

    #     assert('0' in objects)  # destinationip
    #     object0 = objects['0']
    #     assert(object0['type'] == 'ipv4-addr')
    #     assert(object0['value'] == "2.2.2.2")

    #     assert('1' in objects)  # sourceip
    #     object1 = objects['1']
    #     assert(object1['type'] == 'ipv4-addr')
    #     assert(object1['value'] == "1.1.1.1")

    #     assert('2' in objects)
    #     object2 = objects['2']
    #     assert(object2['dst_ref'] == '0')
    #     assert(object2['src_ref'] == '1')
    #     assert(object2['type'] == 'network-traffic')

    # def test_to_array_transformer(self):
    #     data_source = {'id': '123', 'name': 'sourcename', 'type': 'sourcetype'}
    #     map_data = {
    #         "destinationport": {
    #             "key": "network-traffic.dst_port",
    #             "cybox": "true",
    #             "linked": "nt",
    #             "type": "value"
    #         },
    #         "sourceport": {
    #             "key": "network-traffic.src_port",
    #             "cybox": "true",
    #             "type": "value",
    #             "linked": "nt"
    #         },
    #         "protocol": {
    #             "key": "network-traffic.protocols",
    #             "cybox": "true",
    #             "type": "value",
    #             "linked": "nt",
    #             "transformer": "ToArray"
    #         }
    #     }
    #     test_data = [
    #         {"protocol": "TCP", "sourceport": 1, "destinationport": 2}]
    #     options = {}

    #     result = json_to_stix_translator.convert_to_stix(data_source, map_data, test_data,
    #                                                      transformers.get_all_transformers(), options)['objects'][1]

    #     assert(result is not None)
    #     assert('objects' in result)
    #     objects = result['objects']

    #     assert('0' in objects)
    #     network_traffic = objects['0']
    #     assert(network_traffic['src_port'] == 1)
    #     assert(network_traffic['dst_port'] == 2)
    #     assert(isinstance(network_traffic['protocols'], list))
    #     assert(network_traffic['protocols'][0] == 'tcp')
