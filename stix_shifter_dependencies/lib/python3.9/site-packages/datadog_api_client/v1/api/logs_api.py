# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, Union
import warnings

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    UnsetType,
    unset,
)
from datadog_api_client.v1.model.logs_list_response import LogsListResponse
from datadog_api_client.v1.model.logs_list_request import LogsListRequest
from datadog_api_client.v1.model.content_encoding import ContentEncoding
from datadog_api_client.v1.model.http_log import HTTPLog


class LogsApi:
    """
    Search your logs and send them to your Datadog platform over HTTP.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._list_logs_endpoint = _Endpoint(
            settings={
                "response_type": (LogsListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v1/logs-queries/list",
                "operation_id": "list_logs",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (LogsListRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._submit_log_endpoint = _Endpoint(
            settings={
                "response_type": (dict,),
                "auth": ["apiKeyAuth"],
                "endpoint_path": "/v1/input",
                "operation_id": "submit_log",
                "http_method": "POST",
                "version": "v1",
                "servers": [
                    {
                        "url": "https://{subdomain}.{site}",
                        "variables": {
                            "site": {
                                "description": "The regional site for Datadog customers.",
                                "default_value": "datadoghq.com",
                                "enum_values": [
                                    "datadoghq.com",
                                    "us3.datadoghq.com",
                                    "us5.datadoghq.com",
                                    "ap1.datadoghq.com",
                                    "datadoghq.eu",
                                    "ddog-gov.com",
                                ],
                            },
                            "subdomain": {
                                "description": "The subdomain where the API is deployed.",
                                "default_value": "http-intake.logs",
                            },
                        },
                    },
                    {
                        "url": "{protocol}://{name}",
                        "variables": {
                            "name": {
                                "description": "Full site DNS name.",
                                "default_value": "http-intake.logs.datadoghq.com",
                            },
                            "protocol": {
                                "description": "The protocol for accessing the API.",
                                "default_value": "https",
                            },
                        },
                    },
                    {
                        "url": "https://{subdomain}.{site}",
                        "variables": {
                            "site": {
                                "description": "Any Datadog deployment.",
                                "default_value": "datadoghq.com",
                            },
                            "subdomain": {
                                "description": "The subdomain where the API is deployed.",
                                "default_value": "http-intake.logs",
                            },
                        },
                    },
                ],
            },
            params_map={
                "content_encoding": {
                    "openapi_types": (ContentEncoding,),
                    "attribute": "Content-Encoding",
                    "location": "header",
                },
                "ddtags": {
                    "openapi_types": (str,),
                    "attribute": "ddtags",
                    "location": "query",
                },
                "body": {
                    "required": True,
                    "openapi_types": (HTTPLog,),
                    "location": "body",
                    "collection_format": "multi",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": ["application/json", "application/json;simple", "application/logplex-1", "text/plain"],
            },
            api_client=api_client,
        )

    def list_logs(
        self,
        body: LogsListRequest,
    ) -> LogsListResponse:
        """Search logs.

        List endpoint returns logs that match a log search query.
        `Results are paginated </logs/guide/collect-multiple-logs-with-pagination>`_.

        If you are considering archiving logs for your organization,
        consider use of the Datadog archive capabilities instead of the log list API.
        See `Datadog Logs Archive documentation <https://docs.datadoghq.com/logs/archives>`_.

        :param body: Logs filter
        :type body: LogsListRequest
        :rtype: LogsListResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._list_logs_endpoint.call_with_http_info(**kwargs)

    def submit_log(
        self,
        body: HTTPLog,
        *,
        content_encoding: Union[ContentEncoding, UnsetType] = unset,
        ddtags: Union[str, UnsetType] = unset,
    ) -> dict:
        """Send logs. **Deprecated**.

        Send your logs to your Datadog platform over HTTP. Limits per HTTP request are:

        * Maximum content size per payload (uncompressed): 5MB
        * Maximum size for a single log: 1MB
        * Maximum array size if sending multiple logs in an array: 1000 entries

        Any log exceeding 1MB is accepted and truncated by Datadog:

        * For a single log request, the API truncates the log at 1MB and returns a 2xx.
        * For a multi-logs request, the API processes all logs, truncates only logs larger than 1MB, and returns a 2xx.

        Datadog recommends sending your logs compressed.
        Add the ``Content-Encoding: gzip`` header to the request when sending compressed logs.

        The status codes answered by the HTTP API are:

        * 200: OK
        * 400: Bad request (likely an issue in the payload formatting)
        * 403: Permission issue (likely using an invalid API Key)
        * 413: Payload too large (batch is above 5MB uncompressed)
        * 5xx: Internal error, request should be retried after some time

        :param body: Log to send (JSON format).
        :type body: HTTPLog
        :param content_encoding: HTTP header used to compress the media-type.
        :type content_encoding: ContentEncoding, optional
        :param ddtags: Log tags can be passed as query parameters with ``text/plain`` content type.
        :type ddtags: str, optional
        :rtype: dict
        """
        kwargs: Dict[str, Any] = {}
        if content_encoding is not unset:
            kwargs["content_encoding"] = content_encoding

        if ddtags is not unset:
            kwargs["ddtags"] = ddtags

        kwargs["body"] = body

        warnings.warn("submit_log is deprecated", DeprecationWarning, stacklevel=2)
        return self._submit_log_endpoint.call_with_http_info(**kwargs)
