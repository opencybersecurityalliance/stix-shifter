# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

import collections
from typing import Any, Dict, Union

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    datetime,
    set_attribute_from_path,
    get_attribute_from_path,
    UnsetType,
    unset,
)
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.logs_aggregate_response import LogsAggregateResponse
from datadog_api_client.v2.model.logs_aggregate_request import LogsAggregateRequest
from datadog_api_client.v2.model.logs_list_response import LogsListResponse
from datadog_api_client.v2.model.logs_storage_tier import LogsStorageTier
from datadog_api_client.v2.model.logs_sort import LogsSort
from datadog_api_client.v2.model.log import Log
from datadog_api_client.v2.model.logs_list_request import LogsListRequest


class LogsApi:
    """
    Search your logs and send them to your Datadog platform over HTTP.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._aggregate_logs_endpoint = _Endpoint(
            settings={
                "response_type": (LogsAggregateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/logs/analytics/aggregate",
                "operation_id": "aggregate_logs",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (LogsAggregateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._list_logs_endpoint = _Endpoint(
            settings={
                "response_type": (LogsListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/logs/events/search",
                "operation_id": "list_logs",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "openapi_types": (LogsListRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._list_logs_get_endpoint = _Endpoint(
            settings={
                "response_type": (LogsListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/logs/events",
                "operation_id": "list_logs_get",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "filter_query": {
                    "openapi_types": (str,),
                    "attribute": "filter[query]",
                    "location": "query",
                },
                "filter_index": {
                    "openapi_types": (str,),
                    "attribute": "filter[index]",
                    "location": "query",
                },
                "filter_from": {
                    "openapi_types": (datetime,),
                    "attribute": "filter[from]",
                    "location": "query",
                },
                "filter_to": {
                    "openapi_types": (datetime,),
                    "attribute": "filter[to]",
                    "location": "query",
                },
                "filter_storage_tier": {
                    "openapi_types": (LogsStorageTier,),
                    "attribute": "filter[storage_tier]",
                    "location": "query",
                },
                "sort": {
                    "openapi_types": (LogsSort,),
                    "attribute": "sort",
                    "location": "query",
                },
                "page_cursor": {
                    "openapi_types": (str,),
                    "attribute": "page[cursor]",
                    "location": "query",
                },
                "page_limit": {
                    "validation": {
                        "inclusive_maximum": 1000,
                    },
                    "openapi_types": (int,),
                    "attribute": "page[limit]",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._submit_log_endpoint = _Endpoint(
            settings={
                "response_type": (dict,),
                "auth": ["apiKeyAuth"],
                "endpoint_path": "/api/v2/logs",
                "operation_id": "submit_log",
                "http_method": "POST",
                "version": "v2",
                "servers": [
                    {
                        "url": "https://{subdomain}.{site}",
                        "variables": {
                            "site": {
                                "description": "The regional site for customers.",
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
                "content_type": ["application/json", "application/logplex-1", "text/plain"],
            },
            api_client=api_client,
        )

    def aggregate_logs(
        self,
        body: LogsAggregateRequest,
    ) -> LogsAggregateResponse:
        """Aggregate events.

        The API endpoint to aggregate events into buckets and compute metrics and timeseries.

        :type body: LogsAggregateRequest
        :rtype: LogsAggregateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._aggregate_logs_endpoint.call_with_http_info(**kwargs)

    def list_logs(
        self,
        *,
        body: Union[LogsListRequest, UnsetType] = unset,
    ) -> LogsListResponse:
        """Search logs.

        List endpoint returns logs that match a log search query.
        `Results are paginated </logs/guide/collect-multiple-logs-with-pagination>`_.

        Use this endpoint to build complex logs filtering and search.

        If you are considering archiving logs for your organization,
        consider use of the Datadog archive capabilities instead of the log list API.
        See `Datadog Logs Archive documentation <https://docs.datadoghq.com/logs/archives>`_.

        :type body: LogsListRequest, optional
        :rtype: LogsListResponse
        """
        kwargs: Dict[str, Any] = {}
        if body is not unset:
            kwargs["body"] = body

        return self._list_logs_endpoint.call_with_http_info(**kwargs)

    def list_logs_with_pagination(
        self,
        *,
        body: Union[LogsListRequest, UnsetType] = unset,
    ) -> collections.abc.Iterable[Log]:
        """Search logs.

        Provide a paginated version of :meth:`list_logs`, returning all items.

        :type body: LogsListRequest, optional

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[Log]
        """
        kwargs: Dict[str, Any] = {}
        if body is not unset:
            kwargs["body"] = body

        local_page_size = get_attribute_from_path(kwargs, "body.page.limit", 10)
        endpoint = self._list_logs_endpoint
        set_attribute_from_path(kwargs, "body.page.limit", local_page_size, endpoint.params_map)
        while True:
            response = endpoint.call_with_http_info(**kwargs)
            for item in get_attribute_from_path(response, "data"):
                yield item
            if len(get_attribute_from_path(response, "data")) < local_page_size:
                break
            set_attribute_from_path(
                kwargs, "body.page.cursor", get_attribute_from_path(response, "meta.page.after"), endpoint.params_map
            )

    def list_logs_get(
        self,
        *,
        filter_query: Union[str, UnsetType] = unset,
        filter_index: Union[str, UnsetType] = unset,
        filter_from: Union[datetime, UnsetType] = unset,
        filter_to: Union[datetime, UnsetType] = unset,
        filter_storage_tier: Union[LogsStorageTier, UnsetType] = unset,
        sort: Union[LogsSort, UnsetType] = unset,
        page_cursor: Union[str, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
    ) -> LogsListResponse:
        """Get a list of logs.

        List endpoint returns logs that match a log search query.
        `Results are paginated </logs/guide/collect-multiple-logs-with-pagination>`_.

        Use this endpoint to see your latest logs.

        If you are considering archiving logs for your organization,
        consider use of the Datadog archive capabilities instead of the log list API.
        See `Datadog Logs Archive documentation <https://docs.datadoghq.com/logs/archives>`_.

        :param filter_query: Search query following logs syntax.
        :type filter_query: str, optional
        :param filter_index: For customers with multiple indexes, the indexes to search
            Defaults to '*' which means all indexes
        :type filter_index: str, optional
        :param filter_from: Minimum timestamp for requested logs.
        :type filter_from: datetime, optional
        :param filter_to: Maximum timestamp for requested logs.
        :type filter_to: datetime, optional
        :param filter_storage_tier: Specifies the storage type to be used
        :type filter_storage_tier: LogsStorageTier, optional
        :param sort: Order of logs in results.
        :type sort: LogsSort, optional
        :param page_cursor: List following results with a cursor provided in the previous query.
        :type page_cursor: str, optional
        :param page_limit: Maximum number of logs in the response.
        :type page_limit: int, optional
        :rtype: LogsListResponse
        """
        kwargs: Dict[str, Any] = {}
        if filter_query is not unset:
            kwargs["filter_query"] = filter_query

        if filter_index is not unset:
            kwargs["filter_index"] = filter_index

        if filter_from is not unset:
            kwargs["filter_from"] = filter_from

        if filter_to is not unset:
            kwargs["filter_to"] = filter_to

        if filter_storage_tier is not unset:
            kwargs["filter_storage_tier"] = filter_storage_tier

        if sort is not unset:
            kwargs["sort"] = sort

        if page_cursor is not unset:
            kwargs["page_cursor"] = page_cursor

        if page_limit is not unset:
            kwargs["page_limit"] = page_limit

        return self._list_logs_get_endpoint.call_with_http_info(**kwargs)

    def list_logs_get_with_pagination(
        self,
        *,
        filter_query: Union[str, UnsetType] = unset,
        filter_index: Union[str, UnsetType] = unset,
        filter_from: Union[datetime, UnsetType] = unset,
        filter_to: Union[datetime, UnsetType] = unset,
        filter_storage_tier: Union[LogsStorageTier, UnsetType] = unset,
        sort: Union[LogsSort, UnsetType] = unset,
        page_cursor: Union[str, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
    ) -> collections.abc.Iterable[Log]:
        """Get a list of logs.

        Provide a paginated version of :meth:`list_logs_get`, returning all items.

        :param filter_query: Search query following logs syntax.
        :type filter_query: str, optional
        :param filter_index: For customers with multiple indexes, the indexes to search
            Defaults to '*' which means all indexes
        :type filter_index: str, optional
        :param filter_from: Minimum timestamp for requested logs.
        :type filter_from: datetime, optional
        :param filter_to: Maximum timestamp for requested logs.
        :type filter_to: datetime, optional
        :param filter_storage_tier: Specifies the storage type to be used
        :type filter_storage_tier: LogsStorageTier, optional
        :param sort: Order of logs in results.
        :type sort: LogsSort, optional
        :param page_cursor: List following results with a cursor provided in the previous query.
        :type page_cursor: str, optional
        :param page_limit: Maximum number of logs in the response.
        :type page_limit: int, optional

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[Log]
        """
        kwargs: Dict[str, Any] = {}
        if filter_query is not unset:
            kwargs["filter_query"] = filter_query

        if filter_index is not unset:
            kwargs["filter_index"] = filter_index

        if filter_from is not unset:
            kwargs["filter_from"] = filter_from

        if filter_to is not unset:
            kwargs["filter_to"] = filter_to

        if filter_storage_tier is not unset:
            kwargs["filter_storage_tier"] = filter_storage_tier

        if sort is not unset:
            kwargs["sort"] = sort

        if page_cursor is not unset:
            kwargs["page_cursor"] = page_cursor

        if page_limit is not unset:
            kwargs["page_limit"] = page_limit

        local_page_size = get_attribute_from_path(kwargs, "page_limit", 10)
        endpoint = self._list_logs_get_endpoint
        set_attribute_from_path(kwargs, "page_limit", local_page_size, endpoint.params_map)
        while True:
            response = endpoint.call_with_http_info(**kwargs)
            for item in get_attribute_from_path(response, "data"):
                yield item
            if len(get_attribute_from_path(response, "data")) < local_page_size:
                break
            set_attribute_from_path(
                kwargs, "page_cursor", get_attribute_from_path(response, "meta.page.after"), endpoint.params_map
            )

    def submit_log(
        self,
        body: HTTPLog,
        *,
        content_encoding: Union[ContentEncoding, UnsetType] = unset,
        ddtags: Union[str, UnsetType] = unset,
    ) -> dict:
        """Send logs.

        Send your logs to your Datadog platform over HTTP. Limits per HTTP request are:

        * Maximum content size per payload (uncompressed): 5MB
        * Maximum size for a single log: 1MB
        * Maximum array size if sending multiple logs in an array: 1000 entries

        Any log exceeding 1MB is accepted and truncated by Datadog:

        * For a single log request, the API truncates the log at 1MB and returns a 2xx.
        * For a multi-logs request, the API processes all logs, truncates only logs larger than 1MB, and returns a 2xx.

        Datadog recommends sending your logs compressed.
        Add the ``Content-Encoding: gzip`` header to the request when sending compressed logs.
        Log events can be submitted up to 18 hours in the past and 2 hours in the future.

        The status codes answered by the HTTP API are:

        * 202: Accepted: the request has been accepted for processing
        * 400: Bad request (likely an issue in the payload formatting)
        * 401: Unauthorized (likely a missing API Key)
        * 403: Permission issue (likely using an invalid API Key)
        * 408: Request Timeout, request should be retried after some time
        * 413: Payload too large (batch is above 5MB uncompressed)
        * 429: Too Many Requests, request should be retried after some time
        * 500: Internal Server Error, the server encountered an unexpected condition that prevented it from fulfilling the request, request should be retried after some time
        * 503: Service Unavailable, the server is not ready to handle the request probably because it is overloaded, request should be retried after some time

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

        return self._submit_log_endpoint.call_with_http_info(**kwargs)
