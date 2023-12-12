""" test script to perform unit test case for sysdig translate results """
import unittest
from stix_shifter_modules.sysdig.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "sysdig"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "sysdig",
    "identity_class": "events"
}
options = {}

data = {
    "id": "111aaa1111112222eeee333fff999fff666e00eee",
    "cursor": "ababababababababababababababab",
    "timestamp": "2023-08-12T16:18:13.823377041Z",
    "customerId": 11111111,
    "originator": "policy",
    "category": "runtime",
    "source": "syscall",
    "name": "Sysdig Runtime Threat Detection",
    "description": "This policy contains rules which Sysdig considers High Confidence of a security incident. "
                   "They are tightly coupled to common attacker TTP's. They have been designed to minimize "
                   "false positives but may still result in some depending on your environment.",
    "severity": 3,
    "agentId": 0000000,
    "containerId": "12345678910",
    "machineId": "00:00:00:00:00:11",
    "content": {
        "falsePositive": 'false',
        "fields": {
            "container.id": "1111b1b11b11",
            "container.image.repository": "quay.io/openshift-release-dev/ocp-v4.0-art-dev",
            "container.name": "tuned",
            "evt.arg.level": "SOL_SOCKET",
            "evt.res": "SUCCESS",
            "evt.type": "setsockopt",
            "falco.rule": "Possible Backdoor using BPF",
            "fd.sip.name": "",
            "fd.sport": "",
            "group.gid": "0",
            "group.name": "root",
            "proc.aname[2]": "run",
            "proc.aname[3]": "conmon",
            "proc.aname[4]": "systemd",
            "proc.cmdline": "tuned -Es /usr/sbin/tuned --no-dbus",
            "proc.cwd": "/var/lib/tuned/",
            "proc.exepath": "/usr/sbin/tuned",
            "proc.name": "tuned",
            "proc.pcmdline": "openshift-tuned -v=0",
            "proc.pid": "123456",
            "proc.pname": "openshift-tuned",
            "proc.ppid": "77777",
            "proc.sid": "33333",
            "user.loginname": "",
            "user.loginuid": "-1",
            "user.name": "root",
            "user.uid": "0"
        },
        "internalRuleName": "Possible Backdoor using BPF",
        "matchedOnDefault": 'false',
        "origin": "Sysdig",
        "output": "Possible BPFDoor Attempt Detected (proc.cmdline=tuned -Es /usr/sbin/tuned --no-dbus "
                  "port=<NA> domain=<NA> proc.pcmdline=openshift-tuned -v=0 level=SOL_SOCKET proc."
                  "pname=openshift-tuned gparent=run ggparent=conmon ggparent=systemd container=tuned "
                  "(id=5801c9b81b33) evt.type=setsockopt evt.res=SUCCESS proc.pid=123241552 proc.cwd=/var/lib/"
                  "tuned/ proc.ppid=77777 proc.pcmdline=openshift-tuned -v=0 proc.sid=33333 proc.exepath=/usr"
                  "/sbin/tuned user.uid=0 user.loginuid=-1 user.loginname=<NA> user.name=root group.gid=0 group."
                  "name=root container.id=333b3b33333 container.name=tuned image=quay.io/openshift-release-"
                  "dev/ocp-v4.0-art-dev)",
        "policyId": 1000000,
        "ruleName": "Possible Backdoor using BPF",
        "ruleSubType": 0,
        "ruleTags": [
            "network",
            "MITRE",
            "MITRE_TA0007_discovery",
            "MITRE_TA0006_credential_access",
            "MITRE_T1040_network_sniffing",
            "MITRE_TA0005_defense_evasion"
        ],
        "ruleType": 6
    },
    "labels": {
        "container.image.digest": "sha256:aaaaa12345678910",
        "container.image.id": "12345aaaa6a789a",
        "container.image.repo": "quay.io/openshift-release-dev/ocp-v4.0-art-dev",
        "container.label.io.kubernetes.container.name": "tuned",
        "container.label.io.kubernetes.pod.name": "tuned-4nf6b",
        "container.label.io.kubernetes.pod.namespace": "openshift-cluster-node-tuning-operator",
        "container.name": "tuned",
        "host.hostName": "kube-ch548qct0c9fugqhf7bg-cp4scluster-default-00000183.iks.ibm",
        "host.mac": "00:00:00:00:00:00",
        "kubernetes.cluster.name": "ap5s-cluster",
        "kubernetes.daemonSet.name": "tuned",
        "kubernetes.namespace.name": "openshift-cluster-node-tuning-operator",
        "kubernetes.node.name": "00.000.00.000",
        "kubernetes.pod.name": "tuned-12345",
        "kubernetes.workload.name": "tuned",
        "kubernetes.workload.type": "daemonset",
        "process.name": "tuned -Es /usr/sbin/tuned --no-dbus"
    }
}

