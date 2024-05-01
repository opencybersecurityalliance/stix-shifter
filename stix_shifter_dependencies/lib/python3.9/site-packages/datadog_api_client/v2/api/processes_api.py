# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

import collections
from typing import Any, Dict, Union

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    set_attribute_from_path,
    get_attribute_from_path,
    UnsetType,
    unset,
)
from datadog_api_client.v2.model.process_summaries_response import ProcessSummariesResponse
from datadog_api_client.v2.model.process_summary import ProcessSummary


class ProcessesApi:
    """
    The processes API allows you to query processes data for your organization.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._list_processes_endpoint = _Endpoint(
            settings={
                "response_type": (ProcessSummariesResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/processes",
                "operation_id": "list_processes",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "search": {
                    "openapi_types": (str,),
                    "attribute": "search",
                    "location": "query",
                },
                "tags": {
                    "openapi_types": (str,),
                    "attribute": "tags",
                    "location": "query",
                },
                "_from": {
                    "openapi_types": (int,),
                    "attribute": "from",
                    "location": "query",
                },
                "to": {
                    "openapi_types": (int,),
                    "attribute": "to",
                    "location": "query",
                },
                "page_limit": {
                    "validation": {
                        "inclusive_maximum": 10000,
                        "inclusive_minimum": 1,
                    },
                    "openapi_types": (int,),
                    "attribute": "page[limit]",
                    "location": "query",
                },
                "page_cursor": {
                    "openapi_types": (str,),
                    "attribute": "page[cursor]",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

    def list_processes(
        self,
        *,
        search: Union[str, UnsetType] = unset,
        tags: Union[str, UnsetType] = unset,
        _from: Union[int, UnsetType] = unset,
        to: Union[int, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
        page_cursor: Union[str, UnsetType] = unset,
    ) -> ProcessSummariesResponse:
        """Get all processes.

        Get all processes for your organization.

        :param search: String to search processes by.
        :type search: str, optional
        :param tags: Comma-separated list of tags to filter processes by.
        :type tags: str, optional
        :param _from: Unix timestamp (number of seconds since epoch) of the start of the query window.
            If not provided, the start of the query window will be 15 minutes before the ``to`` timestamp. If neither
            ``from`` nor ``to`` are provided, the query window will be ``[now - 15m, now]``.
        :type _from: int, optional
        :param to: Unix timestamp (number of seconds since epoch) of the end of the query window.
            If not provided, the end of the query window will be 15 minutes after the ``from`` timestamp. If neither
            ``from`` nor ``to`` are provided, the query window will be ``[now - 15m, now]``.
        :type to: int, optional
        :param page_limit: Maximum number of results returned.
        :type page_limit: int, optional
        :param page_cursor: String to query the next page of results.
            This key is provided with each valid response from the API in ``meta.page.after``.
        :type page_cursor: str, optional
        :rtype: ProcessSummariesResponse
        """
        kwargs: Dict[str, Any] = {}
        if search is not unset:
            kwargs["search"] = search

        if tags is not unset:
            kwargs["tags"] = tags

        if _from is not unset:
            kwargs["_from"] = _from

        if to is not unset:
            kwargs["to"] = to

        if page_limit is not unset:
            kwargs["page_limit"] = page_limit

        if page_cursor is not unset:
            kwargs["page_cursor"] = page_cursor

        return self._list_processes_endpoint.call_with_http_info(**kwargs)

    def list_processes_with_pagination(
        self,
        *,
        search: Union[str, UnsetType] = unset,
        tags: Union[str, UnsetType] = unset,
        _from: Union[int, UnsetType] = unset,
        to: Union[int, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
        page_cursor: Union[str, UnsetType] = unset,
    ) -> collections.abc.Iterable[ProcessSummary]:
        """Get all processes.

        Provide a paginated version of :meth:`list_processes`, returning all items.

        :param search: String to search processes by.
        :type search: str, optional
        :param tags: Comma-separated list of tags to filter processes by.
        :type tags: str, optional
        :param _from: Unix timestamp (number of seconds since epoch) of the start of the query window.
            If not provided, the start of the query window will be 15 minutes before the ``to`` timestamp. If neither
            ``from`` nor ``to`` are provided, the query window will be ``[now - 15m, now]``.
        :type _from: int, optional
        :param to: Unix timestamp (number of seconds since epoch) of the end of the query window.
            If not provided, the end of the query window will be 15 minutes after the ``from`` timestamp. If neither
            ``from`` nor ``to`` are provided, the query window will be ``[now - 15m, now]``.
        :type to: int, optional
        :param page_limit: Maximum number of results returned.
        :type page_limit: int, optional
        :param page_cursor: String to query the next page of results.
            This key is provided with each valid response from the API in ``meta.page.after``.
        :type page_cursor: str, optional

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[ProcessSummary]
        """
        kwargs: Dict[str, Any] = {}
        if search is not unset:
            kwargs["search"] = search

        if tags is not unset:
            kwargs["tags"] = tags

        if _from is not unset:
            kwargs["_from"] = _from

        if to is not unset:
            kwargs["to"] = to

        if page_limit is not unset:
            kwargs["page_limit"] = page_limit

        if page_cursor is not unset:
            kwargs["page_cursor"] = page_cursor

        local_page_size = get_attribute_from_path(kwargs, "page_limit", 1000)
        endpoint = self._list_processes_endpoint
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
