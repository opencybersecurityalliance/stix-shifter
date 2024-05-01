# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.metric_estimate_type import MetricEstimateType


class MetricEstimateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metric_estimate_type import MetricEstimateType

        return {
            "estimate_type": (MetricEstimateType,),
            "estimated_at": (datetime,),
            "estimated_output_series": (int,),
        }

    attribute_map = {
        "estimate_type": "estimate_type",
        "estimated_at": "estimated_at",
        "estimated_output_series": "estimated_output_series",
    }

    def __init__(
        self_,
        estimate_type: Union[MetricEstimateType, UnsetType] = unset,
        estimated_at: Union[datetime, UnsetType] = unset,
        estimated_output_series: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing the definition of a metric estimate attribute.

        :param estimate_type: Estimate type based on the queried configuration. By default, ``count_or_gauge`` is returned. ``distribution`` is returned for distribution metrics without percentiles enabled. Lastly, ``percentile`` is returned if ``filter[pct]=true`` is queried with a distribution metric.
        :type estimate_type: MetricEstimateType, optional

        :param estimated_at: Timestamp when the cardinality estimate was requested.
        :type estimated_at: datetime, optional

        :param estimated_output_series: Estimated cardinality of the metric based on the queried configuration.
        :type estimated_output_series: int, optional
        """
        if estimate_type is not unset:
            kwargs["estimate_type"] = estimate_type
        if estimated_at is not unset:
            kwargs["estimated_at"] = estimated_at
        if estimated_output_series is not unset:
            kwargs["estimated_output_series"] = estimated_output_series
        super().__init__(kwargs)
