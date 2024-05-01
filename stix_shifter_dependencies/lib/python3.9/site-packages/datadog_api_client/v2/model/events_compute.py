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


class EventsCompute(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.events_aggregation import EventsAggregation

        return {
            "aggregation": (EventsAggregation,),
            "interval": (int,),
            "metric": (str,),
        }

    attribute_map = {
        "aggregation": "aggregation",
        "interval": "interval",
        "metric": "metric",
    }

    def __init__(
        self_,
        aggregation: EventsAggregation,
        interval: Union[int, UnsetType] = unset,
        metric: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The instructions for what to compute for this query.

        :param aggregation: The type of aggregation that can be performed on events-based queries.
        :type aggregation: EventsAggregation

        :param interval: Interval for compute in milliseconds.
        :type interval: int, optional

        :param metric: The "measure" attribute on which to perform the computation.
        :type metric: str, optional
        """
        if interval is not unset:
            kwargs["interval"] = interval
        if metric is not unset:
            kwargs["metric"] = metric
        super().__init__(kwargs)

        self_.aggregation = aggregation
