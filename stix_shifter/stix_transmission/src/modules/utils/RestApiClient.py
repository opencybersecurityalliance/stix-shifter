import requests
import sys
import base64
import ssl
import json
import collections
import urllib.parse

# This is a simple HTTP client that can be used to access the REST API
class RestApiClient:

    def __init__(self, host, port = None, cert=None, headers={}, urlModifierFunction=None):
        server_ip = host
        if port is not None:
            server_ip += ":" + str(port)            
        self.server_ip = server_ip
        self.cert_file = None
        if cert is not None:
            # put cert/key pair into a file to read it later
            cert_file_name = "cert.pem"
            certfile = open(cert_file_name, "w+")
            certfile.write(cert)
            certfile.close()

            with open(cert_file_name, 'w+') as f:
                try:
                    f.write(cert)
                    f.close()
                except IOError:
                    print('Failed to setup certificate')

            self.cert_file = cert_file_name
        self.headers = headers
        self.urlModifierFunction = urlModifierFunction

    # This method is used to set up an HTTP request and send it to the server
    def call_api(self, endpoint, method, headers=None, params=[], data=None, urldata=None, print_request=False):
        url = None
        actual_headers = self.headers.copy()
        if headers is not None:
            for header_key in headers:
                actual_headers[header_key] = headers[header_key]

        if urldata is not None:
            urldata = urllib.parse.urlencode(urldata)
            if '?' in endpoint:
                endpoint += '&'
            else:
                endpoint += '?'
            endpoint += urldata            

        if self.urlModifierFunction is not None:
            url = self.urlModifierFunction(self.server_ip, endpoint, actual_headers)
        else:
            url = 'https://' + self.server_ip + '/' + endpoint
        try:
            
            call = getattr(requests, method.lower())
            response = call(url, headers=actual_headers, data=data, cert=self.cert_file)            
            response.raise_for_status()
            if 'headers' in dir(response) and isinstance(response.headers, collections.Mapping) and 'Content-Type' in response.headers \
                            and "Depricated" in response.headers['Content-Type']:
                print("WARNING: " + response.headers['Content-Type'], file=sys.stderr)
            return ResponseWrapper(response)
        except Exception as e:
            print('exception occured during requiesting url: ' + str(e))
            raise e

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
