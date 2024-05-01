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
    from datadog_api_client.v2.model.ci_app_pipelines_query_filter import CIAppPipelinesQueryFilter
    from datadog_api_client.v2.model.ci_app_pipelines_group_by import CIAppPipelinesGroupBy
    from datadog_api_client.v2.model.ci_app_query_options import CIAppQueryOptions


class CIAppPipelinesAggregateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.ci_app_compute import CIAppCompute
        from datadog_api_client.v2.model.ci_app_pipelines_query_filter import CIAppPipelinesQueryFilter
        from datadog_api_client.v2.model.ci_app_pipelines_group_by import CIAppPipelinesGroupBy
        from datadog_api_client.v2.model.ci_app_query_options import CIAppQueryOptions

        return {
            "compute": ([CIAppCompute],),
            "filter": (CIAppPipelinesQueryFilter,),
            "group_by": ([CIAppPipelinesGroupBy],),
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
        filter: Union[CIAppPipelinesQueryFilter, UnsetType] = unset,
        group_by: Union[List[CIAppPipelinesGroupBy], UnsetType] = unset,
        options: Union[CIAppQueryOptions, UnsetType] = unset,
        **kwargs,
    ):
        """
        The object sent with the request to retrieve aggregation buckets of pipeline events from your organization.

        :param compute: The list of metrics or timeseries to compute for the retrieved buckets.
        :type compute: [CIAppCompute], optional

        :param filter: The search and filter query settings.
        :type filter: CIAppPipelinesQueryFilter, optional

        :param group_by: The rules for the group-by.
        :type group_by: [CIAppPipelinesGroupBy], optional

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
