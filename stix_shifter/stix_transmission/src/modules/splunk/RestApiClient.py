from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.request import install_opener
from urllib.request import build_opener
from urllib.request import HTTPSHandler
from .Utilities import *

import ssl
import sys
import base64
import json
import os

# This is a simple HTTP client that can be used to access the REST API
class RestApiClient:

    # Constructor for the RestApiClient Class
    def __init__(self, server_ip, auth=None, cert=None, output_mode='json', version=None):
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept': 'application/json'}
        # TODO: check version functionality

        if version is not None:
            self.headers['Version'] = version
        if auth is None:
            raise Exception('No valid credentials found in configuration.')
       
        self.server_ip = server_ip
        self.base_uri = server_ip
        self.output_mode = output_mode
        self.auth = auth

        # Create a secure SSLContext
        # PROTOCOL_SSLv23 is misleading.  PROTOCOL_SSLv23 will use the highest
        # version of SSL or TLS that both the client and server supports.
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

        # Disable ssl check
        context.verify_mode = ssl.CERT_NONE
        context.check_hostname = False
        check_hostname = False

        if cert is not None:
            cert_file_name = "cert.pem"
            certfile = open("cert.pem", "w+")
            certfile.write(cert)
            certfile.close()

            with open(cert_file_name, 'w+') as f:
                try:
                    f.write(cert)
                    f.close()
                except IOError:
                    print('Failed to setup certificate')

            try:
                context.load_default_certs()
                context.load_cert_chain(certfile="cert.pem")
            except:
                print('Failed to load certificate')

            os.remove("cert.pem")

        install_opener(build_opener(
            HTTPSHandler(context=context, check_hostname=check_hostname)))
        
        self.set_auth_token()  # set authorization token in header



    # This method is used to set up an HTTP request and send it to the server
    def call_api(self, endpoint, method, headers=None, params=[], data=None,
                 print_request=False):
        
        path = self.parse_path(endpoint, params)

        # If the caller specified customer headers merge them with the default
        # headers.
        actual_headers = self.headers.copy()
        if headers is not None:
            for header_key in headers:
                actual_headers[header_key] = headers[header_key]

        # Send the request and receive the response
        request = Request(
            'https://' + self.server_ip + '/' + path,
            headers=actual_headers)
        request.get_method = lambda: method

        # Print the request if print_request is True.
        if print_request:
            SampleUtilities.pretty_print_request(self, path, method,
                                                 headers=actual_headers)

        try:
            response = urlopen(request, data)
            response_info = response.info()
            if 'Deprecated' in response_info:

                # This version of the API is Deprecated. Print a warning to
                # stderr.
                print("WARNING: " + response_info['Deprecated'],
                      file=sys.stderr)

            # returns response object for opening url.
            return response
        except HTTPError as e:
            # an object which contains information similar to a request object
            return e
        except URLError as e:
            if (isinstance(e.reason, ssl.SSLError) and
                    e.reason.reason == "CERTIFICATE_VERIFY_FAILED"):
                print("Certificate verification failed.")
                sys.exit(3)
            else:
                raise e

    # This method constructs the query string
    def parse_path(self, endpoint, params):

        path = endpoint + '?'

        if isinstance(params, list):

            for kv in params:
                if kv[1]:
                    path += kv[0]+'='+quote(kv[1])+'&'

        else:
            for k, v in params.items():
                if params[k]:
                    path += k+'='+quote(v)+'&'

        # removes last '&' or hanging '?' if no params.
        return path[:len(path)-1]

    # Simple getters that can be used to inspect the state of this client.
    def get_headers(self):
        return self.headers.copy()

    def get_server_ip(self):
        return self.server_ip

    def get_base_uri(self):
        return self.base_uri

    def set_auth_token(self):
       
        data = {'username': self.auth['username'], 'password': self.auth['password'], 'output_mode': self.output_mode}
        endpoint = self.endpoint_start + 'auth/login'
        
        try:
            data = urlencode(data)
            data = data.encode('utf-8')
            response_json = json.load(self.call_api(endpoint, 'POST', None, data=data))
            self.headers['Authorization'] = "Splunk " + response_json['sessionKey']
        except Exception as e:
            print('Authentication error occured while getting auth token.')
            raise e

