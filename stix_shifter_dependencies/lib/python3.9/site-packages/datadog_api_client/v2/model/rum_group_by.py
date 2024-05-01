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
    from datadog_api_client.v2.model.rum_group_by_histogram import RUMGroupByHistogram
    from datadog_api_client.v2.model.rum_group_by_missing import RUMGroupByMissing
    from datadog_api_client.v2.model.rum_aggregate_sort import RUMAggregateSort
    from datadog_api_client.v2.model.rum_group_by_total import RUMGroupByTotal


class RUMGroupBy(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.rum_group_by_histogram import RUMGroupByHistogram
        from datadog_api_client.v2.model.rum_group_by_missing import RUMGroupByMissing
        from datadog_api_client.v2.model.rum_aggregate_sort import RUMAggregateSort
        from datadog_api_client.v2.model.rum_group_by_total import RUMGroupByTotal

        return {
            "facet": (str,),
            "histogram": (RUMGroupByHistogram,),
            "limit": (int,),
            "missing": (RUMGroupByMissing,),
            "sort": (RUMAggregateSort,),
            "total": (RUMGroupByTotal,),
        }

    attribute_map = {
        "facet": "facet",
        "histogram": "histogram",
        "limit": "limit",
        "missing": "missing",
        "sort": "sort",
        "total": "total",
    }

    def __init__(
        self_,
        facet: str,
        histogram: Union[RUMGroupByHistogram, UnsetType] = unset,
        limit: Union[int, UnsetType] = unset,
        missing: Union[RUMGroupByMissing, str, float, UnsetType] = unset,
        sort: Union[RUMAggregateSort, UnsetType] = unset,
        total: Union[RUMGroupByTotal, bool, str, float, UnsetType] = unset,
        **kwargs,
    ):
        """
        A group-by rule.

        :param facet: The name of the facet to use (required).
        :type facet: str

        :param histogram: Used to perform a histogram computation (only for measure facets).
            Note: At most 100 buckets are allowed, the number of buckets is (max - min)/interval.
        :type histogram: RUMGroupByHistogram, optional

        :param limit: The maximum buckets to return for this group-by.
        :type limit: int, optional

        :param missing: The value to use for logs that don't have the facet used to group by.
        :type missing: RUMGroupByMissing, optional

        :param sort: A sort rule.
        :type sort: RUMAggregateSort, optional

        :param total: A resulting object to put the given computes in over all the matching records.
        :type total: RUMGroupByTotal, optional
        """
        if histogram is not unset:
            kwargs["histogram"] = histogram
        if limit is not unset:
            kwargs["limit"] = limit
        if missing is not unset:
            kwargs["missing"] = missing
        if sort is not unset:
            kwargs["sort"] = sort
        if total is not unset:
            kwargs["total"] = total
        super().__init__(kwargs)

        self_.facet = facet
