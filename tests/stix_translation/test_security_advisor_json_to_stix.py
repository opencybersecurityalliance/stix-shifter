import json
from stix_shifter.stix_translation.src.utils import transformers
from stix_shifter.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter.stix_translation.src.modules.security_advisor import security_advisor_translator
from stix_shifter.stix_translation import stix_translation


import unittest

interface = security_advisor_translator.Translator()
map_file = open(interface.mapping_filepath).read()
map_data = json.loads(map_file)
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "BigFix",
    "identity_class": "events"
}
options = {}

class TestSecurityAdvisorResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for bigfix translate results
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
        return TestSecurityAdvisorResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    def test_common_prop(self):
        """
        to test the common stix object properties
        """
        data = { 'createTime' : '2019-10-31T11:15:55.099615Z' , 'updateTime' : '2019-10-31T11:15:55.099635Z',
                 'occurence_count': 1 }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
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

        assert observed_data['first_observed'] is not None
        assert (observed_data['first_observed'] == data['createTime'] )

        assert observed_data['last_observed'] is not None
        assert (observed_data['last_observed'] == data['updateTime'] )

        assert observed_data['number_observed'] is not None
        assert (observed_data['number_observed'] == data['occurence_count'] )

    def test_cybox_observables(self):

        data = { 
                    'author_id': 'IBMid-123',
                    'email': 'test@gmail.com',
                }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        curr_obj = TestSecurityAdvisorResultsToStix.get_first_of_type(objects.values(), 'user-account')
        assert(curr_obj is not None), 'user-account object type not found'
        assert(curr_obj.keys() == {'type', 'user_id'})
        assert(curr_obj['user_id'] == data['author_id'])

        curr_obj = TestSecurityAdvisorResultsToStix.get_first_of_type(objects.values(), 'email-addr')
        assert(curr_obj is not None), 'eamil-addr object type not found'
        assert(curr_obj.keys() == {'type', 'value'})
        assert(curr_obj['value'] == data['email'])

    def test_custom_property(self):
        """
        to test the custom stix object properties
        """
        data = {
                'author_accountId': 'test_id_1',
                'name': 'test_id_1/providers/sec_adv/occurrences/853092',
                'id': '853092', 'noteName': 'test_id_1/providers/sec_adv/notes/cert_mngr',
                'updateTime': '2019-10-31T11:15:55.099635Z', 'createTime': '2019-10-31T11:15:55.099615Z',
                'shortDescription': 'testing data tranlation',
                'providerId': 'sec_adv', 'providerName': 'test_id_1/providers/sec_adv',
                'longDescription': 'testing data tranlation', 'context_accountId': 'test_id_1',
                'context_resourceName': 'mycluster', 'reportedBy_id': 'cert_mngr',
                'reportedBy_title': 'Security Advisor', 'finding_severity': 'MEDIUM',
                'finding_certainty': 'HIGH', 'occurence_count': 1
            }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        observed_data = result_bundle_objects[1]

        custom_props = observed_data['x_com_security_advisor_finding']
        assert(custom_props['author_accountId'] == data['author_accountId'])

        assert(custom_props['name'] == data['name'])
        assert(custom_props['noteName'] == data['noteName'])
        assert(custom_props['shortDescription'] == data['shortDescription'])
        assert(custom_props['longDescription'] == data['longDescription'])
        assert(custom_props['context_accountId'] == data['context_accountId'])
        assert(custom_props['context_resourceName'] == data['context_resourceName'])
        assert(custom_props['finding_severity'] == data['finding_severity'])
        assert(custom_props['finding_certainty'] == data['finding_certainty'])

        assert(custom_props['providerId'] == data['providerId'])
        assert(custom_props['providerName'] == data['providerName'])
        assert(custom_props['reportedBy_id'] == data['reportedBy_id'])
        assert(custom_props['reportedBy_title'] == data['reportedBy_title'])

    def test_custom_mapping(self):
        data_source_string = json.dumps(data_source)
        data = [{
                    'author_id': 'IBMid-123',
                    'author_email': 'test@gmail.com', 
                    'name': 'test_id_1/providers/sec_adv/occurrences/853092',
                    'id': '853092', 
                }]
        data_string = json.dumps(data)

        options = {"mapping": {
            "author_id": {"key": "user-account.user_id"},
            "id": {"key": "x_finding.id", "cybox": False},
            "name": {"key": "x_finding.name", "cybox": False},
            "author_email": {"key": "email-addr.value"},
        }}

        translation = stix_translation.StixTranslation()
        result = translation.translate('security_advisor', 'results', data_source_string, data_string, options)
        result_bundle = json.loads(result)

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        curr_obj = TestSecurityAdvisorResultsToStix.get_first_of_type(objects.values(), 'user-account')
        assert(curr_obj is not None), 'user-account object type not found'
        assert(curr_obj.keys() == {'type', 'user_id'})
        assert(curr_obj['user_id'] == data[0]['author_id'])

        curr_obj = TestSecurityAdvisorResultsToStix.get_first_of_type(objects.values(), 'email-addr')
        assert(curr_obj is not None), 'email-addr object type not found'
        assert(curr_obj.keys() == {'type', 'value'})
        assert(curr_obj['value'] == "test@gmail.com")

    def test_unmapped_attribute_with_mapped_attribute(self):
        accountId = 'test_id_1',
        data = {"author_accountId": accountId, "unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert ('objects' in observed_data)
        objects = observed_data['objects']
        assert (objects == {})
        curr_obj = TestSecurityAdvisorResultsToStix.get_first_of_type(objects.values(), 'author_accountId')
        assert (curr_obj is None), 'author_accountId object type not found'

    def test_unmapped_attribute_alone(self):
        data = {"unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert ('objects' in observed_data)
        objects = observed_data['objects']
        assert (objects == {})
