import requests
from requests_toolbelt.adapters import host_header_ssl
import sys
import collections
import os
import errno
import uuid

from stix_shifter_utils.utils import logger

# This is a simple HTTP client that can be used to access the REST API


class RestApiClient:
    # cert_verify can be
    #  True -- do proper signed cert check that is in trust store,
    #  False -- skip all cert checks,
    #  or The String content of your self signed cert required for TLS communication
    def __init__(self, host, port=None, headers={}, url_modifier_function=None, cert_verify=True,  sni=None):
        self.logger = logger.set_logger(__name__)
        unique_file_handle = uuid.uuid4()
        self.server_cert_name = "/tmp/{0}-server_cert.pem".format(unique_file_handle)
        server_ip = host
        if port is not None:
            server_ip += ":" + str(port)
        self.server_ip = server_ip
        # sni is none unless we are using a server cert
        self.sni = None

        if isinstance(cert_verify, bool):
            # verify certificate non self signed case
            if cert_verify:
                self.server_cert_content = True
                self.server_cert_file_content_exists = False
            # ignore certificates all together
            else:
                self.server_cert_content = False
                self.server_cert_file_content_exists = False
        # self signed cert provided
        elif isinstance(cert_verify, str):
            self.server_cert_content = self.server_cert_name
            self.server_cert_file_content_exists = True
            self.server_cert_file_content = cert_verify
            if sni is not None:
                self.sni = sni

        self.headers = headers
        self.url_modifier_function = url_modifier_function

    # This method is used to set up an HTTP request and send it to the server
    def call_api(self, endpoint, method, headers=None, params=[], data=None, urldata=None, timeout=None):
        try:
            # covnert server cert to file
            if self.server_cert_file_content_exists is True:
                with open(self.server_cert_name, 'w') as f:
                    try:
                        f.write(self.server_cert_file_content)
                    except IOError:
                        self.logger.error('Failed to setup certificate')

            url = None
            actual_headers = self.headers.copy()
            if headers is not None:
                for header_key in headers:
                    actual_headers[header_key] = headers[header_key]

            if self.url_modifier_function is not None:
                url = self.url_modifier_function(
                    self.server_ip, endpoint, actual_headers)
            else:
                url = 'https://' + self.server_ip + '/' + endpoint
            try:
                call = getattr(requests, method.lower())

                # only use the tool belt session in case of SNI for safety
                if self.sni is not None:
                    session = requests.Session()
                    call = getattr(session, method.lower())
                    session.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
                    actual_headers["Host"] = self.sni

                response = call(url, headers=actual_headers, params=urldata, data=data, verify=self.server_cert_content,
                                timeout=timeout)

                if 'headers' in dir(response) and isinstance(response.headers, collections.Mapping) and \
                   'Content-Type' in response.headers and "Deprecated" in response.headers['Content-Type']:
                    self.logger.error("WARNING: " +
                          response.headers['Content-Type'], file=sys.stderr)
                return ResponseWrapper(response)
            except Exception as e:
                self.logger.error('exception occured during requesting url: ' + str(e))
                raise e
        finally:
            if self.server_cert_file_content_exists is True:
                try:
                    os.remove(self.server_cert_name)
                except OSError as e:
                    if e.errno != errno.ENOENT:
                        raise

    # Simple getters that can be used to inspect the state of this client.
    def get_headers(self):
        return self.headers.copy()

    def get_server_ip(self):
        return self.server_ip


class ResponseWrapper:
    def __init__(self, response):
        self.response = response

    def read(self):
        return self.response.content

    @property
    def bytes(self):
        return self.response.content

    @property
    def code(self):
        return self.response.status_code
