# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.events_query_filter import EventsQueryFilter
    from datadog_api_client.v2.model.events_query_options import EventsQueryOptions
    from datadog_api_client.v2.model.events_request_page import EventsRequestPage
    from datadog_api_client.v2.model.events_sort import EventsSort


class EventsListRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.events_query_filter import EventsQueryFilter
        from datadog_api_client.v2.model.events_query_options import EventsQueryOptions
        from datadog_api_client.v2.model.events_request_page import EventsRequestPage
        from datadog_api_client.v2.model.events_sort import EventsSort

        return {
            "filter": (EventsQueryFilter,),
            "options": (EventsQueryOptions,),
            "page": (EventsRequestPage,),
            "sort": (EventsSort,),
        }

    attribute_map = {
        "filter": "filter",
        "options": "options",
        "page": "page",
        "sort": "sort",
    }

    def __init__(
        self_,
        filter: Union[EventsQueryFilter, UnsetType] = unset,
        options: Union[EventsQueryOptions, UnsetType] = unset,
        page: Union[EventsRequestPage, UnsetType] = unset,
        sort: Union[EventsSort, UnsetType] = unset,
        **kwargs,
    ):
        """
        The object sent with the request to retrieve a list of events from your organization.

        :param filter: The search and filter query settings.
        :type filter: EventsQueryFilter, optional

        :param options: The global query options that are used. Either provide a timezone or a time offset but not both,
            otherwise the query fails.
        :type options: EventsQueryOptions, optional

        :param page: Pagination settings.
        :type page: EventsRequestPage, optional

        :param sort: The sort parameters when querying events.
        :type sort: EventsSort, optional
        """
        if filter is not unset:
            kwargs["filter"] = filter
        if options is not unset:
            kwargs["options"] = options
        if page is not unset:
            kwargs["page"] = page
        if sort is not unset:
            kwargs["sort"] = sort
        super().__init__(kwargs)
