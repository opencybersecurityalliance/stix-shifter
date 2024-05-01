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
    from datadog_api_client.v2.model.ci_app_aggregation_function import CIAppAggregationFunction
    from datadog_api_client.v2.model.ci_app_sort_order import CIAppSortOrder
    from datadog_api_client.v2.model.ci_app_aggregate_sort_type import CIAppAggregateSortType


class CIAppAggregateSort(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.ci_app_aggregation_function import CIAppAggregationFunction
        from datadog_api_client.v2.model.ci_app_sort_order import CIAppSortOrder
        from datadog_api_client.v2.model.ci_app_aggregate_sort_type import CIAppAggregateSortType

        return {
            "aggregation": (CIAppAggregationFunction,),
            "metric": (str,),
            "order": (CIAppSortOrder,),
            "type": (CIAppAggregateSortType,),
        }

    attribute_map = {
        "aggregation": "aggregation",
        "metric": "metric",
        "order": "order",
        "type": "type",
    }

    def __init__(
        self_,
        aggregation: Union[CIAppAggregationFunction, UnsetType] = unset,
        metric: Union[str, UnsetType] = unset,
        order: Union[CIAppSortOrder, UnsetType] = unset,
        type: Union[CIAppAggregateSortType, UnsetType] = unset,
        **kwargs,
    ):
        """
        A sort rule.

        :param aggregation: An aggregation function.
        :type aggregation: CIAppAggregationFunction, optional

        :param metric: The metric to sort by (only used for ``type=measure`` ).
        :type metric: str, optional

        :param order: The order to use, ascending or descending.
        :type order: CIAppSortOrder, optional

        :param type: The type of sorting algorithm.
        :type type: CIAppAggregateSortType, optional
        """
        if aggregation is not unset:
            kwargs["aggregation"] = aggregation
        if metric is not unset:
            kwargs["metric"] = metric
        if order is not unset:
            kwargs["order"] = order
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
