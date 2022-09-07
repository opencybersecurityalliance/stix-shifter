""" test script to perform unit test case for rhacs translate results """
import unittest
from stix_shifter_modules.rhacs.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "rhacs"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "rhacs",
    "identity_class": "events"
}
options = {}

data = {
            "findingType": "violation",
            "alertId": "474037ca-e615-4f16-b50c-f8197b9d37ae",
            "policyName": "Unauthorized Network Flow",
            "policyId": "1b74ffdd-8e67-444c-9814-1c23863c8ccb",
            "description": "This policy generates a violation for the network "
                           "flows that fall outside baselines for "
                           "which \"alert on anomalous violations\" is set.",
            "rationale": "The network baseline is a list of flows that are "
                         "allowed, and once it is frozen, any flow outside that is a concern.",
            "remediation": "Evaluate this network flow. If deemed to be okay, "
                           "add it to the baseline. If not, investigate further as required.",
            "disabled": False,
            "categories": [
                "Anomalous Activity"
            ],
            "severity": "HIGH_SEVERITY",
            "eventSource": "DEPLOYMENT_EVENT",
            "sortName": "Unauthorized Network Flow",
            "sortLifecycleStage": "RUNTIME",
            "lifecycleStage": "RUNTIME",
            "clusterId": "fdbec9d7-5913-4ad0-8bb7-404386e311a8",
            "cluster": "cp4s-cluster",
            "namespace": "sample-app1",
            "namespaceId": "2c91b5dc-bf07-4075-ab54-568ecd40c584",
            "violationState": "ACTIVE",
            "deployment": "postgresql",
            "deploymentId": "ac359411-1c5d-4e5a-9283-d651f3f7f246",
            "inactive": False,
            "firstObserved": "2022-09-06T13:29:30.352918776Z",
            "lastObserved": "2022-09-06T13:29:30.352918776Z",
            "violationMessage": "Unexpected network flow found in deployment. "
                                "Source name: \"django-psql-persistent\". "
                                "Destination name: \"postgresql\". "
                                "Destination port: \"5432\". Protocol: \"L4_PROTOCOL_TCP\".",
            "containerName": "postgresql",
            "containerImage": {
                "id": "sha256:1896ab7cbfc4ade742b23ca45f410a1c58a520095c2507619c3346afec125ecc",
                "name": {
                    "registry": "image-registry.openshift-image-registry.svc:5000",
                    "remote": "openshift/postgresql",
                    "tag": "",
                    "fullName": "image-registry.openshift-image-registry.svc:5000/openshift/postgr"
                                "esql@sha256:1896ab7cbfc4ade742b23ca45f410a1"
                                "c58a520095c2507619c3346afec125ecc"
                }
            },
            "networkFlow": {
                "netflow_protocol": "L4_PROTOCOL_TCP",
                "netflow_source": {
                    "name": "django-psql-persistent",
                    "entity_type": "DEPLOYMENT",
                    "deployment_namespace": "sample-app1",
                    "deployment_type": "DeploymentConfig",
                    "port": 0
                },
                "netflow_destination": {
                    "name": "postgresql",
                    "entity_type": "DEPLOYMENT",
                    "deployment_namespace": "sample-app1",
                    "deployment_type": "DeploymentConfig",
                    "port": 5432
                }
            }
        }


class TestRhacsResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for rhacs translate results
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
        return TestRhacsResultsToStix.get_first(itr,
                                                lambda o: isinstance(o, dict) and
                                                o.get('type') == typ)

    def test_common_prop(self):
        """to test common stix object properties"""

        result_bundle = json_to_stix_translator.convert_to_stix(data_source, map_data, [data],
                                                                get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert observed_data is not None
        assert observed_data['id'] is not None
        assert observed_data['type'] == "observed-data"
        assert observed_data['created_by_ref'] == result_bundle_identity['id']
        assert observed_data['first_observed'] is not None
        assert observed_data['last_observed'] is not None
        assert observed_data['number_observed'] is not None

    def test_x_rhacs_cluster_json_to_stix(self):
        """  to test x-rhacs-cluster stix object properties  """

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        cluster_obj = TestRhacsResultsToStix.get_first_of_type(objects.values(), 'x-rhacs-cluster')

        assert cluster_obj is not None
        assert cluster_obj['name'] == 'cp4s-cluster'
        assert cluster_obj['cluster_id'] == 'fdbec9d7-5913-4ad0-8bb7-404386e311a8'
        assert cluster_obj['namespace'] == 'sample-app1'
        assert cluster_obj['namespace_id'] == '2c91b5dc-bf07-4075-ab54-568ecd40c584'

    def test_x_rhacs_deployment_json_to_stix(self):
        """to test x-rhacs-deployment stix object properties"""

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        deployment_obj = TestRhacsResultsToStix.get_first_of_type(objects.values(), 'x-rhacs-deployment')
        assert deployment_obj is not None
        assert deployment_obj['deployment_name'] == 'postgresql'
        assert deployment_obj['deployment_id'] == 'ac359411-1c5d-4e5a-9283-d651f3f7f246'

    def test_x_ibm_finding_json_to_stix(self):
        """to test x-ibm-finding stix object properties"""

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        finding_obj = TestRhacsResultsToStix.get_first_of_type(objects.values(),
                                                               'x-ibm-finding')
        assert finding_obj is not None
        assert finding_obj["type"] == 'x-ibm-finding'
        assert finding_obj["finding_type"] == 'violation'
        assert finding_obj["extensions"]['x-rhacs-finding']['alert_id'] == \
               '474037ca-e615-4f16-b50c-f8197b9d37ae'
        assert finding_obj["extensions"]['x-rhacs-finding']['lifecycle_stage'] == 'RUNTIME'
        assert finding_obj["extensions"]['x-rhacs-finding']['violation_state'] == 'ACTIVE'
        assert finding_obj['name'] == 'Unauthorized Network Flow'
        assert finding_obj['severity'] == 75

    def test_x_rhacs_container_json_to_stix(self):
        """to test x-rhacs-container stix object properties"""

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        container_obj = TestRhacsResultsToStix.get_first_of_type(objects.values(),
                                                                 'x-rhacs-container')
        assert container_obj is not None
        assert container_obj["type"] == 'x-rhacs-container'
        assert container_obj["container_name"] == 'postgresql'
        assert container_obj["image"]['id'] == 'sha256:1896ab7cbfc4ade742b23ca45f' \
                                               '410a1c58a520095c2507619c3346afec125ecc'
        assert container_obj["image"]['name']['remote'] == 'openshift/postgresql'
        assert container_obj["image"]['name']['registry'] == 'image-registry.openshift-' \
                                                             'image-registry.svc:5000'

    def test_x_rhacs_policy_json_to_stix(self):
        """to test x-rhacs-policy stix object properties"""

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        policy_obj = TestRhacsResultsToStix.get_first_of_type(objects.values(),
                                                              'x-rhacs-policy')
        assert policy_obj is not None
        assert policy_obj["type"] == 'x-rhacs-policy'
        assert policy_obj["description"] == 'Unauthorized Network Flow'
        assert policy_obj["policy_id"] == '1b74ffdd-8e67-444c-9814-1c23863c8ccb'
        assert policy_obj["event_source"] == 'DEPLOYMENT_EVENT'
        assert policy_obj["sort_name"] == 'Unauthorized Network Flow'
        assert policy_obj["sort_lifecycle_stage"] == 'RUNTIME'

    def test_x_rhacs_network_flow_json_to_stix(self):
        """to test x-rhacs-networkflow stix object properties"""

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestRhacsResultsToStix.get_first_of_type(objects.values(),
                                                               'x-rhacs-networkflow')
        assert network_obj is not None
        assert network_obj["type"] == 'x-rhacs-networkflow'
        assert network_obj["protocol"] == 'L4_PROTOCOL_TCP'
        assert network_obj["source"]['name'] == 'django-psql-persistent'
        assert network_obj["source"]['entity_type'] == 'DEPLOYMENT'
        assert network_obj["source"]['deployment_namespace'] == 'sample-app1'
        assert network_obj["source"]['deployment_type'] == 'DeploymentConfig'
        assert network_obj["destination"]['name'] == 'postgresql'
        assert network_obj["destination"]['deployment_type'] == 'DeploymentConfig'
        assert network_obj["destination"]['port'] == 5432
