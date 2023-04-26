""" test script to perform unit test case for rhacs transmit module """
import json
import unittest
from unittest.mock import patch

from stix_shifter_modules.rhacs.entry_point import EntryPoint
from stix_shifter.stix_transmission import stix_transmission
from tests.utils.async_utils import get_mock_response


class TestRhacsConnection(unittest.TestCase):
    """ class for test rhacs connection"""

    @staticmethod
    def config():
        """format for configuration"""
        return {
            "auth": {
                "token": "test"
            }
        }

    @staticmethod
    def connection():
        """format for connection"""
        return {
            "host": "testhost",
            "sni":"testsni",
            "selfSignedCert":"-----BEGIN CERTIFICATE-----XXXX123-----END CERTIFICATE-----",
            "port": 443,
            "options": {"result_limit": 10}
        }

    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.__init__')
    def test_is_async(self, mock_api_client):
        """check for synchronous or asynchronous"""
        mock_api_client.return_value = None
        entry_point = EntryPoint(self.connection(), self.config())
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.__init__')
    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.ping_data_source')
    def test_ping_endpoint(self, mock_ping_source, mock_api_client):
        """ test to check ping_data_source function"""

        obj_alert_list = """{"status":"ok"}"""
        resp = get_mock_response(200, obj_alert_list)
        mock_ping_source.return_value = resp

        mock_api_client.return_value = None

        transmission = stix_transmission.StixTransmission('rhacs',
                                                          self.connection(),
                                                          self.config())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.__init__')
    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.get_limit')
    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.get_inner_results')
    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_process_violation_result(self, mock_results_response, mock_final_response,
                                      mock_result_limit, mock_api_client):
        """ test to check result of process violation object"""

        obj_alert_list = """{
        "alerts": [{
            "id": "9b46b268-a10b-4595-8b14-2039e88f4f90",
            "lifecycleStage": "RUNTIME",
            "time": "2022-06-28T07:32:19.511349708Z",
            "policy": {
            "id": "a919ccaf-6b43-4160-ac5d-a405e1440a41",
            "name": "Fixable Severity at least Important",
            "severity": "HIGH_SEVERITY",
            "description": "Alert on deployments with fixable vulnerabilities with a Severity Rating at least Important",
            "categories": [
            "Vulnerability Management"
            ],
            "developerInternalFields": null
            },
            "state": "RESOLVED",
            "enforcementCount": 0,
            "tags": [],
            "enforcementAction": "UNSET_ENFORCEMENT",
            "commonEntityInfo": {
            "clusterName": "cp4s-cluster",
            "namespace": "openshift-marketplace",
            "clusterId": "9346e392-6ac5-4247-be91-9b292b9a1eb7",
            "namespaceId": "bb6ab565-f588-4621-91c8-b9842feec56f",
            "resourceType": "DEPLOYMENT"
            },
            "deployment": {
            "id": "56d033fc-e0ec-4b61-9f7b-b3867dc8e38e",
            "name": "certified-operators-wkdv7",
            "clusterName": "cp4s-cluster",
            "namespace": "openshift-marketplace",
            "clusterId": "9346e392-6ac5-4247-be91-9b292b9a1eb7",
            "inactive": false,
            "namespaceId": "bb6ab565-f588-4621-91c8-b9842feec56f"
            }
            }]
            }"""
        obj_alert_details = """{
        "id": "9b46b268-a10b-4595-8b14-2039e88f4f90",
        "policy": {
        "id": "ed8c7957-14de-40bc-aeab-d27ceeecfa7b",
        "name": "Iptables Executed in Privileged Container",
        "description": "Alert on privileged pods that execute iptables",
        "rationale": "Processes that are running with UID 0 run as the root user. iptables can be used in privileged containers to modify the node's network routing.",
        "remediation": "Specify the USER instruction in the Docker image or the runAsUser field within the Pod Security Context",
        "disabled": false,
        "categories": ["Network Tools", "Security Best Practices"],
        "lifecycleStages": ["RUNTIME"],
        "eventSource": "DEPLOYMENT_EVENT",
        "exclusions": [{
        "name": "Don't alert on Kube System Namespace",
        "deployment": {
        "name": "",
        "scope": {
        "cluster": "",
        "namespace": "kube-system",
        "label": null
        }
        },
        "image": null,
        "expiration": null
        }, {
        "name": "Don't alert on istio-system namespace",
        "deployment": {
        "name": "",
        "scope": {
        "cluster": "",
        "namespace": "istio-system",
        "label": null
        }
        },
        "image": null,
        "expiration": null
        }, {
        "name": "Don't alert on openshift-sdn namespace",
        "deployment": {
        "name": "",
        "scope": {
        "cluster": "",
        "namespace": "openshift-sdn",
        "label": null
        }
        },
        "image": null,
        "expiration": null
        }],
        "scope": [],
        "severity": "CRITICAL_SEVERITY",
        "enforcementActions": [],
        "notifiers": [],
        "lastUpdated": null,
        "SORTName": "Iptables Executed in Privileged Container",
        "SORTLifecycleStage": "RUNTIME",
        "SORTEnforcement": false,
        "policyVersion": "1.1",
        "policySections": [{
        "sectionName": "",
        "policyGroups": [{
        "fieldName": "Privileged Container",
        "booleanOperator": "OR",
        "negate": false,
        "values": [{
        "value": "true"
        }]
        }, {
        "fieldName": "Process Name",
        "booleanOperator": "OR",
        "negate": false,
        "values": [{
        "value": "iptables"
        }]
        }, {
        "fieldName": "Process UID",
        "booleanOperator": "OR",
        "negate": false,
        "values": [{
        "value": "0"
        }]
        }]
        }],
        "mitreAttackVectors": [{
        "tactic": "TA0004",
        "techniques": ["T1611"]
        }, {
        "tactic": "TA0005",
        "techniques": ["T1562.004"]
        }],
        "criteriaLocked": true,
        "mitreVectorsLocked": true,
        "isDefault": true
        },
        "lifecycleStage": "RUNTIME",
        "clusterId": "9346e392-6ac5-4247-be91-9b292b9a1eb7",
        "clusterName": "cp4s-cluster",
        "namespace": "calico-system",
        "namespaceId": "e40fd566-7cfe-4b54-864f-2adfc081d303",
        "deployment": {
        "id": "51be7837-838f-479a-8292-7f54c08635da",
        "name": "calico-node",
        "type": "DaemonSet",
        "namespace": "calico-system",
        "namespaceId": "e40fd566-7cfe-4b54-864f-2adfc081d303",
        "labels": {},
        "clusterId": "9346e392-6ac5-4247-be91-9b292b9a1eb7",
        "clusterName": "cp4s-cluster",
        "containers": [{
        "image": {
        "id": "sha256:4a3526e606f7f3f8483e1ba432f06e80eab4fdacdbf64f624c625204b0efb2e9",
        "name": {
        "registry": "registry.au-syd.bluemix.net",
        "remote": "armada-master/calico/node",
        "tag": "v3.21.5",
        "fullName": "registry.au-syd.bluemix.net/armada-master/calico/node:v3.21.5"
        },
        "notPullable": false,
        "isClusterLocal": false
        },
        "name": "calico-node"
        }],
        "annotations": {
        "deprecated.daemonset.template.generation": "1"
        },
        "inactive": false
        },
        "violations": [{
        "message": "Container 'calico-node' is privileged",
        "type": "GENERIC",
        "time": null
        }],
        "processViolation": {
        "message": "Binary '/usr/sbin/iptables' executed with arguments '--version' under user ID 0",
        "processes": [{
        "id": "8e50956f-a14d-4d7a-bb65-85db3fded423",
        "deploymentId": "51be7837-838f-479a-8292-7f54c08635da",
        "containerName": "calico-node",
        "podId": "calico-node-lsx2d",
        "podUid": "0cbe71e5-5e8a-5f3a-be3c-0a2aab6e4103",
        "signal": {
        "id": "e3099528-f2ce-11ec-9ef7-267244758a55",
        "containerId": "d4bb98407b36",
        "time": "2022-06-23T08:31:32.757890057Z",
        "name": "iptables",
        "args": "--version",
        "execFilePath": "/usr/sbin/iptables",
        "pid": 4382,
        "uid": 0,
        "gid": 0,
        "lineage": [],
        "scraped": false,
        "lineageInfo": [{
        "parentUid": 0,
        "parentExecFilePath": "/usr/bin/calico-node"
        }, {
        "parentUid": 0,
        "parentExecFilePath": "/usr/local/bin/runsv"
        }, {
        "parentUid": 0,
        "parentExecFilePath": "/usr/local/bin/runsvdir"
        }]
        },
        "clusterId": "NULL",
        "namespace": "calico-system",
        "containerStartTime": "2022-05-02T14:50:52Z",
        "imageId": "sha256:4a3526e606f7f3f8483e1ba432f06e80eab4fdacdbf64f624c625204b0efb2e9"
        }]
        }
        }"""
        resp = get_mock_response(200, obj_alert_list)
        mock_results_response.return_value = resp
        resp_detail = get_mock_response(200, obj_alert_details)
        mock_final_response.return_value = resp_detail

        mock_api_client.return_value = None
        mock_result_limit.return_value = 10

        query = json.dumps('Lifecycle Stage:"RUNTIME"+Violation Time:>=06/28/2022')

        transmission = stix_transmission.StixTransmission('rhacs',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.__init__')
    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.get_limit')
    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.get_inner_results')
    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_network_flow_result(self, mock_results_response, mock_final_response,
                                 mock_result_limit, mock_api_client):
        """ test to check result network flow object"""

        obj_alert_list = """{
        "alerts": [{
        "id": "009fcc81-1f77-4803-be0f-a1d00c1ab1f3",
        "lifecycleStage": "RUNTIME",
        "time": "2022-06-28T07:32:19.511349708Z",
        "policy": {
        "id": "a919ccaf-6b43-4160-ac5d-a405e1440a41",
        "name": "Fixable Severity at least Important",
        "severity": "HIGH_SEVERITY",
        "description": "Alert on deployments with fixable vulnerabilities with a Severity Rating at least Important",
        "categories": [
        "Vulnerability Management"
        ],
        "developerInternalFields": null
        },
        "state": "RESOLVED",
        "enforcementCount": 0,
        "tags": [],
        "enforcementAction": "UNSET_ENFORCEMENT",
        "commonEntityInfo": {
        "clusterName": "cp4s-cluster",
        "namespace": "openshift-marketplace",
        "clusterId": "9346e392-6ac5-4247-be91-9b292b9a1eb7",
        "namespaceId": "bb6ab565-f588-4621-91c8-b9842feec56f",
        "resourceType": "DEPLOYMENT"
        },
        "deployment": {
        "id": "56d033fc-e0ec-4b61-9f7b-b3867dc8e38e",
        "name": "certified-operators-wkdv7",
        "clusterName": "cp4s-cluster",
        "namespace": "openshift-marketplace",
        "clusterId": "9346e392-6ac5-4247-be91-9b292b9a1eb7",
        "inactive": false,
        "namespaceId": "bb6ab565-f588-4621-91c8-b9842feec56f"
        }
        }]
        }"""
        obj_alert_details = """{
        "id": "009fcc81-1f77-4803-be0f-a1d00c1ab1f3",
        "policy": {
        "id": "1b74ffdd-8e67-444c-9814-1c23863c8ccb",
        "name": "Unauthorized Network Flow",
        "description": "This policy generates a violation for the network flows that fall outside baselines for which 'alert on anomalous violations' is set.",
        "rationale": "The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.",
        "remediation": "Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.",
        "disabled": false,
        "categories": [
        "Anomalous Activity"
        ],
        "lifecycleStages": [
        "RUNTIME"
        ],
        "eventSource": "DEPLOYMENT_EVENT",
        "exclusions": [],
        "scope": [],
        "severity": "HIGH_SEVERITY",
        "enforcementActions": [],
        "notifiers": [],
        "lastUpdated": null,
        "SORTName": "Unauthorized Network Flow",
        "SORTLifecycleStage": "RUNTIME",
        "SORTEnforcement": false,
        "policyVersion": "1.1",
        "policySections": [{
        "sectionName": "Unauthorized Network Flow",
        "policyGroups": [{
        "fieldName": "Unexpected Network Flow Detected",
        "booleanOperator": "OR",
        "negate": false,
        "values": [{
        "value": "true"
        }]
        }]
        }],
        "mitreAttackVectors": [],
        "criteriaLocked": true,
        "mitreVectorsLocked": true,
        "isDefault": true
        },
        "lifecycleStage": "RUNTIME",
        "clusterId": "a9bb4695-8335-473b-beea-8dc4fd44c6ba",
        "clusterName": "cp4s-cluster",
        "namespace": "test-app1",
        "namespaceId": "88af0905-0323-4080-8693-57f1ff0bcc94",
        "deployment": {
        "id": "177ec02b-1cf9-4852-9a73-9aa4c7d056e6",
        "name": "postgresql",
        "type": "DeploymentConfig",
        "namespace": "test-app1",
        "namespaceId": "88af0905-0323-4080-8693-57f1ff0bcc94",
        "labels": {
        "app": "django-psql-example",
        "template": "django-psql-example",
        "template.openshift.io/template-instance-owner": "fd5af023-7f55-4e1d-94f3-6322d7d76caf"
        },
        "clusterId": "a9bb4695-8335-473b-beea-8dc4fd44c6ba",
        "clusterName": "cp4s-cluster",
        "containers": [{
        "image": {
        "id": "sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985",
        "name": {
        "registry": "image-registry.openshift-image-registry.svc:5000",
        "remote": "openshift/postgresql",
        "tag": "",
        "fullName": "image-registry.openshift-image-registry.svc:5000/openshift/postgresql@sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985"
        },
        "notPullable": false,
        "isClusterLocal": false
        },
        "name": "postgresql"
        }],
        "annotations": {
        "description": "Defines how to deploy the database",
        "template.alpha.openshift.io/wait-for-ready": "true"
        },
        "inactive": false
        },
        "violations": [{
        "message": "Unexpected network flow found in deployment. Source name: 'django-psql-example'. Destination name: 'postgresql'. Destination port: '5432'. Protocol: 'L4_PROTOCOL_TCP'.",
        "networkFlowInfo": {
        "protocol": "L4_PROTOCOL_TCP",
        "source": {
        "name": "django-psql-example",
        "entityType": "DEPLOYMENT",
        "deploymentNamespace": "test-app1",
        "deploymentType": "DeploymentConfig",
        "port": 0
        },
        "destination": {
        "name": "postgresql",
        "entityType": "DEPLOYMENT",
        "deploymentNamespace": "test-app1",
        "deploymentType": "DeploymentConfig",
        "port": 5432
        }
        },
        "type": "NETWORK_FLOW",
        "time": "2022-06-22T06:43:37.561176101Z"
        }

        ],
        "processViolation": null,
        "enforcement": null,
        "time": "2022-06-22T06:43:37.561455470Z",
        "firstOccurred": "2022-06-08T05:41:42.164657588Z",
        "resolvedAt": "2022-06-22T06:48:12.765180563Z",
        "state": "RESOLVED",
        "snoozeTill": null,
        "tags": []
        }"""
        resp = get_mock_response(200, obj_alert_list)
        mock_results_response.return_value = resp
        resp_detail = get_mock_response(200, obj_alert_details)
        mock_final_response.return_value = resp_detail

        mock_api_client.return_value = None
        mock_result_limit.return_value = 10

        query = json.dumps('Lifecycle Stage:"RUNTIME"+Violation Time:>=06/28/2022')

        transmission = stix_transmission.StixTransmission('rhacs',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.__init__')
    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.get_limit')
    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.get_inner_results')
    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_violation_without_network_process(self, mock_results_response,
                                    mock_final_response, mock_result_limit, mock_api_client):
        """ test to check result without process and network violation object"""

        obj_alert_list = """{
            "alerts": [{
            "id": "f5457fd2-71da-476f-8c4c-6c1b13d91aee",
            "lifecycleStage": "DEPLOY",
            "time": "2022-06-28T07:32:19.511349708Z",
            "policy": {
            "id": "a919ccaf-6b43-4160-ac5d-a405e1440a41",
            "name": "Fixable Severity at least Important",
            "severity": "HIGH_SEVERITY",
            "description": "Alert on deployments with fixable vulnerabilities with a Severity Rating at least Important",
            "categories": [
            "Vulnerability Management"
            ],
            "developerInternalFields": null
            },
            "state": "RESOLVED",
            "enforcementCount": 0,
            "tags": [],
            "enforcementAction": "UNSET_ENFORCEMENT",
            "commonEntityInfo": {
            "clusterName": "cp4s-cluster",
            "namespace": "openshift-marketplace",
            "clusterId": "9346e392-6ac5-4247-be91-9b292b9a1eb7",
            "namespaceId": "bb6ab565-f588-4621-91c8-b9842feec56f",
            "resourceType": "DEPLOYMENT"
            },
            "deployment": {
            "id": "56d033fc-e0ec-4b61-9f7b-b3867dc8e38e",
            "name": "certified-operators-wkdv7",
            "clusterName": "cp4s-cluster",
            "namespace": "openshift-marketplace",
            "clusterId": "9346e392-6ac5-4247-be91-9b292b9a1eb7",
            "inactive": false,
            "namespaceId": "bb6ab565-f588-4621-91c8-b9842feec56f"
            }
            }]
            }"""
        obj_alert_details = """{
        "id": "f5457fd2-71da-476f-8c4c-6c1b13d91aee",
        "policy": {
        "id": "a919ccaf-6b43-4160-ac5d-a405e1440a41",
        "name": "Fixable Severity at least Important",
        "description": "Alert on deployments with fixable vulnerabilities with a Severity Rating at least Important",
        "rationale": "Known vulnerabilities make it easier for adversaries to exploit your application. You can fix these high-severity vulnerabilities by updating to a newer version of the affected component(s).",
        "remediation": "Use your package manager to update to a fixed version in future builds or speak with your security team to mitigate the vulnerabilities.",
        "disabled": false,
        "categories": [
        "Vulnerability Management"
        ],
        "lifecycleStages": [
        "BUILD",
        "DEPLOY"
        ],
        "eventSource": "NOT_APPLICABLE",
        "exclusions": [],
        "scope": [],
        "severity": "HIGH_SEVERITY",
        "enforcementActions": [
        "FAIL_BUILD_ENFORCEMENT"
        ],
        "notifiers": [],
        "lastUpdated": null,
        "SORTName": "Fixable Severity at least Important",
        "SORTLifecycleStage": "BUILD,DEPLOY",
        "SORTEnforcement": true,
        "policyVersion": "1.1",
        "policySections": [{
        "sectionName": "",
        "policyGroups": [{
        "fieldName": "Fixed By",
        "booleanOperator": "OR",
        "negate": false,
        "values": [{
        "value": ".*"
        }]
        },
        {
        "fieldName": "Severity",
        "booleanOperator": "OR",
        "negate": false,
        "values": [{
        "value": ">= IMPORTANT"
        }]
        }
        ]
        }],
        "mitreAttackVectors": [],
        "criteriaLocked": true,
        "mitreVectorsLocked": true,
        "isDefault": true
        },
        "lifecycleStage": "DEPLOY",
        "clusterId": "9346e392-6ac5-4247-be91-9b292b9a1eb7",
        "clusterName": "cp4s-cluster",
        "namespace": "openshift-marketplace",
        "namespaceId": "bb6ab565-f588-4621-91c8-b9842feec56f",
        "deployment": {
        "id": "bed94225-2e1a-4967-abec-c5b425681476",
        "name": "redhat-operators-jr9fc",
        "type": "Pod",
        "namespace": "openshift-marketplace",
        "namespaceId": "bb6ab565-f588-4621-91c8-b9842feec56f",
        "labels": {
        "catalogsource.operators.coreos.com/update": "redhat-operators",
        "olm.catalogSource": "",
        "olm.pod-spec-hash": "695c74c777"
        },
        "clusterId": "9346e392-6ac5-4247-be91-9b292b9a1eb7",
        "clusterName": "cp4s-cluster",
        "containers": [{
        "image": {
        "id": "sha256:13040c6aa1d39fb44a7c8f6578e6834679c29b20d0ad51070c597056786e9558",
        "name": {
        "registry": "registry.redhat.io",
        "remote": "redhat/redhat-operator-index",
        "tag": "v4.8",
        "fullName": "registry.redhat.io/redhat/redhat-operator-index:v4.8"
        },
        "notPullable": false,
        "isClusterLocal": false
        },
        "name": "registry-server"
        }],
        "annotations": {
        "cni.projectcalico.org/containerID": 
        "db82cbecc0068a0ed769d219857de1df18561641300a41214efc1235d7efdb63",
        "cni.projectcalico.org/podIP": "172.30.108.234/32",
        "cni.projectcalico.org/podIPs": "172.30.108.234/32",
        "openshift.io/scc": "anyuid",
        "operatorframework.io/managed-by": "marketplace-operator",
        "operatorframework.io/priorityclass": "system-cluster-critical"
        },
        "inactive": false
        },
        "violations": [{
        "message": "Fixable RHSA-2022:4993 (CVSS 7.1) (severity Important) found in component 'xz-libs' (version 5.2.4-3.el8.x86_64) in container 'registry-server', resolved by version 0:5.2.4-4.el8_4",
        "type": "GENERIC",
        "time": null
        }],
        "processViolation": null,
        "enforcement": null,
        "time": "2022-06-23T14:56:23.840797596Z",
        "firstOccurred": "2022-06-23T14:56:23.848388776Z",
        "resolvedAt": "2022-06-23T14:56:42.289570662Z",
        "state": "RESOLVED",
        "snoozeTill": null,
        "tags": []
        }"""

        resp = get_mock_response(200, obj_alert_list)
        mock_results_response.return_value = resp
        resp_detail = get_mock_response(200, obj_alert_details)
        mock_final_response.return_value = resp_detail

        mock_api_client.return_value = None
        mock_result_limit.return_value = 10

        query = json.dumps('Lifecycle Stage:"DEPLOY"+Violation Time:>=06/28/2022')

        transmission = stix_transmission.StixTransmission('rhacs',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is True
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host_ping(self, mock_ping):
        """Test Invalid host"""
        mock_ping.side_effect = Exception("Invalid Host")
        transmission = stix_transmission.StixTransmission('rhacs', self.connection(), self.config())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert 'rhacs connector error => Invalid Host' in ping_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_url_parameter_ping(self, mock_ping):
        """Test Invalid host"""
        mock_ping.side_effect = Exception("Invalid parameter or Url")
        transmission = stix_transmission.StixTransmission('rhacs', self.connection(), self.config())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert 'rhacs connector error => Invalid parameter or Url' in ping_response['error']

    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.__init__')
    def test_x_ibm_finding_query(self, mock_api_client):
        """ test to check query of x-ibm-finding element """
        mock_api_client.return_value = None
        query = json.dumps('Lifecycle Stage:"RUNTIME"+Violation Time:>=06/28/2022')

        transmission = stix_transmission.StixTransmission('rhacs',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.__init__')
    def test_x_rhacs_deployment_query(self, mock_api_client):
        """ test to check query of x-rhacs-deployment element """
        mock_api_client.return_value = None
        query = json.dumps('Deployment:"app-manager"+Violation Time:>=06/01/2022')

        transmission = stix_transmission.StixTransmission('rhacs',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.__init__')
    def test_x_rhacs_cluster_query(self, mock_api_client):
        """ test to check query of x-rhacs-deployment element """
        mock_api_client.return_value = None
        query = json.dumps('Cluster:"cp4s-cluster"+Violation Time:>=06/01/2022')

        transmission = stix_transmission.StixTransmission('rhacs',
                                                          self.connection(),
                                                          self.config())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] is not None
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.__init__')
    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.get_limit')
    @patch('stix_shifter_modules.rhacs.stix_transmission.api_client'
           '.APIClient.get_search_results')
    def test_search_result_authentication_error(self, mock_results_response,
                                                mock_result_limit, mock_api_client):
        """ test to check translate result authentication error """
        obj = '{"error":"credentials not found:token validation failed","code":16,"message":' \
              '"credentials not found:token validation failed","details": []}'
        mock_resp = get_mock_response(401, obj)
        mock_results_response.return_value = mock_resp
        mock_api_client.return_value = None
        mock_result_limit.return_value = 10

        query = json.dumps('Lifecycle Stage:"RUNTIME"+Violation Time:>=06/28/2022')

        transmission = stix_transmission.StixTransmission('rhacs',
                                                          self.connection(),
                                                          self.config())
        offset = 0
        length = 1
        results_response = transmission.results(query, offset, length)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['error'] is not None
