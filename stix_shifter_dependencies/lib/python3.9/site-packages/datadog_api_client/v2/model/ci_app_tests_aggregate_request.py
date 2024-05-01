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
    from datadog_api_client.v2.model.ci_app_compute import CIAppCompute
    from datadog_api_client.v2.model.ci_app_tests_query_filter import CIAppTestsQueryFilter
    from datadog_api_client.v2.model.ci_app_tests_group_by import CIAppTestsGroupBy
    from datadog_api_client.v2.model.ci_app_query_options import CIAppQueryOptions


class CIAppTestsAggregateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.ci_app_compute import CIAppCompute
        from datadog_api_client.v2.model.ci_app_tests_query_filter import CIAppTestsQueryFilter
        from datadog_api_client.v2.model.ci_app_tests_group_by import CIAppTestsGroupBy
        from datadog_api_client.v2.model.ci_app_query_options import CIAppQueryOptions

        return {
            "compute": ([CIAppCompute],),
            "filter": (CIAppTestsQueryFilter,),
            "group_by": ([CIAppTestsGroupBy],),
            "options": (CIAppQueryOptions,),
        }

    attribute_map = {
        "compute": "compute",
        "filter": "filter",
        "group_by": "group_by",
        "options": "options",
    }

    def __init__(
        self_,
        compute: Union[List[CIAppCompute], UnsetType] = unset,
        filter: Union[CIAppTestsQueryFilter, UnsetType] = unset,
        group_by: Union[List[CIAppTestsGroupBy], UnsetType] = unset,
        options: Union[CIAppQueryOptions, UnsetType] = unset,
        **kwargs,
    ):
        """
        The object sent with the request to retrieve aggregation buckets of test events from your organization.

        :param compute: The list of metrics or timeseries to compute for the retrieved buckets.
        :type compute: [CIAppCompute], optional

        :param filter: The search and filter query settings.
        :type filter: CIAppTestsQueryFilter, optional

        :param group_by: The rules for the group-by.
        :type group_by: [CIAppTestsGroupBy], optional

        :param options: Global query options that are used during the query.
            Only supply timezone or time offset, not both. Otherwise, the query fails.
        :type options: CIAppQueryOptions, optional
        """
        if compute is not unset:
            kwargs["compute"] = compute
        if filter is not unset:
            kwargs["filter"] = filter
        if group_by is not unset:
            kwargs["group_by"] = group_by
        if options is not unset:
            kwargs["options"] = options
        super().__init__(kwargs)
