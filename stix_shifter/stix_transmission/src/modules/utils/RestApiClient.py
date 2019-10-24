import requests
import sys
import collections
import urllib.parse
import os
import errno

# This is a simple HTTP client that can be used to access the REST API


class RestApiClient:

    def __init__(self, host, port=None, cert=None, headers={}, url_modifier_function=None, cert_verify=True):
        server_ip = host
        if port is not None:
            server_ip += ":" + str(port)
        self.server_ip = server_ip
        self.cert_verify = cert_verify
        self.cert = cert
        self.headers = headers
        self.url_modifier_function = url_modifier_function

    # This method is used to set up an HTTP request and send it to the server
    def call_api(self, endpoint, method, headers=None, params=[], data=None, urldata=None):
        self.client_cert = None
        self.server_cert = None
        try:
            if self.cert is not None:
                # put key/cert pair into a file to read it later
                self.client_cert = "client_cert.pem"
                with open(self.client_cert, 'w') as f:
                    try:
                        f.write(self.cert)
                    except IOError:
                        print('Failed to setup certificate')
            else:
                self.client_cert = self.cert

            # check for certificate
            if self.cert_verify is not True:
                # put key/cert pair into a file to read it later
                self.server_cert = "server_cert.pem"
                with open(self.server_cert, 'w') as f:
                    try:
                        f.write(self.cert)
                    except IOError:
                        print('Failed to setup certificate')
            else:
                self.server_cert = self.cert_verify

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
                response = call(url, headers=actual_headers,
                                cert=self.client_cert, data=data, verify=self.server_cert)

                if 'headers' in dir(response) and isinstance(response.headers, collections.Mapping) and 'Content-Type' in response.headers \
                        and "Deprecated" in response.headers['Content-Type']:
                    print("WARNING: " +
                          response.headers['Content-Type'], file=sys.stderr)
                return ResponseWrapper(response)
            except Exception as e:
                print('exception occured during requesting url: ' + str(e))
                raise e
        finally:
            if self.server_cert is not None:
                try:
                    os.remove(self.server_cert)
                except OSError as e:
                    if e.errno != errno.ENOENT:
                        raise
            if self.client_cert is not None:
                try:
                    os.remove(self.client_cert)
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
