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
from datadog_api_client.v2.model.ci_app_tests_analytics_aggregate_response import CIAppTestsAnalyticsAggregateResponse
from datadog_api_client.v2.model.ci_app_tests_aggregate_request import CIAppTestsAggregateRequest
from datadog_api_client.v2.model.ci_app_test_events_response import CIAppTestEventsResponse
from datadog_api_client.v2.model.ci_app_sort import CIAppSort
from datadog_api_client.v2.model.ci_app_test_event import CIAppTestEvent
from datadog_api_client.v2.model.ci_app_test_events_request import CIAppTestEventsRequest


class CIVisibilityTestsApi:
    """
    Search or aggregate your CI Visibility test events over HTTP.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient(Configuration())
        self.api_client = api_client

        self._aggregate_ci_app_test_events_endpoint = _Endpoint(
            settings={
                "response_type": (CIAppTestsAnalyticsAggregateResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/ci/tests/analytics/aggregate",
                "operation_id": "aggregate_ci_app_test_events",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (CIAppTestsAggregateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._list_ci_app_test_events_endpoint = _Endpoint(
            settings={
                "response_type": (CIAppTestEventsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/ci/tests/events",
                "operation_id": "list_ci_app_test_events",
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
                    "openapi_types": (CIAppSort,),
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

        self._search_ci_app_test_events_endpoint = _Endpoint(
            settings={
                "response_type": (CIAppTestEventsResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth"],
                "endpoint_path": "/api/v2/ci/tests/events/search",
                "operation_id": "search_ci_app_test_events",
                "http_method": "POST",
                "version": "v2",
                "servers": None,
            },
            params_map={
                "body": {
                    "openapi_types": (CIAppTestEventsRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

    def aggregate_ci_app_test_events(
        self,
        body: CIAppTestsAggregateRequest,
    ) -> CIAppTestsAnalyticsAggregateResponse:
        """Aggregate tests events.

        The API endpoint to aggregate CI Visibility test events into buckets of computed metrics and timeseries.

        :type body: CIAppTestsAggregateRequest
        :rtype: CIAppTestsAnalyticsAggregateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._aggregate_ci_app_test_events_endpoint.call_with_http_info(**kwargs)

    def list_ci_app_test_events(
        self,
        *,
        filter_query: Union[str, UnsetType] = unset,
        filter_from: Union[datetime, UnsetType] = unset,
        filter_to: Union[datetime, UnsetType] = unset,
        sort: Union[CIAppSort, UnsetType] = unset,
        page_cursor: Union[str, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
    ) -> CIAppTestEventsResponse:
        """Get a list of tests events.

        List endpoint returns CI Visibility test events that match a log search query.
        `Results are paginated similarly to logs <https://docs.datadoghq.com/logs/guide/collect-multiple-logs-with-pagination>`_.

        Use this endpoint to see your latest test events.

        :param filter_query: Search query following log syntax.
        :type filter_query: str, optional
        :param filter_from: Minimum timestamp for requested events.
        :type filter_from: datetime, optional
        :param filter_to: Maximum timestamp for requested events.
        :type filter_to: datetime, optional
        :param sort: Order of events in results.
        :type sort: CIAppSort, optional
        :param page_cursor: List following results with a cursor provided in the previous query.
        :type page_cursor: str, optional
        :param page_limit: Maximum number of events in the response.
        :type page_limit: int, optional
        :rtype: CIAppTestEventsResponse
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

        return self._list_ci_app_test_events_endpoint.call_with_http_info(**kwargs)

    def list_ci_app_test_events_with_pagination(
        self,
        *,
        filter_query: Union[str, UnsetType] = unset,
        filter_from: Union[datetime, UnsetType] = unset,
        filter_to: Union[datetime, UnsetType] = unset,
        sort: Union[CIAppSort, UnsetType] = unset,
        page_cursor: Union[str, UnsetType] = unset,
        page_limit: Union[int, UnsetType] = unset,
    ) -> collections.abc.Iterable[CIAppTestEvent]:
        """Get a list of tests events.

        Provide a paginated version of :meth:`list_ci_app_test_events`, returning all items.

        :param filter_query: Search query following log syntax.
        :type filter_query: str, optional
        :param filter_from: Minimum timestamp for requested events.
        :type filter_from: datetime, optional
        :param filter_to: Maximum timestamp for requested events.
        :type filter_to: datetime, optional
        :param sort: Order of events in results.
        :type sort: CIAppSort, optional
        :param page_cursor: List following results with a cursor provided in the previous query.
        :type page_cursor: str, optional
        :param page_limit: Maximum number of events in the response.
        :type page_limit: int, optional

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[CIAppTestEvent]
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
        endpoint = self._list_ci_app_test_events_endpoint
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

    def search_ci_app_test_events(
        self,
        *,
        body: Union[CIAppTestEventsRequest, UnsetType] = unset,
    ) -> CIAppTestEventsResponse:
        """Search tests events.

        List endpoint returns CI Visibility test events that match a log search query.
        `Results are paginated similarly to logs <https://docs.datadoghq.com/logs/guide/collect-multiple-logs-with-pagination>`_.

        Use this endpoint to build complex events filtering and search.

        :type body: CIAppTestEventsRequest, optional
        :rtype: CIAppTestEventsResponse
        """
        kwargs: Dict[str, Any] = {}
        if body is not unset:
            kwargs["body"] = body

        return self._search_ci_app_test_events_endpoint.call_with_http_info(**kwargs)

    def search_ci_app_test_events_with_pagination(
        self,
        *,
        body: Union[CIAppTestEventsRequest, UnsetType] = unset,
    ) -> collections.abc.Iterable[CIAppTestEvent]:
        """Search tests events.

        Provide a paginated version of :meth:`search_ci_app_test_events`, returning all items.

        :type body: CIAppTestEventsRequest, optional

        :return: A generator of paginated results.
        :rtype: collections.abc.Iterable[CIAppTestEvent]
        """
        kwargs: Dict[str, Any] = {}
        if body is not unset:
            kwargs["body"] = body

        local_page_size = get_attribute_from_path(kwargs, "body.page.limit", 10)
        endpoint = self._search_ci_app_test_events_endpoint
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
