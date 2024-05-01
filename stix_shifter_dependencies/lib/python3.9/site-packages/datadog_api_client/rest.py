# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.

import json
import logging
import re
import ssl
from urllib.parse import urlencode
import zlib

import urllib3  # type: ignore

from datadog_api_client.exceptions import (
    ApiException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    ServiceException,
    ApiValueError,
)


logger = logging.getLogger(__name__)


class RESTClientObject:
    def __init__(self, configuration, pools_size=4, maxsize=4):
        # urllib3.PoolManager will pass all kw parameters to connectionpool
        # https://github.com/shazow/urllib3/blob/f9409436f83aeb79fbaf090181cd81b784f1b8ce/urllib3/poolmanager.py#L75
        # https://github.com/shazow/urllib3/blob/f9409436f83aeb79fbaf090181cd81b784f1b8ce/urllib3/connectionpool.py#L680
        # maxsize is the number of requests to host that are allowed in parallel
        # Custom SSL certificates and client certificates: http://urllib3.readthedocs.io/en/latest/advanced-usage.html

        # cert_reqs
        if configuration.verify_ssl:
            cert_reqs = ssl.CERT_REQUIRED
        else:
            cert_reqs = ssl.CERT_NONE

        addition_pool_args = {}
        if configuration.assert_hostname is not None:
            addition_pool_args["assert_hostname"] = configuration.assert_hostname

        if configuration.retries is not None:
            addition_pool_args["retries"] = configuration.retries

        if configuration.socket_options is not None:
            addition_pool_args["socket_options"] = configuration.socket_options

        # https pool manager
        if configuration.proxy:
            self.pool_manager = urllib3.ProxyManager(
                num_pools=pools_size,
                maxsize=maxsize,
                cert_reqs=cert_reqs,
                ca_certs=configuration.ssl_ca_cert,
                cert_file=configuration.cert_file,
                key_file=configuration.key_file,
                proxy_url=configuration.proxy,
                proxy_headers=configuration.proxy_headers,
                **addition_pool_args
            )
        else:
            self.pool_manager = urllib3.PoolManager(
                num_pools=pools_size,
                maxsize=maxsize,
                cert_reqs=cert_reqs,
                ca_certs=configuration.ssl_ca_cert,
                cert_file=configuration.cert_file,
                key_file=configuration.key_file,
                **addition_pool_args
            )

    def request(
        self,
        method,
        url,
        query_params=None,
        headers=None,
        body=None,
        post_params=None,
        preload_content=True,
        request_timeout=None,
    ):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param query_params: query parameters in the url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param preload_content: if False, the urllib3.HTTPResponse object will
                                be returned without reading/decoding response
                                data. Default is True.
        :param request_timeout: timeout setting for this request. If one
                                number provided, it will be total request
                                timeout. It can also be a pair (tuple) of
                                (connection, read) timeouts.
        """
        method = method.upper()

        if post_params and body:
            raise ApiValueError("body parameter cannot be used with post_params parameter.")

        post_params = post_params or {}
        headers = headers or {}

        timeout = None
        if request_timeout:
            if isinstance(request_timeout, (int, float)):
                timeout = urllib3.Timeout(total=request_timeout)
            elif isinstance(request_timeout, tuple) and len(request_timeout) == 2:
                timeout = urllib3.Timeout(connect=request_timeout[0], read=request_timeout[1])

        try:
            # For `POST`, `PUT`, `PATCH`, `OPTIONS`, `DELETE`
            if method in ("POST", "PUT", "PATCH", "OPTIONS", "DELETE"):
                # Only set a default Content-Type for POST, PUT, PATCH and OPTIONS requests
                if method != "DELETE" and "Content-Type" not in headers:
                    headers["Content-Type"] = "application/json"
                if query_params:
                    url += "?" + urlencode(query_params)
                if "Content-Type" not in headers or re.search("json", headers["Content-Type"], re.IGNORECASE):
                    request_body = None
                    if body is not None:
                        request_body = json.dumps(body)
                        if headers.get("Content-Encoding") == "gzip":
                            compressor = zlib.compressobj(wbits=16 + zlib.MAX_WBITS)
                            request_body = compressor.compress(request_body.encode("utf-8")) + compressor.flush()
                        elif headers.get("Content-Encoding") == "deflate":
                            request_body = zlib.compress(request_body.encode("utf-8"))
                        elif headers.get("Content-Encoding") == "zstd1":
                            import zstandard as zstd

                            compressor = zstd.ZstdCompressor()
                            request_body = compressor.compress(request_body.encode("utf-8"))
                    r = self.pool_manager.request(
                        method,
                        url,
                        body=request_body,
                        preload_content=preload_content,
                        timeout=timeout,
                        headers=headers,
                    )
                elif headers["Content-Type"] == "application/x-www-form-urlencoded":
                    r = self.pool_manager.request(
                        method,
                        url,
                        fields=post_params,
                        encode_multipart=False,
                        preload_content=preload_content,
                        timeout=timeout,
                        headers=headers,
                    )
                elif headers["Content-Type"] == "multipart/form-data":
                    # must del headers['Content-Type'], or the correct
                    # Content-Type which generated by urllib3 will be
                    # overwritten.
                    del headers["Content-Type"]
                    r = self.pool_manager.request(
                        method,
                        url,
                        fields=post_params,
                        encode_multipart=True,
                        preload_content=preload_content,
                        timeout=timeout,
                        headers=headers,
                    )
                # Pass a `string` parameter directly in the body to support
                # other content types than Json when `body` argument is
                # provided in serialized form
                elif isinstance(body, (str, bytes)):
                    request_body = body
                    r = self.pool_manager.request(
                        method,
                        url,
                        body=request_body,
                        preload_content=preload_content,
                        timeout=timeout,
                        headers=headers,
                    )
                else:
                    # Cannot generate the request from given parameters
                    msg = """Cannot prepare a request message for provided
                             arguments. Please check that your arguments match
                             declared content type."""
                    raise ApiException(status=0, reason=msg)
            # For `GET`, `HEAD`
            else:
                r = self.pool_manager.request(
                    method, url, fields=query_params, preload_content=preload_content, timeout=timeout, headers=headers
                )
        except urllib3.exceptions.SSLError as e:
            msg = "{0}\n{1}".format(type(e).__name__, str(e))
            raise ApiException(status=0, reason=msg)

        if preload_content:
            # log response body
            logger.debug("response body: %s", r.data)

        if not 200 <= r.status <= 299:
            if r.status == 401:
                raise UnauthorizedException(http_resp=r)

            if r.status == 403:
                raise ForbiddenException(http_resp=r)

            if r.status == 404:
                raise NotFoundException(http_resp=r)

            if 500 <= r.status <= 599:
                raise ServiceException(http_resp=r)

            raise ApiException(http_resp=r)

        return r


class _AioSonicResponseWrapper:
    def __init__(self, response, data):
        self.response = response
        self.status = response.status_code
        self.reason = response.response_initial.get("reason")
        self.data = data

    def getheaders(self):
        return self.response.headers


class AsyncRESTClientObject:
    def __init__(self, configuration):
        import aiosonic  # type: ignore

        proxy = None
        if configuration.proxy:
            proxy = aiosonic.Proxy(configuration.proxy, configuration.proxy_headers)
        self._client = aiosonic.HTTPClient(proxy=proxy)

    async def request(
        self,
        method,
        url,
        query_params=None,
        headers=None,
        body=None,
        post_params=None,
        preload_content=True,
        request_timeout=None,
    ):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param query_params: query parameters in the url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param preload_content: if False, the raw HTTP response object will
                                be returned without reading/decoding response
                                data. Default is True.
        :param request_timeout: timeout setting for this request. If one
                                number provided, it will be total request
                                timeout. It can also be a pair (tuple) of
                                (connection, read) timeouts.
        """
        assert not post_params, "not supported for now"
        request_body = None
        if (
            "Content-Type" not in headers
            or re.search("json", headers["Content-Type"], re.IGNORECASE)
            and body is not None
        ):
            request_body = json.dumps(body)
            if headers.get("Content-Encoding") == "gzip":
                compress = zlib.compressobj(wbits=16 + zlib.MAX_WBITS)
                request_body = compress.compress(request_body.encode("utf-8")) + compress.flush()
            elif headers.get("Content-Encoding") == "deflate":
                request_body = zlib.compress(request_body.encode("utf-8"))
        response = await self._client.request(
            url, method, headers, query_params, request_body, timeouts=request_timeout
        )

        if not 200 <= response.status_code <= 299:
            data = b""
            if preload_content:
                data = await response.content()
            r = _AioSonicResponseWrapper(response, data)

            if response.status_code == 401:
                raise UnauthorizedException(http_resp=r)

            if response.status_code == 403:
                raise ForbiddenException(http_resp=r)

            if response.status_code == 404:
                raise NotFoundException(http_resp=r)

            if 500 <= response.status_code <= 599:
                raise ServiceException(http_resp=r)

            raise ApiException(http_resp=r)

        return response
