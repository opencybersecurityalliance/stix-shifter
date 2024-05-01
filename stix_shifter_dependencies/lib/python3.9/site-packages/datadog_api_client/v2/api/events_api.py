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
from datadog_api_client.v2.model.events_list_response import EventsListResponse
from datadog_api_client.v2.model.events_sort import EventsSort
from datadog_api_client.v2.model.event_response import EventResponse
from datadog_api_client.v2.model.events_list_request import EventsListRequest


class EventsApi:
    """
    The events service allows you to programmatically post events to the event stream
    and fetch events from the event stream. Events are limited to 4000 characters.
    If an event is sent out with a message containing more than 4000 characters, only the
    first 4000 characters are displayed.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._list_events_endpoint = _Endpoint(
            settings={
                "response_type": (EventsListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/events",
                "operation_id": "list_events",
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
                "filter_from": {
                    "openapi_types": (str,),
                    "attribute": "filter[from]",
                    "location": "query",
                },
                "filter_to": {
                    "openapi_types": (str,),
                    "attribute": "filter[to]",
                    "location": "query",
                },
                "sort": {
                    "openapi_types": (EventsSort,),
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

        self._search_events_endpoint = _Endpoint(
            settings={
                "response_type": (EventsListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/events/search",
                "operation_id": "search_events",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "openapi_types": (EventsListRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def list_events(
        self,
        *,
        filter_query: Union[str, UnsetType] = unset,
        filter_from: Union[str, UnsetType] = unset,
        filter_to: Union[str, UnsetType] = unset,
        sort: Union[EventsSort, UnsetType] = unset,
        page_cursor: Union[str, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
    ) -> EventsListResponse:
        """Get a list of events.

        List endpoint returns events that match an events search query.
        `Results are paginated similarly to logs <https://docs.datadoghq.com/logs/guide/collect-multiple-logs-with-pagination>`_.

        Use this endpoint to see your latest events.

        :param filter_query: Search query following events syntax.
        :type filter_query: str, optional
        :param filter_from: Minimum timestamp for requested events.
        :type filter_from: str, optional
        :param filter_to: Maximum timestamp for requested events.
        :type filter_to: str, optional
        :param sort: Order of events in results.
        :type sort: EventsSort, optional
        :param page_cursor: List following results with a cursor provided in the previous query.
        :type page_cursor: str, optional
        :param page_limit: Maximum number of events in the response.
        :type page_limit: int, optional
        :rtype: EventsListResponse
        """
        kwargs: Dict[str, Any] = {}
        if filter_query is not unset:
            kwargs["filter_query"] = filter_query

        if filter_from is not unset:
            kwargs["filter_from"] = filter_from

        if filter_to is not unset:
            kwargs["filter_to"] = filter_to

        if sort is not unset:
            kwargs["sort"] = sort

        if page_cursor is not unset:
            kwargs["page_cursor"] = page_cursor

        if page_limit is not unset:
            kwargs["page_limit"] = page_limit

        return self._list_events_endpoint.call_with_http_info(**kwargs)

    def list_events_with_pagination(
        self,
        *,
        filter_query: Union[str, UnsetType] = unset,
        filter_from: Union[str, UnsetType] = unset,
        filter_to: Union[str, UnsetType] = unset,
        sort: Union[EventsSort, UnsetType] = unset,
        page_cursor: Union[str, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
    ) -> collections.abc.Iterable[EventResponse]:
        """Get a list of events.

        Provide a paginated version of :meth:`list_events`, returning all items.

        :param filter_query: Search query following events syntax.
        :type filter_query: str, optional
        :param filter_from: Minimum timestamp for requested events.
        :type filter_from: str, optional
        :param filter_to: Maximum timestamp for requested events.
        :type filter_to: str, optional
        :param sort: Order of events in results.
        :type sort: EventsSort, optional
        :param page_cursor: List following results with a cursor provided in the previous query.
        :type page_cursor: str, optional
        :param page_limit: Maximum number of events in the response.
        :type page_limit: int, optional

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[EventResponse]
        """
        kwargs: Dict[str, Any] = {}
        if filter_query is not unset:
            kwargs["filter_query"] = filter_query

        if filter_from is not unset:
            kwargs["filter_from"] = filter_from

        if filter_to is not unset:
            kwargs["filter_to"] = filter_to

        if sort is not unset:
            kwargs["sort"] = sort

        if page_cursor is not unset:
            kwargs["page_cursor"] = page_cursor

        if page_limit is not unset:
            kwargs["page_limit"] = page_limit

        local_page_size = get_attribute_from_path(kwargs, "page_limit", 10)
        endpoint = self._list_events_endpoint
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

    def search_events(
        self,
        *,
        body: Union[EventsListRequest, UnsetType] = unset,
    ) -> EventsListResponse:
        """Search events.

        List endpoint returns events that match an events search query.
        `Results are paginated similarly to logs <https://docs.datadoghq.com/logs/guide/collect-multiple-logs-with-pagination>`_.

        Use this endpoint to build complex events filtering and search.

        :type body: EventsListRequest, optional
        :rtype: EventsListResponse
        """
        kwargs: Dict[str, Any] = {}
        if body is not unset:
            kwargs["body"] = body

        return self._search_events_endpoint.call_with_http_info(**kwargs)

    def search_events_with_pagination(
        self,
        *,
        body: Union[EventsListRequest, UnsetType] = unset,
    ) -> collections.abc.Iterable[EventResponse]:
        """Search events.

        Provide a paginated version of :meth:`search_events`, returning all items.

        :type body: EventsListRequest, optional

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[EventResponse]
        """
        kwargs: Dict[str, Any] = {}
        if body is not unset:
            kwargs["body"] = body

        local_page_size = get_attribute_from_path(kwargs, "body.page.limit", 10)
        endpoint = self._search_events_endpoint
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
