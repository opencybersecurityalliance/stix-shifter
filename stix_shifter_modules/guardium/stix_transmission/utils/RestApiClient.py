import requests
from requests_toolbelt.adapters import host_header_ssl
import sys
import collections
import urllib.parse
import os
import errno

# This is a simple HTTP client that can be used to access the REST API
CLIENT_CERT_NAME = "client_cert.pem"
SERVER_CERT_NAME = "server_cert.pem"

class RestApiClient:
    #cert_verify can be True -- do proper signed cert check, False -- skip all cert checks, or a Cert -- use the proper cleint side cert
    #mutual_auth is in the case the gateway is being used
    def __init__(self, host, port=None, cert=None, headers={}, url_modifier_function=None, cert_verify=True,
                 mutual_auth=False, sni=None):
        print("Guardium Version of RestApiClient ----")
        server_ip = host
        if port is not None:
            server_ip += ":" + str(port)
        self.server_ip = server_ip
        #sni is none unless we are using a server cert
        self.sni = None
        #Gateway Case -- use client cert cert_verify is None
        if mutual_auth:
            self.server_cert_content = None
            self.server_cert_file_content_exists = False
            self.client_cert_content = CLIENT_CERT_NAME
            self.client_cert_file_content_exists = True
            self.client_cert_file_content = cert
        #verify is true or false
        elif isinstance(cert_verify, bool):
            if cert_verify:
                self.server_cert_content = True
                self.server_cert_file_content_exists = False
                self.client_cert_content = None
                self.client_cert_file_content_exists = False
            else:
                self.server_cert_content = False
                self.server_cert_file_content_exists = False
                self.client_cert_content = None
                self.client_cert_file_content_exists = False
        #server cert provided
        elif isinstance(cert_verify, str):
            self.server_cert_content = SERVER_CERT_NAME
            self.server_cert_file_content_exists = True
            self.server_cert_file_content = cert_verify
            self.client_cert_content = None
            self.client_cert_file_content_exists = False
            if sni is not None:
                self.sni = sni

        self.headers = headers
        self.url_modifier_function = url_modifier_function

    # This method is used to set up an HTTP request and send it to the server
    def call_api(self, endpoint, method, headers=None, params=[], data=None, urldata=None):
        try:

            # convert client cert to file
            if self.client_cert_file_content_exists is True:
                with open(CLIENT_CERT_NAME, 'w') as f:
                    try:
                        f.write(self.client_cert_file_content)
                    except IOError:
                        print('Failed to setup certificate')

            # covnert server cert to file
            if self.server_cert_file_content_exists is True:
                with open(SERVER_CERT_NAME, 'w') as f:
                    try:
                        f.write(self.server_cert_file_content)
                    except IOError:
                        print('Failed to setup certificate')

            url = None
            actual_headers = self.headers.copy()
            if headers is not None:
                for header_key in headers:
                    actual_headers[header_key] = headers[header_key]

            if urldata:
                urldata = urllib.parse.urlencode(urldata)
                if '?' in endpoint:
                    endpoint += '&'
                else:
                    endpoint += '?'
                endpoint += urldata

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
#
# This is original call 
                #response = call(url, headers=actual_headers,
                                #cert=self.client_cert_content, data=data, verify=self.server_cert_content)
# Replaced with
#  Subroto: Replaced the above line with the following because params is not passed to the call though the
#  'call_api' signature has params as a parameter.
#
# This code is added because Guardium api requires 'params' to be sent to get the
# Authorization token AND 'data' to be sent to retrieve report information.
#
                if (not params or params is None):
                    response = call(url, headers=actual_headers,
                                    cert=self.client_cert_content, data=data, verify=self.server_cert_content)
                #
                elif data is None and params is not None:
                    response = call(url, headers=actual_headers, cert=self.client_cert_content,
                                    params=params, verify=self.server_cert_content)
                #
                else:
                    response = call(url, headers=actual_headers, cert=self.client_cert_content,
                                    params=params, data=data, verify=self.server_cert_content)
                #
# End Change

                if 'headers' in dir(response) and isinstance(response.headers, collections.Mapping) and 'Content-Type' in response.headers \
                        and "Deprecated" in response.headers['Content-Type']:
                    print("WARNING: " +
                          response.headers['Content-Type'], file=sys.stderr)
                return ResponseWrapper(response)
            except Exception as e:
                print('exception occured during requesting url: ' + str(e))
                raise e
        finally:
            if self.server_cert_file_content_exists is True:
                try:
                    os.remove(SERVER_CERT_NAME)
                except OSError as e:
                    if e.errno != errno.ENOENT:
                        raise
            if self.client_cert_file_content_exists is True:
                try:
                    os.remove(CLIENT_CERT_NAME)
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
