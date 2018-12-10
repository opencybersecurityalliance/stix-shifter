from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import install_opener
from urllib.request import build_opener
from urllib.request import HTTPSHandler

import ssl
import sys
import base64
import os

class RestApiClient:

    def __init__(self, server_ip, user_name, password, cert):
        self.headers = {}

        if user_name and password:
            self.headers['Authorization'] = b"Basic " + base64.b64encode(
                (user_name + ':' + password).encode('ascii'))
        else:
            raise Exception('No valid credentials found in configuration.')

        self.server_ip = server_ip
        self.base_uri = '/api/'

        # Create a secure SSLContext
        # PROTOCOL_SSLv23 is misleading.  PROTOCOL_SSLv23 will use the highest
        # version of SSL or TLS that both the client and server supports.
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

        # SSL version 2 and SSL version 3 are insecure. The insecure versions
        # are disabled.
        context.verify_mode = ssl.CERT_REQUIRED
        if sys.version_info >= (3, 4):
            context.check_hostname = True

        check_hostname = True
        if cert is not None:
            # put cert/key pair into a file to read it later
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

            # The default QRadar certificate does not have a valid hostname,
            # so me must disable hostname checking.
            if sys.version_info >= (3, 4):
                context.check_hostname = False
            check_hostname = False

            # Instead of loading the default certificates load only the
            # certificates specified by the user.
            try:
                context.load_default_certs()
                context.load_cert_chain(certfile="cert.pem")
            except:
                print('Failed to load certificate')

            #os.remove("cert.pem")
        else:
            if sys.version_info >= (3, 4):
                # Python 3.4 and above has the improved load_default_certs()
                # function.
                context.load_default_certs(ssl.Purpose.CLIENT_AUTH)
            else:
                # Versions of Python before 3.4 do not have the
                # load_default_certs method.  set_default_verify_paths will
                # work on some, but not all systems.  It fails silently.  If
                # this call fails the certificate will fail to validate.
                context.set_default_verify_paths()

        install_opener(build_opener(
            HTTPSHandler(context=context, check_hostname=check_hostname)))

    # This method is used to set up an HTTP request and send it to the server
    def call_api(self, endpoint, method, headers=None, params=[], data=None):

        path = self.parse_path(endpoint, params)

        # If the caller specified customer headers merge them with the default
        # headers.
        actual_headers = self.headers.copy()
        if headers is not None:
            for header_key in headers:
                actual_headers[header_key] = headers[header_key]

        # Send the request and receive the response
        request = Request(
            'https://' + self.server_ip + self.base_uri + path,
            headers=actual_headers)
        request.get_method = lambda: method

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