data_1 = {
    "id": "123445678910abcdefghijklmn",
    "cursor": "ABCDEFGHIJ12345678910",
    "timestamp": "2023-08-01T19:02:06.198576572Z",
    "customerId": 1111111,
    "originator": "policy",
    "category": "runtime",
    "source": "syscall",
    "name": "Sysdig Runtime Threat Detection",
    "description": "This policy contains rules which Sysdig considers High Confidence of a security incident."
                   " They are tightly coupled to common attacker TTP's. They have been designed to minimize false "
                   "positives but may still result in some depending on your environment.",
    "severity": 3,
    "agentId": 12345678,
    "containerId": "123abc456",
    "machineId": "00:00:00:00:11:1a",
    "content": {
        "falsePositive": 'false',
        "fields": {
            "container.image.repository": "au.icr.io/armada-master/keepalived",
            "container.name": "ibm-cloud-provider-ip-111-11-11-111",
            "evt.args": "domain=17(AF_PACKET) type=3 proto=0 ",
            "evt.type": "socket",
            "falco.rule": "Packet socket created in container",
            "fd.cport": "",
            "fd.name": "",
            "fd.sport": "",
            "proc.aname[2]": "conmon",
            "proc.aname[3]": "systemd",
            "proc.aname[4]": "",
            "proc.cmdline": "tcpdump -v -l -n -i eth1 ip proto 112 or host 222.0.0.00",
            "proc.cwd": "/",
            "proc.exepath": "/usr/bin/tcpdump",
            "proc.name": "tcpdump",
            "proc.pcmdline": "keepalived",
            "proc.pname": "keepalived",
            "user.loginname": "",
            "user.loginuid": "-1",
            "user.name": "root",
            "user.uid": "0"
        },
        "internalRuleName": "Packet socket created in container",
        "matchedOnDefault": 'false',
        "origin": "Sysdig",
        "output": "Packet socket was created in a container (evt.type=socket evt.args=domain=17(AF_PACKET) type=3"
                  " proto=0  proc.name=tcpdump proc.pname=keepalived gparent=conmon ggparent=systemd gggparent=<NA>"
                  " container.name=ibm-cloud-provider-ip-111-11-11-111 image=au.icr.io/armada-master/keepalived proc."
                  "cmdline=tcpdump -v -l -n -i eth1 ip proto 112 or host 222.0.0.22 proc.cwd=/ proc.pcmdline=keepalived"
                  " user.name=root user.loginuid=-1 user.uid=0 user.loginname=<NA> fd.cport=<NA> "
                  "fd.sport=<NA> fd.name=<NA>)",
        "policyId": 12345678,
        "ruleName": "Packet socket created in container",
        "ruleSubType": 0,
        "ruleTags": [
            "network",
            "SOC2",
            "SOC2_CC6.8",
            "NIST",
            "NIST_800-53",
            "NIST_800-53_AC-6(9)",
            "NIST_800-53_AC-6(10)",
            "ISO",
            "ISO_27001",
            "ISO_27001_A.9.1.2",
            "HIPAA",
            "HIPAA_164.308(a)",
            "HIPAA_164.312(a)",
            "HITRUST",
            "HITRUST_CSF",
            "HITRUST_CSF_01.c",
            "HITRUST_CSF_09.aa",
            "MITRE",
            "MITRE_T1133_external_remote_services",
            "MITRE_TA0003_persistence",
            "MITRE_TA0006_credential_access",
            "MITRE_TA0009_collection",
            "MITRE_TA0004_privilege_escaltion",
            "MITRE_T1557_adversary_in_the_middle"
        ],
        "ruleType": 6
    },
    "labels": {
        "container.image.digest": "sha256:abcedfghijklmnoped674c589316d7a9e0d3862f9387a9197d8c5ee8b83fcb085eb661478a5",
        "container.image.id": "12345abcdefgh",
        "container.image.repo": "au.icr.io/armada-master/keepalived",
        "container.image.tag": "1111",
        "container.label.io.kubernetes.container.name": "ibm-cloud-provider-ip-123-45-67-8910",
        "container.label.io.kubernetes.pod.name": "ibm-cloud-provider-ip-123-45-67-8910-1234567-jp98p",
        "container.label.io.kubernetes.pod.namespace": "ibm-system",
        "container.name": "ibm-cloud-provider-ip-123-12-12-123",
        "host.hostName": "kube-ch548qct0cabcdefghijkl-cp4scluster-default-0000028c.iks.ibm",
        "host.mac": "00:00:00:11:11:1a",
        "kubernetes.cluster.name": "ap5s-cluster",
        "kubernetes.deployment.name": "ibm-cloud-provider-ip-111-11-11-111",
        "kubernetes.namespace.name": "ibm-system",
        "kubernetes.node.name": "10.000.00.000",
        "kubernetes.pod.name": "ibm-cloud-provider-ip-123-45-67-8910-12345d8f4777-jp98p",
        "kubernetes.replicaSet.name": "ibm-cloud-provider-ip-123-45-67-8910-847d8f47b7",
        "kubernetes.workload.name": "ibm-cloud-provider-ip-123-45-67-8910",
        "kubernetes.workload.type": "deployment",
        "process.name": "tcpdump -v -l -n -i eth1 ip proto 112 or host 222.0.0.11"
    }
}
data_2 = {
    "id": "123456789100000",
    "cursor": "ABCDEFGHIJKLMN",
    "timestamp": "2023-11-22T11:16:28.101680299Z",
    "customerId": 100,
    "originator": "policy",
    "category": "runtime",
    "source": "syscall",
    "name": "sysdig custom network rules-2",
    "description": "updated network rules with network tag",
    "severity": 0,
    "agentId": 12345,
    "containerId": "12345678910",
    "machineId": "10:00:00:00:00:00",
    "content": {
        "falsePositive": 'false',
        "fields": {
            "container.id": "12345678910",
            "container.image.repository": "docker.io/radial",
            "container.image.tag": "curl",
            "container.name": "curl-sample-app1",
            "evt.res": "EINPROGRESS",
            "evt.type": "connect",
            "falco.rule": "Contact EC2 Instance Metadata Service From Container",
            "fd.name": "111.111.11.111:1000->111.11.111.111:00",
            "group.gid": "0",
            "group.name": "root",
            "proc.aname[2]": "containerd-shim",
            "proc.aname[3]": "systemd",
            "proc.aname[4]": "",
            "proc.args": "-s http://111.111.111.111:11/iam/security-credentials",
            "proc.cmdline": "curl -s http://111.111.111.111:11/iam/security-credentials",
            "proc.cwd": "/",
            "proc.exepath": "/usr/bin/curl",
            "proc.name": "curl",
            "proc.pcmdline": "sh",
            "proc.pid": "11111",
            "proc.pname": "sh",
            "proc.ppid": "12345",
            "proc.sid": "1",
            "user.loginname": "",
            "user.loginuid": "-1",
            "user.name": "root",
            "user.uid": "0"
        },
        "internalRuleName": "Contact EC2 Instance Metadata Service From Container",
        "matchedOnDefault": 'false',
        "origin": "Secure UI",
        "ruleName": "Contact EC2 Instance Metadata Service From Container",
        "ruleSubType": 0,
        "ruleType": 6
    },
    "labels": {
        "aws.accountId": "1111111111",
        "aws.instanceId": "i-00000000",
        "aws.region": "us-east-1",
        "cloudProvider.account.id": "111111111",
        "cloudProvider.name": "aws",
        "cloudProvider.region": "us-east-1",
        "container.image.digest": "sha256:111111",
        "container.image.id": "4776f1f7d1f6",
        "container.image.repo": "docker.io/radial",
        "container.image.tag": "curl",
        "container.label.io.kubernetes.container.name": "curl-sample-app1",
        "container.label.io.kubernetes.pod.name": "curl-sample-app1",
        "container.label.io.kubernetes.pod.namespace": "default",
        "container.name": "curl-sample-app1",
        "host.hostName": "ip-111-111-11-111.ec2.internal",
        "host.mac": "11:aa:bb:dd:11:00",
        "kubernetes.cluster.name": "sysdig-eks-cluster",
        "kubernetes.namespace.name": "default",
        "kubernetes.node.name": "ip-111-111-11-111.ec2.internal",
        "kubernetes.pod.name": "curl-sample-app1",
        "process.name": "curl -s http://111.111.111.111:11/iam/security-credentials"
    },
    "finding_type": "threat",
    "direction": "out",
    "source_ip": "111.111.11.111",
    "source_port": "10000",
    "destination_ip": "111.11.111.111",
    "destination_port": "00",
    "proto": "tcp"
}


class TestsysdigResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for sysdig translate results
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
        return TestsysdigResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

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

    def test_x_sysdig_cluster_json_to_stix(self):
        """  to test x-sysdig-cluster stix object properties  """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']
        cluster_obj = TestsysdigResultsToStix.get_first_of_type(objects.values(), 'x-sysdig-cluster')
        assert cluster_obj is not None
        assert cluster_obj['type'] == 'x-sysdig-cluster'
        assert cluster_obj['name'] == 'ap5s-cluster'
        assert cluster_obj['daemonset'] == 'tuned'
        assert cluster_obj['namespace'] == 'openshift-cluster-node-tuning-operator'
        node_ref = cluster_obj['x_node_ref']
        assert (node_ref in objects), f"node_ref with key {cluster_obj['x_node_ref']} " \
                                      f"not found"

    def test_x_sysdig_deployment_json_to_stix(self):
        """to test x-sysdig-deployment stix object properties"""

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data_1], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        deployment_obj = TestsysdigResultsToStix.get_first_of_type(objects.values(), 'x-sysdig-deployment')
        assert deployment_obj is not None
        assert deployment_obj['type'] == 'x-sysdig-deployment'
        assert deployment_obj['name'] == 'ibm-cloud-provider-ip-111-11-11-111'

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

        finding_obj = TestsysdigResultsToStix.get_first_of_type(objects.values(),
                                                                'x-ibm-finding')
        assert finding_obj is not None
        assert finding_obj["type"] == 'x-ibm-finding'
        assert finding_obj["x_threat_originator"] == 'policy'
        assert finding_obj["x_category"] == 'runtime'
        assert finding_obj["x_threat_source"] == 'syscall'

        cluster_ref = finding_obj['x_cluster_ref']
        assert (cluster_ref in objects), f"cluster_ref with key {finding_obj['x_cluster_ref']} " \
                                         f"not found"

        policy_ref = finding_obj['x_policy_ref']
        assert (policy_ref in objects), f" policy_ref with key {finding_obj['x_policy_ref']} " \
                                        f"not found"

    def test_x_oca_asset_json_to_stix(self):
        """to test x-oca-asset stix object properties"""

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data_1], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        asset_obj = TestsysdigResultsToStix.get_first_of_type(objects.values(),
                                                              'x-oca-asset')
        assert asset_obj is not None
        assert asset_obj["type"] == 'x-oca-asset'
        assert asset_obj['extensions']['x-oca-container-ext']['container_id'] == '123abc456'
        assert asset_obj['extensions']['x-oca-container-ext']['x_digest'] == \
               'sha256:abcedfghijklmnoped674c589316d7a9e0d3862f9387a9197d8' \
               'c5ee8b83fcb085eb661478a5'
        ip_ref = asset_obj['ip_refs']
        assert (values in objects for values in ip_ref), f"ip_refs with key {asset_obj['ip_refs']} " \
                                                         f"not found"

        mac_ref = asset_obj['mac_refs']
        assert (values in objects for values in mac_ref), f"mac_refs with key {asset_obj['mac_refs']} " \
                                                          f"not found"

    def test_x_sysdig_policy_json_to_stix(self):
        """to test x-sysdig-policy stix object properties"""

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data_1], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        policy_obj = TestsysdigResultsToStix.get_first_of_type(objects.values(),
                                                               'x-sysdig-policy')
        assert policy_obj is not None
        assert policy_obj["type"] == 'x-sysdig-policy'
        assert policy_obj["rule_name"] == 'Packet socket created in container'
        assert policy_obj["rule_type"] == 6

    def test_x_mac_addr_json_to_stix(self):
        """to test mac-addr stix object properties"""

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data_1], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        policy_obj = TestsysdigResultsToStix.get_first_of_type(objects.values(),
                                                               'mac-addr')
        assert policy_obj is not None
        assert policy_obj["type"] == 'mac-addr'
        assert policy_obj["value"] == '00:00:00:11:11:1a'

    def test_cloud_provider_details(self):
        """to test cloud provider stix object properties"""

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data_2], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        cloud_obj = TestsysdigResultsToStix.get_first_of_type(objects.values(),
                                                              'x-cloud-provider')
        assert cloud_obj is not None
        assert cloud_obj["type"] == 'x-cloud-provider'
        assert cloud_obj["account_id"] == '1111111111'
        assert cloud_obj["name"] == 'aws'
        assert cloud_obj["region"] == 'us-east-1'
