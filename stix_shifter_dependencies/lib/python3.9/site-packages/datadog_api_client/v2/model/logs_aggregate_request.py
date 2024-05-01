# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.logs_compute import LogsCompute
    from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
    from datadog_api_client.v2.model.logs_group_by import LogsGroupBy
    from datadog_api_client.v2.model.logs_query_options import LogsQueryOptions
    from datadog_api_client.v2.model.logs_aggregate_request_page import LogsAggregateRequestPage


class LogsAggregateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.logs_compute import LogsCompute
        from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
        from datadog_api_client.v2.model.logs_group_by import LogsGroupBy
        from datadog_api_client.v2.model.logs_query_options import LogsQueryOptions
        from datadog_api_client.v2.model.logs_aggregate_request_page import LogsAggregateRequestPage

        return {
            "compute": ([LogsCompute],),
            "filter": (LogsQueryFilter,),
            "group_by": ([LogsGroupBy],),
            "options": (LogsQueryOptions,),
            "page": (LogsAggregateRequestPage,),
        }

    attribute_map = {
        "compute": "compute",
        "filter": "filter",
        "group_by": "group_by",
        "options": "options",
        "page": "page",
    }

    def __init__(
        self_,
        compute: Union[List[LogsCompute], UnsetType] = unset,
        filter: Union[LogsQueryFilter, UnsetType] = unset,
        group_by: Union[List[LogsGroupBy], UnsetType] = unset,
        options: Union[LogsQueryOptions, UnsetType] = unset,
        page: Union[LogsAggregateRequestPage, UnsetType] = unset,
        **kwargs,
    ):
        """
        The object sent with the request to retrieve a list of logs from your organization.

        :param compute: The list of metrics or timeseries to compute for the retrieved buckets.
        :type compute: [LogsCompute], optional

        :param filter: The search and filter query settings
        :type filter: LogsQueryFilter, optional

        :param group_by: The rules for the group by
        :type group_by: [LogsGroupBy], optional

        :param options: Global query options that are used during the query.
            Note: You should only supply timezone or time offset but not both otherwise the query will fail.
        :type options: LogsQueryOptions, optional

        :param page: Paging settings
        :type page: LogsAggregateRequestPage, optional
        """
        if compute is not unset:
            kwargs["compute"] = compute
        if filter is not unset:
            kwargs["filter"] = filter
        if group_by is not unset:
            kwargs["group_by"] = group_by
        if options is not unset:
            kwargs["options"] = options
        if page is not unset:
            kwargs["page"] = page
        super().__init__(kwargs)
