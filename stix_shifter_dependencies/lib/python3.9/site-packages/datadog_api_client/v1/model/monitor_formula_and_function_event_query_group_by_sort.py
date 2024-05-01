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
    from datadog_api_client.v1.model.monitor_formula_and_function_event_aggregation import (
        MonitorFormulaAndFunctionEventAggregation,
    )
    from datadog_api_client.v1.model.query_sort_order import QuerySortOrder


class MonitorFormulaAndFunctionEventQueryGroupBySort(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.monitor_formula_and_function_event_aggregation import (
            MonitorFormulaAndFunctionEventAggregation,
        )
        from datadog_api_client.v1.model.query_sort_order import QuerySortOrder

        return {
            "aggregation": (MonitorFormulaAndFunctionEventAggregation,),
            "metric": (str,),
            "order": (QuerySortOrder,),
        }

    attribute_map = {
        "aggregation": "aggregation",
        "metric": "metric",
        "order": "order",
    }

    def __init__(
        self_,
        aggregation: MonitorFormulaAndFunctionEventAggregation,
        metric: Union[str, UnsetType] = unset,
        order: Union[QuerySortOrder, UnsetType] = unset,
        **kwargs,
    ):
        """
        Options for sorting group by results.

        :param aggregation: Aggregation methods for event platform queries.
        :type aggregation: MonitorFormulaAndFunctionEventAggregation

        :param metric: Metric used for sorting group by results.
        :type metric: str, optional

        :param order: Direction of sort.
        :type order: QuerySortOrder, optional
        """
        if metric is not unset:
            kwargs["metric"] = metric
        if order is not unset:
            kwargs["order"] = order
        super().__init__(kwargs)

        self_.aggregation = aggregation
