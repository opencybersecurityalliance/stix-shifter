import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.darktrace.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "darktrace"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "darktrace",
    "identity_class": "events"
}
options = {}


class TestDarktraceResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for darktrace translate results
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
        return TestDarktraceResultsToStix.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)

    def test_macaddress_json_to_stix(self):
        """
        to test mac-address stix object properties
        """
        data = \
            {
                "dhcp":
                    {
                        "mac": "12:2f:23:46:35:5b",
                        "epochdate": 1647859960.933523,
                        "source_ip": "172.31.81.98",
                        "trans_id": 1512448313,
                        "assigned_ip": "172.31.81.98",
                        "dest_ip": "172.31.80.1",
                        "source_port": 68,
                        "dest_port": 67,
                        "uid": "C5FYmbt4Q19KyCfNg01",
                        "dhcp_type": "DHCP::ack",
                        "domain_name": "ec2.internal",
                        "lease_time": 3600,
                        "subnet_mask": "255.255.240.0"
                    }
            }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        mac_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'mac-addr')

        assert mac_obj is not None
        assert mac_obj['type'] == 'mac-addr'

    def test_domain_name_json_to_stix(self):
        """
        to test domain_name stix object properties
        """
        data = \
            {
                "dhcp":
                    {
                        "mac": "12:2f:23:46:35:5b",
                        "epochdate": 1647859960.933523,
                        "source_ip": "172.31.81.98",
                        "trans_id": 1512448313,
                        "assigned_ip": "172.31.81.98",
                        "dest_ip": "172.31.80.1",
                        "source_port": 68,
                        "dest_port": 67,
                        "uid": "C5FYmbt4Q19KyCfNg01",
                        "dhcp_type": "DHCP::ack",
                        "domain_name": "ec2.internal",
                        "lease_time": 3600,
                        "subnet_mask": "255.255.240.0"
                    }
            }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        domain_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'domain-name')
        assert domain_obj is not None

        assert domain_obj['type'] == 'domain-name'
        assert domain_obj['value'] == 'ec2.internal'

    def test_email_addr_json_to_stix(self):
        """
        to test email-addr stix object properties
        """
        data = \
            {
                "smtp":
                    {
                        "tls": 'false',
                        "epochdate": 1647934092.62255,
                        "source_ip": "172.31.81.98",
                        "source_port": 49642,
                        "dest_ip": "172.253.115.109",
                        "rcptto": "shahtanveer@gmail.com",
                        "uid": "ClEmCm1nIzVuPnsVf01",
                        "dest_port": 587,
                        "trans_depth": 1,
                        "path": [
                            "172.253.115.109",
                            "172.31.81.98"
                        ],
                        "mailfrom": "shahtanve\b\b\b\b\brayyan31@gmail.com",
                        "last_reply": "221 2.0.0 closing connection "
                                      "f34-20020a05622a1a2200b002e1a35ed1desm13627195qtb.94 - gsmtp",
                        "proto": "null"
                    }
            }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        email_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'email-addr')
        assert email_obj is not None

        assert email_obj['type'] == 'email-addr'
        assert email_obj['value'] == 'shahtanveer@gmail.com'

    def test_software_json_to_stix(self):
        """
        to test software stix object properties
        """
        data = \
            {
                "software":
                    {
                        "epochdate": 1647762879.269305,
                        "source_ip": "172.31.81.98",
                        "source_port": 50507,
                        "version_minor": 0,
                        "host": "172.31.81.98",
                        "uid": "COygFk1aHXEfHLN7I301",
                        "name": "Windows",
                        "version_major": 10,
                        "dest_ip": "8.253.131.111",
                        "dest_port": 80,
                        "software_type": "OS::WINDOWS"
                    }
            }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        software_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'software')
        assert software_obj is not None
        assert software_obj['type'] == 'software'
        assert software_obj['name'] == 'Windows'

    def test_file_json_to_stix(self):
        """to test file-identifier stix object properties"""

        data = \
            {
                "files_identified":
                    {
                        "fuid": "Flj8fX36Su0utIp4Pi01",
                        "epochdate": 1647594890.251892,
                        "total_bytes": 7796,
                        "source_port": 50368,
                        "sha1": "a1dc74ef8495c9a1489dd937659b5c2875027e16",
                        "sha256": "ebf3e7290b8fd1e5509caa69335251f22b61baf3f9ff87b4e8544f3c1fea279d",
                        "dest_port": 80,
                        "seen_bytes": 7796,
                        "file_ident_descr": "http://ctldl.windowsupdate.com/msdownload/update/v3/static"
                                            "/trustedr/en/pinrulesstl.cab?cbb06552d1d4d1c9",
                        "source_ip": "172.31.81.98",
                        "dest_ip": "72.21.81.240",
                        "file_ident_ports": 80,
                        "conn_uids": "CuO37a3edvzWRvNbNa01",
                        "uid": "CuO37a3edvzWRvNbNa01",
                        "source": "HTTP",
                        "md5": "fb60e1afe48764e6bf78719c07813d32",
                        "mime_type": "application/vnd.ms-cab-compressed",
                        "tx_hosts": "72.21.81.240",
                        "rx_hosts": "172.31.81.98"
                    }
            }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        file_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'file')
        assert file_obj is not None
        assert file_obj['type'] == 'file'
        assert file_obj['mime_type'] == 'application/vnd.ms-cab-compressed'

    def test_x509_json_to_stix(self):
        """to test x509-certificate stix object properties"""

        data = \
            {
                "x509":
                    {
                        "epochdate": 1647412159.700335,
                        "source_port": 57990,
                        "certificate_not_valid_after": 1660562534,
                        "fid": "FSne9FVehr5qzFONl01",
                        "certificate_key_type": "rsa",
                        "certificate_sig_alg": "sha256WithRSAEncryption",
                        "certificate_key_alg": "rsaEncryption",
                        "certificate_subject": "CN=EC2AMAZ-2GNPPAQ",
                        "source_ip": "193.93.62.11",
                        "certificate_exponent": "65537",
                        "certificate_key_length": 2048,
                        "dest_ip": "172.31.81.98",
                        "certificate_not_valid_before": 1644751334,
                        "uid": "CPgY6C2m1WXehA0Nsa01",
                        "dest_port": 3389,
                        "certificate_version": 3,
                        "certificate_serial": "76FDB38B8D5AA88844250EFE0EA89026",
                        "certificate_issuer": "CN=EC2AMAZ-2GNPPAQ"
                    }
            }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        x509_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'x509-certificate')

        assert x509_obj is not None
        assert x509_obj['subject'] == "CN=EC2AMAZ-2GNPPAQ"
        assert x509_obj['issuer'] == "CN=EC2AMAZ-2GNPPAQ"

    def test_network_traffic_json_to_stix(self):
        """to test network-traffic stix object properties"""

        data = \
            {
                "conn":
                    {
                        "orig_pkts": 14,
                        "epochdate": 1647598741.40136,
                        "orig_ttl": 109,
                        "resp_bytes": 1603,
                        "missed_bytes_resp": 0,
                        "duration": "Date",
                        "source_port": 39785,
                        "dest_port": 3389,
                        "resp_ttl": 128,
                        "conn_state": "RSTO",
                        "source_ip": "94.232.47.12",
                        "orig_bytes": 1226,
                        "resp_ip_bytes": 1999,
                        "orig_asn": "AS51036 JSC Zenit-PPM-Technology",
                        "resp_pkts": 8,
                        "proto": "tcp",
                        "orig_cc": "RU",
                        "orig_ip_bytes": 1910,
                        "history": "ShADdaR",
                        "dest_ip": "172.31.81.98",
                        "start_ts": 1647598741.40136,
                        "missed_bytes_orig": 0,
                        "uid": "CcZ7DV3CWxqDTeq2wi01",
                        "local_resp": 'true',
                        "local_orig": 'false',
                        "conn_state_full": "Originator aborted",
                        "service": "ssl"
                    }
            }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        connection_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'network-traffic')

        assert connection_obj is not None
        assert connection_obj["type"] == 'network-traffic'
        assert connection_obj["src_port"] == 39785
        assert connection_obj["dst_port"] == 3389

    def test_ssl_json_to_stix(self):
        """  to test x-darktrace-ssl custom object properties  """
        data = \
            {
                "ssl":
                    {
                        "epochdate": 1647422782.822214,
                        "total_client_ciphers": 50,
                        "validation_status": "unable to get local issuer certificate",
                        "client_hello_seen": 'true',
                        "ja3_client_fingerprint": "75fb48a465416d66291fb52a733d4787",
                        "source_port": 51797,
                        "dest_port": 3389,
                        "established": 'true',
                        "source_ip": "185.190.24.86",
                        "issuer": "CN=EC2AMAZ-2GNPPAQ",
                        "cipher": "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                        "dest_ip": "172.31.81.98",
                        "cert_chain_fuids": "FZ0NMJ17z414GCruTl01",
                        "curve": "secp384r1",
                        "uid": "Cl1dpm2TNyrsDI6yM801",
                        "version": "TLS1.0",
                        "ja3s_server_fingerprint": "bcf3a836c82d12ee988005fb0c011445",
                        "subject": "CN=EC2AMAZ-2GNPPAQ",
                        "resumed": 'false'
                    }
            }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        ssl_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'x509-certificate')

        assert ssl_obj['version'] == 'TLS1.0'
        assert ssl_obj['extensions']['x-darktrace-ssl']['is_resumed'] == 'false'
        assert ssl_obj['extensions']['x-darktrace-ssl']['total_ciphers'] == 50
        assert ssl_obj['extensions']['x-darktrace-ssl']['validation_status'] == 'unable to get local issuer certificate'
        assert ssl_obj['extensions']['x-darktrace-ssl']['is_client_hello_seen'] == 'true'

    def test_conn_json_to_stix(self):
        """to test x-darktrace-conn custom object properties"""

        data = \
            {
                "conn":
                    {
                        "orig_pkts": 3,
                        "epochdate": 1648187581.293184,
                        "orig_ttl": 109,
                        "resp_bytes": 0,
                        "conn_state_full": "Responder aborted",
                        "history": "Shr",
                        "dest_port": 3389,
                        "resp_ttl": 128,
                        "conn_state": "RSTR",
                        "source_port": 32781,
                        "orig_bytes": 0,
                        "resp_ip_bytes": 228,
                        "source_ip": "94.232.47.63",
                        "orig_asn": "AS51036 JSC Zenit-PPM-Technology",
                        "proto": "tcp",
                        "orig_cc": "RU",
                        "resp_pkts": 4,
                        "orig_ip_bytes": 176,
                        "dest_ip": "172.31.81.98",
                        "start_ts": 1648187581.293184,
                        "missed_bytes_orig": 0,
                        "uid": "C7hEYQ30RI4Pr0zseh01",
                        "missed_bytes_resp": 0,
                        "local_resp": 'true',
                        "local_orig": 'false',
                        "duration": 20.535259008407593
                    }
            }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        conn_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'network-traffic')

        assert conn_obj['extensions']['x-darktrace-conn']['missed_bytes_resp'] == 0
        assert conn_obj['extensions']['x-darktrace-conn']['orig_country_code'] == 'RU'
        assert conn_obj['extensions']['x-darktrace-conn']['is_locally_responded'] == 'true'

    def test_rdp_json_to_stix(self):
        """to test x-darktrace-rdp custom object properties"""

        data = \
            {
                "rdp":
                    {
                        "epochdate": 1647855167.997449,
                        "source_ip": "94.232.47.15",
                        "source_port": 53606,
                        "dest_ip": "172.31.81.98",
                        "cookie": "hello",
                        "dest_port": 3389,
                        "uid": "CT26Og19jDlyl5IjBc01",
                        "security_protocol": "HYBRID",
                        "cert_count": 0,
                        "result": "encrypted"
                    }
            }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        rdp_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'network-traffic')

        assert rdp_obj['extensions']['x-darktrace-rdp']['cookie'] == 'hello'
        assert rdp_obj['extensions']['x-darktrace-rdp']['security_protocol'] == 'HYBRID'

    def test_http_json_to_stix(self):
        """to test x-oca-event object properties"""

        data = \
            {
                "http":
                    {
                        "epochdate": 1647342620.459522,
                        "source_port": 62283,
                        "host": "www.darktrace.com",
                        "trans_depth": 1,
                        "uri": "/en/darktrace-antigena/",
                        "dest_port": 80,
                        "source_ip": "172.31.81.98",
                        "response_body_len": 0,
                        "redirect_location": "https://www.darktrace.com/en/darktrace-antigena/",
                        "dest_ip": "104.20.203.23",
                        "client_header_names": [
                            "HOST",
                            "CONNECTION",
                            "UPGRADE-INSECURE-REQUESTS",
                            "USER-AGENT",
                            "ACCEPT",
                            "ACCEPT-ENCODING",
                            "ACCEPT-LANGUAGE",
                            "COOKIE"
                        ],
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                      "(KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                        "uid": "CSVt7v2rT7aukksv3e01",
                        "version": "1.1",
                        "status_msg": "Moved Permanently",
                        "method": "GET",
                        "status_code": 301,
                        "request_body_len": 0
                    }
            }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        http_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'network-traffic')

        assert http_obj['extensions']['x-darktrace-http']['redirect_location'] == 'https://www.darktrace.com' \
                                                                                  '/en/darktrace-antigena/'
        assert http_obj['extensions']['x-darktrace-http']['status_code'] == 301
        assert http_obj['extensions']['x-darktrace-http']['status_msg'] == 'Moved Permanently'

    def test_ftp_json_to_stix(self):
        """to test x-darktrace-ftp custom object properties"""

        data = \
            {
                "ftp":
                    {
                        "epochdate": 1647513572.325977,
                        "source_ip": "172.31.81.98",
                        "user": "anonymous",
                        "dest_ip": "204.76.241.31",
                        "reply_msg": "Entering Passive Mode (204,76,241,31,205,14).",
                        "dest_port": 21,
                        "uid": "CnfvJM3aBJnAMsXnj601",
                        "reply_code": 227,
                        "command": "PASV",
                        "source_port": 52491
                    }
            }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        ftp_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'network-traffic')

        assert ftp_obj['extensions']['x-darktrace-ftp']['client_command'] == 'PASV'
        assert ftp_obj['extensions']['x-darktrace-ftp']['reply_code'] == 227

    def test_dns_json_to_stix(self):
        """
        to test x-darktrace-dns custom object properties
        """
        data = \
            {
                "dns":
                    {
                        "epochdate": 1647859960.933582,
                        "source_ip": "172.31.81.98",
                        "trans_id": 28521,
                        "details": "Request.",
                        "dest_ip": "224.0.0.252",
                        "source_port": 59985,
                        "dest_port": 5355,
                        "uid": "CKCJJUAVMd8vDbKzi01",
                        "query_type": "*",
                        "query": "ec2amaz-2gnppaq",
                        "query_class": "C_INTERNET",
                        "proto": "udp",
                        "TTLs": [149],
                    }
            }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        dns_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'network-traffic')

        assert dns_obj['extensions']['x-darktrace-dns']['transaction_id'] == 28521
        assert dns_obj['extensions']['x-darktrace-dns']['details'] == 'Request.'
        assert dns_obj['extensions']['x-darktrace-dns']['query_class'] == 'C_INTERNET'

    def test_dhcp_json_to_stix(self):
        """
        to test x-darktrace-dhcp custom object properties
        """
        data = \
            {
                "dhcp":
                    {
                        "mac": "12:2f:23:46:35:5b",
                        "epochdate": 1647859960.93352,
                        "source_ip": "172.31.81.98",
                        "trans_id": 1512448313,
                        "dest_ip": "172.31.80.1",
                        "dest_port": 67,
                        "uid": "C5FYmbt4Q19KyCfNg01",
                        "source_port": 68,
                        "host_name": "EC2AMAZ-2GNPPAQ",
                        "requested_ip": "0.0.0.0",
                        "dhcp_type": "DHCP::request"
                    }
            }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        dhcp_obj = TestDarktraceResultsToStix.get_first_of_type(objects.values(), 'network-traffic')

        assert dhcp_obj['extensions']['x-darktrace-dhcp']['host_name'] == 'EC2AMAZ-2GNPPAQ'
        assert dhcp_obj['extensions']['x-darktrace-dhcp']['dhcp_type'] == 'DHCP::request'
