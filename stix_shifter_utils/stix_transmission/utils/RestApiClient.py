import requests
from requests.packages.urllib3.util.retry import Retry
from stix_shifter_utils.stix_transmission.utils.timeout_http_adapter import TimeoutHTTPAdapter
import sys
from collections.abc import Mapping
import os
import errno
import uuid
from stix_shifter_utils.utils import logger
import threading

# This is a simple HTTP client that can be used to access the REST API

RETRY_MAX_DEFAULT = 1
CONNECT_TIMEOUT_DEFAULT = 2


class InterruptableThread(threading.Thread):
    def __init__(self, func, *args, **kwargs):
        threading.Thread.__init__(self)
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._result = None
        self.daemon = True

    def run(self):
        self._result = self._func(*self._args, **self._kwargs)

    @property
    def result(self):
        return self._result


def exception_catcher(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as ex:
        return ex


class RestApiClient:
    """
    Deprecated RestApiClient, 
    consider using RestApiClientAsync
    """
    # cert_verify can be
    #  True -- do proper signed cert check that is in trust store,
    #  False -- skip all cert checks,
    #  or The String content of your self signed cert required for TLS communication
    def __init__(self, host, port=None, headers={}, url_modifier_function=None, cert_verify=True,  auth=None):
        self.retry_max = os.getenv('STIXSHIFTER_RETRY_MAX', RETRY_MAX_DEFAULT)
        self.retry_max = int(self.retry_max)
        self.connect_timeout = os.getenv('STIXSHIFTER_CONNECT_TIMEOUT', CONNECT_TIMEOUT_DEFAULT)
        self.connect_timeout = int(self.connect_timeout)

        self.logger = logger.set_logger(__name__)
        unique_file_handle = uuid.uuid4()
        self.server_cert_name = "/tmp/{0}-server_cert.pem".format(unique_file_handle)
        server_ip = host
        if port is not None:
            server_ip += ":" + str(port)
        self.server_ip = server_ip

        self.server_cert_file_content_exists = False
        self.server_cert_content = False
        if isinstance(cert_verify, bool):
            # verify certificate non self signed case
            if cert_verify:
                self.server_cert_content = True
        # self signed cert provided
        elif isinstance(cert_verify, str):
            self.server_cert_content = self.server_cert_name
            self.server_cert_file_content_exists = True
            self.server_cert_file_content = cert_verify

        self.headers = headers
        self.url_modifier_function = url_modifier_function
        self.auth = auth

        self.logger.warning('Deprecated RestApiClient, consider using RestApiClientAsync')

    # This method is used to set up an HTTP request and send it to the server
    def call_api(self, endpoint, method, headers=None, data=None, urldata=None, timeout=None):
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
                session = requests.Session()
                retry_strategy = Retry(total=self.retry_max, backoff_factor=0, status_forcelist=[429, 500, 502, 503, 504],
                                       allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"])
                session.mount("https://", TimeoutHTTPAdapter(max_retries=retry_strategy))
                call = getattr(session, method.lower())
                it = InterruptableThread(exception_catcher, call, url, headers=actual_headers, params=urldata, data=data,
                                         verify=self.server_cert_content,
                                         timeout=(self.connect_timeout, timeout),
                                         auth=self.auth)
                it.start()
                it.join(timeout)
                if it.is_alive():
                    raise Exception(f'timeout_error ({timeout} sec)')
                response = it.result
                if isinstance(response, Exception):
                    raise response
                if 'headers' in dir(response) and isinstance(response.headers, Mapping) and \
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

    def raise_for_status(self):
        return self.response.raise_for_status()

    @property
    def headers(self):
        return self.response.headers

    @property
    def bytes(self):
        return self.response.content

    @property
    def code(self):
        return self.response.status_code