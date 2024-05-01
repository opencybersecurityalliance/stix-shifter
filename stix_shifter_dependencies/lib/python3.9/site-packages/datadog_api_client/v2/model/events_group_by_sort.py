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
    from datadog_api_client.v2.model.events_aggregation import EventsAggregation
    from datadog_api_client.v2.model.query_sort_order import QuerySortOrder
    from datadog_api_client.v2.model.events_sort_type import EventsSortType


class EventsGroupBySort(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.events_aggregation import EventsAggregation
        from datadog_api_client.v2.model.query_sort_order import QuerySortOrder
        from datadog_api_client.v2.model.events_sort_type import EventsSortType

        return {
            "aggregation": (EventsAggregation,),
            "metric": (str,),
            "order": (QuerySortOrder,),
            "type": (EventsSortType,),
        }

    attribute_map = {
        "aggregation": "aggregation",
        "metric": "metric",
        "order": "order",
        "type": "type",
    }

    def __init__(
        self_,
        aggregation: EventsAggregation,
        metric: Union[str, UnsetType] = unset,
        order: Union[QuerySortOrder, UnsetType] = unset,
        type: Union[EventsSortType, UnsetType] = unset,
        **kwargs,
    ):
        """
        The dimension by which to sort a query's results.

        :param aggregation: The type of aggregation that can be performed on events-based queries.
        :type aggregation: EventsAggregation

        :param metric: Metric whose calculated value should be used to define the sort order of a query's results.
        :type metric: str, optional

        :param order: Direction of sort.
        :type order: QuerySortOrder, optional

        :param type: The type of sort to use on the calculated value.
        :type type: EventsSortType, optional
        """
        if metric is not unset:
            kwargs["metric"] = metric
        if order is not unset:
            kwargs["order"] = order
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)

        self_.aggregation = aggregation
