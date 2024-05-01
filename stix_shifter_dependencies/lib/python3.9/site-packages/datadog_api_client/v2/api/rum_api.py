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
from datadog_api_client.v2.model.rum_analytics_aggregate_response import RUMAnalyticsAggregateResponse
from datadog_api_client.v2.model.rum_aggregate_request import RUMAggregateRequest
from datadog_api_client.v2.model.rum_applications_response import RUMApplicationsResponse
from datadog_api_client.v2.model.rum_application_response import RUMApplicationResponse
from datadog_api_client.v2.model.rum_application_create_request import RUMApplicationCreateRequest
from datadog_api_client.v2.model.rum_application_update_request import RUMApplicationUpdateRequest
from datadog_api_client.v2.model.rum_events_response import RUMEventsResponse
from datadog_api_client.v2.model.rum_sort import RUMSort
from datadog_api_client.v2.model.rum_event import RUMEvent
from datadog_api_client.v2.model.rum_search_events_request import RUMSearchEventsRequest


class RUMApi:
    """
    Search or aggregate your RUM events over HTTP.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._aggregate_rum_events_endpoint = _Endpoint(
            settings={
                "response_type": (RUMAnalyticsAggregateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/rum/analytics/aggregate",
                "operation_id": "aggregate_rum_events",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (RUMAggregateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._create_rum_application_endpoint = _Endpoint(
            settings={
                "response_type": (RUMApplicationResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/rum/applications",
                "operation_id": "create_rum_application",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (RUMApplicationCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._delete_rum_application_endpoint = _Endpoint(
            settings={
                "response_type": None,
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/rum/applications/{id}",
                "operation_id": "delete_rum_application",
                "http_method": "DELETE",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["*/*"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_rum_application_endpoint = _Endpoint(
            settings={
                "response_type": (RUMApplicationResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/rum/applications/{id}",
                "operation_id": "get_rum_application",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._get_rum_applications_endpoint = _Endpoint(
            settings={
                "response_type": (RUMApplicationsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/rum/applications",
                "operation_id": "get_rum_applications",
                "http_method": "GET",
                "version": "v2",
                "servers": None,
            },
            params_map={},
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_rum_events_endpoint = _Endpoint(
            settings={
                "response_type": (RUMEventsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/rum/events",
                "operation_id": "list_rum_events",
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
                    "openapi_types": (datetime,),
                    "attribute": "filter[from]",
                    "location": "query",
                },
                "filter_to": {
                    "openapi_types": (datetime,),
                    "attribute": "filter[to]",
                    "location": "query",
                },
                "sort": {
                    "openapi_types": (RUMSort,),
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

        self._search_rum_events_endpoint = _Endpoint(
            settings={
                "response_type": (RUMEventsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v2/rum/events/search",
                "operation_id": "search_rum_events",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (RUMSearchEventsRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._update_rum_application_endpoint = _Endpoint(
            settings={
                "response_type": (RUMApplicationResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/rum/applications/{id}",
                "operation_id": "update_rum_application",
                "http_method": "PATCH",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "id": {
                    "required": True,
                    "openapi_types": (str,),
                    "attribute": "id",
                    "location": "path",
                },
                "body": {
                    "required": True,
                    "openapi_types": (RUMApplicationUpdateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def aggregate_rum_events(
        self,
        body: RUMAggregateRequest,
    ) -> RUMAnalyticsAggregateResponse:
        """Aggregate RUM events.

        The API endpoint to aggregate RUM events into buckets of computed metrics and timeseries.

        :type body: RUMAggregateRequest
        :rtype: RUMAnalyticsAggregateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._aggregate_rum_events_endpoint.call_with_http_info(**kwargs)

    def create_rum_application(
        self,
        body: RUMApplicationCreateRequest,
    ) -> RUMApplicationResponse:
        """Create a new RUM application.

        Create a new RUM application in your organization.

        :type body: RUMApplicationCreateRequest
        :rtype: RUMApplicationResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_rum_application_endpoint.call_with_http_info(**kwargs)

    def delete_rum_application(
        self,
        id: str,
    ) -> None:
        """Delete a RUM application.

        Delete an existing RUM application in your organization.

        :param id: RUM application ID.
        :type id: str
        :rtype: None
        """
        kwargs: Dict[str, Any] = {}
        kwargs["id"] = id

        return self._delete_rum_application_endpoint.call_with_http_info(**kwargs)

    def get_rum_application(
        self,
        id: str,
    ) -> RUMApplicationResponse:
        """Get a RUM application.

        Get the RUM application with given ID in your organization.

        :param id: RUM application ID.
        :type id: str
        :rtype: RUMApplicationResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["id"] = id

        return self._get_rum_application_endpoint.call_with_http_info(**kwargs)

    def get_rum_applications(
        self,
    ) -> RUMApplicationsResponse:
        """List all the RUM applications.

        List all the RUM applications in your organization.

        :rtype: RUMApplicationsResponse
        """
        kwargs: Dict[str, Any] = {}
        return self._get_rum_applications_endpoint.call_with_http_info(**kwargs)

    def list_rum_events(
        self,
        *,
        filter_query: Union[str, UnsetType] = unset,
        filter_from: Union[datetime, UnsetType] = unset,
        filter_to: Union[datetime, UnsetType] = unset,
        sort: Union[RUMSort, UnsetType] = unset,
        page_cursor: Union[str, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
    ) -> RUMEventsResponse:
        """Get a list of RUM events.

        List endpoint returns events that match a RUM search query.
        `Results are paginated <https://docs.datadoghq.com/logs/guide/collect-multiple-logs-with-pagination>`_.

        Use this endpoint to see your latest RUM events.

        :param filter_query: Search query following RUM syntax.
        :type filter_query: str, optional
        :param filter_from: Minimum timestamp for requested events.
        :type filter_from: datetime, optional
        :param filter_to: Maximum timestamp for requested events.
        :type filter_to: datetime, optional
        :param sort: Order of events in results.
        :type sort: RUMSort, optional
        :param page_cursor: List following results with a cursor provided in the previous query.
        :type page_cursor: str, optional
        :param page_limit: Maximum number of events in the response.
        :type page_limit: int, optional
        :rtype: RUMEventsResponse
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

        return self._list_rum_events_endpoint.call_with_http_info(**kwargs)

    def list_rum_events_with_pagination(
        self,
        *,
        filter_query: Union[str, UnsetType] = unset,
        filter_from: Union[datetime, UnsetType] = unset,
        filter_to: Union[datetime, UnsetType] = unset,
        sort: Union[RUMSort, UnsetType] = unset,
        page_cursor: Union[str, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
    ) -> collections.abc.Iterable[RUMEvent]:
        """Get a list of RUM events.

        Provide a paginated version of :meth:`list_rum_events`, returning all items.

        :param filter_query: Search query following RUM syntax.
        :type filter_query: str, optional
        :param filter_from: Minimum timestamp for requested events.
        :type filter_from: datetime, optional
        :param filter_to: Maximum timestamp for requested events.
        :type filter_to: datetime, optional
        :param sort: Order of events in results.
        :type sort: RUMSort, optional
        :param page_cursor: List following results with a cursor provided in the previous query.
        :type page_cursor: str, optional
        :param page_limit: Maximum number of events in the response.
        :type page_limit: int, optional

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[RUMEvent]
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
        endpoint = self._list_rum_events_endpoint
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

    def search_rum_events(
        self,
        body: RUMSearchEventsRequest,
    ) -> RUMEventsResponse:
        """Search RUM events.

        List endpoint returns RUM events that match a RUM search query.
        `Results are paginated <https://docs.datadoghq.com/logs/guide/collect-multiple-logs-with-pagination>`_.

        Use this endpoint to build complex RUM events filtering and search.

        :type body: RUMSearchEventsRequest
        :rtype: RUMEventsResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._search_rum_events_endpoint.call_with_http_info(**kwargs)

    def search_rum_events_with_pagination(
        self,
        body: RUMSearchEventsRequest,
    ) -> collections.abc.Iterable[RUMEvent]:
        """Search RUM events.

        Provide a paginated version of :meth:`search_rum_events`, returning all items.

        :type body: RUMSearchEventsRequest

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[RUMEvent]
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        local_page_size = get_attribute_from_path(kwargs, "body.page.limit", 10)
        endpoint = self._search_rum_events_endpoint
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

    def update_rum_application(
        self,
        id: str,
        body: RUMApplicationUpdateRequest,
    ) -> RUMApplicationResponse:
        """Update a RUM application.

        Update the RUM application with given ID in your organization.

        :param id: RUM application ID.
        :type id: str
        :type body: RUMApplicationUpdateRequest
        :rtype: RUMApplicationResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["id"] = id

        kwargs["body"] = body

        return self._update_rum_application_endpoint.call_with_http_info(**kwargs)
