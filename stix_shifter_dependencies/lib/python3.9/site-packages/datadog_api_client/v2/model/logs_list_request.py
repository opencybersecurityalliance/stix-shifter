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
    from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
    from datadog_api_client.v2.model.logs_query_options import LogsQueryOptions
    from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
    from datadog_api_client.v2.model.logs_sort import LogsSort


class LogsListRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
        from datadog_api_client.v2.model.logs_query_options import LogsQueryOptions
        from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
        from datadog_api_client.v2.model.logs_sort import LogsSort

        return {
            "filter": (LogsQueryFilter,),
            "options": (LogsQueryOptions,),
            "page": (LogsListRequestPage,),
            "sort": (LogsSort,),
        }

    attribute_map = {
        "filter": "filter",
        "options": "options",
        "page": "page",
        "sort": "sort",
    }

    def __init__(
        self_,
        filter: Union[LogsQueryFilter, UnsetType] = unset,
        options: Union[LogsQueryOptions, UnsetType] = unset,
        page: Union[LogsListRequestPage, UnsetType] = unset,
        sort: Union[LogsSort, UnsetType] = unset,
        **kwargs,
    ):
        """
        The request for a logs list.

        :param filter: The search and filter query settings
        :type filter: LogsQueryFilter, optional

        :param options: Global query options that are used during the query.
            Note: You should only supply timezone or time offset but not both otherwise the query will fail.
        :type options: LogsQueryOptions, optional

        :param page: Paging attributes for listing logs.
        :type page: LogsListRequestPage, optional

        :param sort: Sort parameters when querying logs.
        :type sort: LogsSort, optional
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
