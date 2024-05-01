# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, Union

from datadog_api_client.api_client import ApiClient, Endpoint as _Endpoint
from datadog_api_client.configuration import Configuration
from datadog_api_client.model_utils import (
    UnsetType,
    unset,
)
from datadog_api_client.v1.model.event_list_response import EventListResponse
from datadog_api_client.v1.model.event_priority import EventPriority
from datadog_api_client.v1.model.event_create_response import EventCreateResponse
from datadog_api_client.v1.model.event_create_request import EventCreateRequest
from datadog_api_client.v1.model.event_response import EventResponse


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

        self._create_event_endpoint = _Endpoint(
            settings={
                "response_type": (EventCreateResponse,),
                "auth": ["apiKeyAuth"],
                "endpoint_path": "/api/v1/events",
                "operation_id": "create_event",
                "http_method": "POST",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "body": {
                    "required": True,
                    "openapi_types": (EventCreateRequest,),
                    "location": "body",
                },
            },
            headers_map={"accept": ["application/json"], "content_type": ["application/json"]},
            api_client=api_client,
        )

        self._get_event_endpoint = _Endpoint(
            settings={
                "response_type": (EventResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/events/{event_id}",
                "operation_id": "get_event",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "event_id": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "event_id",
                    "location": "path",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

        self._list_events_endpoint = _Endpoint(
            settings={
                "response_type": (EventListResponse,),
                "auth": ["apiKeyAuth", "appKeyAuth", "AuthZ"],
                "endpoint_path": "/api/v1/events",
                "operation_id": "list_events",
                "http_method": "GET",
                "version": "v1",
                "servers": None,
            },
            params_map={
                "start": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "start",
                    "location": "query",
                },
                "end": {
                    "required": True,
                    "openapi_types": (int,),
                    "attribute": "end",
                    "location": "query",
                },
                "priority": {
                    "openapi_types": (EventPriority,),
                    "attribute": "priority",
                    "location": "query",
                },
                "sources": {
                    "openapi_types": (str,),
                    "attribute": "sources",
                    "location": "query",
                },
                "tags": {
                    "openapi_types": (str,),
                    "attribute": "tags",
                    "location": "query",
                },
                "unaggregated": {
                    "openapi_types": (bool,),
                    "attribute": "unaggregated",
                    "location": "query",
                },
                "exclude_aggregate": {
                    "openapi_types": (bool,),
                    "attribute": "exclude_aggregate",
                    "location": "query",
                },
                "page": {
                    "validation": {
                        "inclusive_maximum": 2147483647,
                    },
                    "openapi_types": (int,),
                    "attribute": "page",
                    "location": "query",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

    def create_event(
        self,
        body: EventCreateRequest,
    ) -> EventCreateResponse:
        """Post an event.

        This endpoint allows you to post events to the stream.
        Tag them, set priority and event aggregate them with other events.

        :param body: Event request object
        :type body: EventCreateRequest
        :rtype: EventCreateResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["body"] = body

        return self._create_event_endpoint.call_with_http_info(**kwargs)

    def get_event(
        self,
        event_id: int,
    ) -> EventResponse:
        """Get an event.

        This endpoint allows you to query for event details.

        **Note** : If the event you’re querying contains markdown formatting of any kind,
        you may see characters such as ``%`` , ``\\`` , ``n`` in your output.

        :param event_id: The ID of the event.
        :type event_id: int
        :rtype: EventResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["event_id"] = event_id

        return self._get_event_endpoint.call_with_http_info(**kwargs)

    def list_events(
        self,
        start: int,
        end: int,
        *,
        priority: Union[EventPriority, UnsetType] = unset,
        sources: Union[str, UnsetType] = unset,
        tags: Union[str, UnsetType] = unset,
        unaggregated: Union[bool, UnsetType] = unset,
        exclude_aggregate: Union[bool, UnsetType] = unset,
        page: Union[int, UnsetType] = unset,
    ) -> EventListResponse:
        """Get a list of events.

        The event stream can be queried and filtered by time, priority, sources and tags.

        **Notes** :

        *
          If the event you’re querying contains markdown formatting of any kind,
          you may see characters such as ``%`` , ``\\`` , ``n`` in your output.

        *
          This endpoint returns a maximum of ``1000`` most recent results. To return additional results,
          identify the last timestamp of the last result and set that as the ``end`` query time to
          paginate the results. You can also use the page parameter to specify which set of ``1000`` results to return.

        :param start: POSIX timestamp.
        :type start: int
        :param end: POSIX timestamp.
        :type end: int
        :param priority: Priority of your events, either ``low`` or ``normal``.
        :type priority: EventPriority, optional
        :param sources: A comma separated string of sources.
        :type sources: str, optional
        :param tags: A comma separated list indicating what tags, if any, should be used to filter the list of events.
        :type tags: str, optional
        :param unaggregated: Set unaggregated to ``true`` to return all events within the specified [ ``start`` , ``end`` ] timeframe.
            Otherwise if an event is aggregated to a parent event with a timestamp outside of the timeframe,
            it won't be available in the output. Aggregated events with ``is_aggregate=true`` in the response will still be returned unless exclude_aggregate is set to ``true.``
        :type unaggregated: bool, optional
        :param exclude_aggregate: Set ``exclude_aggregate`` to ``true`` to only return unaggregated events where ``is_aggregate=false`` in the response. If the ``exclude_aggregate`` parameter is set to ``true`` ,
            then the unaggregated parameter is ignored and will be ``true`` by default.
        :type exclude_aggregate: bool, optional
        :param page: By default 1000 results are returned per request. Set page to the number of the page to return with ``0`` being the first page. The page parameter can only be used
            when either unaggregated or exclude_aggregate is set to ``true.``
        :type page: int, optional
        :rtype: EventListResponse
        """
        kwargs: Dict[str, Any] = {}
        kwargs["start"] = start

        kwargs["end"] = end

        if priority is not unset:
            kwargs["priority"] = priority

        if sources is not unset:
            kwargs["sources"] = sources

        if tags is not unset:
            kwargs["tags"] = tags

        if unaggregated is not unset:
            kwargs["unaggregated"] = unaggregated

        if exclude_aggregate is not unset:
            kwargs["exclude_aggregate"] = exclude_aggregate

        if page is not unset:
            kwargs["page"] = page

        return self._list_events_endpoint.call_with_http_info(**kwargs)
