from aiohttp_retry import RetryClient, ExponentialRetry
from aiohttp import ClientTimeout
from asyncio.exceptions import TimeoutError
import aiohttp
from collections.abc import Mapping
import os
import errno
import ssl
import sys
import threading
import uuid

from stix_shifter_utils.utils import logger
 
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


class RestApiClientAsync:
    # cert_verify (assigned to self.ssl_context) can be
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

        self.server_cert_file_content = None
        self.ssl_context = False
        
        if isinstance(cert_verify, bool):
            # verify certificate non self signed case
            if cert_verify:
                self.ssl_context = True
        # self signed cert provided
        elif isinstance(cert_verify, str):
            self.server_cert_file_content = cert_verify

        self.headers = headers
        self.url_modifier_function = url_modifier_function
        self.auth = auth

    # This method is used to set up an HTTP request and send it to the server
    async def call_api(self, endpoint, method, headers=None, cookies=None, data=None, urldata=None, timeout=None):
        try:
            # covnert server cert to file
            if self.server_cert_file_content:
                with open(self.server_cert_name, 'w') as f:
                    try:
                        f.write(self.server_cert_file_content)
                    except IOError:
                        self.logger.error('Failed to setup certificate')

                self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                self.ssl_context.load_verify_locations(self.server_cert_name)
                self.ssl_context.verify_mode = ssl.CERT_REQUIRED
                self.ssl_context.check_hostname = True

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
                client_timeout = ClientTimeout(connect=self.connect_timeout, total=timeout) # https://docs.aiohttp.org/en/stable/client_reference.html?highlight=timeout#aiohttp.ClientTimeout
                retry_options = ExponentialRetry(attempts=self.retry_max, statuses=[429, 500, 502, 503, 504])
                async with RetryClient(retry_options=retry_options) as client:
                    call = getattr(client, method.lower()) 

                    async with call(url, headers=actual_headers, params=urldata, data=data,
                                            ssl=self.ssl_context,
                                            timeout=client_timeout,
                                            cookies=cookies,
                                            auth=self.auth) as response:

                        respWrapper = ResponseWrapper(response, client)
                        await respWrapper.wait()

                        if respWrapper.code == 429:
                            raise Exception(f'Max retries exceeded. too_many_requests with max retry ({self.retry_max})')

                        if 'headers' in dir(response) and isinstance(response.headers, Mapping) and \
                            'Content-Type' in response.headers and "Deprecated" in response.headers['Content-Type']:

                            self.logger.error("WARNING: " + response.headers['Content-Type'], file=sys.stderr)

                        return respWrapper
            except aiohttp.client_exceptions.ServerTimeoutError as e:
                raise Exception(f'server timeout_error ({self.connect_timeout} sec)')
            except aiohttp.client_exceptions.ClientConnectorError as e:
                raise Exception(f'client_connector_error: ({e})')
            except TimeoutError as e:
                raise Exception(f'timeout_error ({timeout} sec)')
            except Exception as e:
                self.logger.error('exception occured during requesting url: ' + str(e) + " " + str(type(e)))
                raise e
        finally:
            if self.server_cert_file_content:
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
    _content = None
    _headers = None
    _code = None

    def __init__(self, response, client=None):
        self.response = response
        self.client = client

    async def wait(self):
        self._content = await self.response.content.read()
        self._headers = self.response.headers
        self._code = self.response.status
    
    def read(self):
        return self._content

    def raise_for_status(self):
        return self.response.raise_for_status()

    def get_cookies(self, url):
        cookie = None
        if self.client:
            cookie = self.client._client.cookie_jar.filter_cookies(url)
        return cookie

    @property
    def headers(self):
        return self._headers

    @property
    def content(self):
        return self._content

    @property
    def bytes(self):
        return self._content

    @property
    def code(self):
        return self._code

    @headers.setter
    def headers(self, v):
        self._headers = v

    @content.setter
    def content(self, v):
        self._content = v

    @code.setter
    def code(self, v):
        self._code = v
