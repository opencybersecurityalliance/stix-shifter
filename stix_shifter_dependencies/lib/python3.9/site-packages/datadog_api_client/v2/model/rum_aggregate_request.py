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
    from datadog_api_client.v2.model.rum_compute import RUMCompute
    from datadog_api_client.v2.model.rum_query_filter import RUMQueryFilter
    from datadog_api_client.v2.model.rum_group_by import RUMGroupBy
    from datadog_api_client.v2.model.rum_query_options import RUMQueryOptions
    from datadog_api_client.v2.model.rum_query_page_options import RUMQueryPageOptions


class RUMAggregateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.rum_compute import RUMCompute
        from datadog_api_client.v2.model.rum_query_filter import RUMQueryFilter
        from datadog_api_client.v2.model.rum_group_by import RUMGroupBy
        from datadog_api_client.v2.model.rum_query_options import RUMQueryOptions
        from datadog_api_client.v2.model.rum_query_page_options import RUMQueryPageOptions

        return {
            "compute": ([RUMCompute],),
            "filter": (RUMQueryFilter,),
            "group_by": ([RUMGroupBy],),
            "options": (RUMQueryOptions,),
            "page": (RUMQueryPageOptions,),
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
        compute: Union[List[RUMCompute], UnsetType] = unset,
        filter: Union[RUMQueryFilter, UnsetType] = unset,
        group_by: Union[List[RUMGroupBy], UnsetType] = unset,
        options: Union[RUMQueryOptions, UnsetType] = unset,
        page: Union[RUMQueryPageOptions, UnsetType] = unset,
        **kwargs,
    ):
        """
        The object sent with the request to retrieve aggregation buckets of RUM events from your organization.

        :param compute: The list of metrics or timeseries to compute for the retrieved buckets.
        :type compute: [RUMCompute], optional

        :param filter: The search and filter query settings.
        :type filter: RUMQueryFilter, optional

        :param group_by: The rules for the group by.
        :type group_by: [RUMGroupBy], optional

        :param options: Global query options that are used during the query.
            Note: Only supply timezone or time offset, not both. Otherwise, the query fails.
        :type options: RUMQueryOptions, optional

        :param page: Paging attributes for listing events.
        :type page: RUMQueryPageOptions, optional
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
