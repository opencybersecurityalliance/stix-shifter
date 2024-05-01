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
    from datadog_api_client.v2.model.metric_custom_aggregations import MetricCustomAggregations
    from datadog_api_client.v2.model.metric_tag_configuration_metric_types import MetricTagConfigurationMetricTypes


class MetricTagConfigurationCreateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metric_custom_aggregations import MetricCustomAggregations
        from datadog_api_client.v2.model.metric_tag_configuration_metric_types import MetricTagConfigurationMetricTypes

        return {
            "aggregations": (MetricCustomAggregations,),
            "include_percentiles": (bool,),
            "metric_type": (MetricTagConfigurationMetricTypes,),
            "tags": ([str],),
        }

    attribute_map = {
        "aggregations": "aggregations",
        "include_percentiles": "include_percentiles",
        "metric_type": "metric_type",
        "tags": "tags",
    }

    def __init__(
        self_,
        metric_type: MetricTagConfigurationMetricTypes,
        aggregations: Union[MetricCustomAggregations, UnsetType] = unset,
        include_percentiles: Union[bool, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing the definition of a metric tag configuration to be created.

        :param aggregations: A list of queryable aggregation combinations for a count, rate, or gauge metric.
            By default, count and rate metrics require the (time: sum, space: sum) aggregation and
            Gauge metrics require the (time: avg, space: avg) aggregation.
            Additional time & space combinations are also available:

            * time: avg, space: avg
            * time: avg, space: max
            * time: avg, space: min
            * time: avg, space: sum
            * time: count, space: sum
            * time: max, space: max
            * time: min, space: min
            * time: sum, space: avg
            * time: sum, space: sum

            Can only be applied to metrics that have a ``metric_type`` of ``count`` , ``rate`` , or ``gauge``.
        :type aggregations: MetricCustomAggregations, optional

        :param include_percentiles: Toggle to include/exclude percentiles for a distribution metric.
            Defaults to false. Can only be applied to metrics that have a ``metric_type`` of ``distribution``.
        :type include_percentiles: bool, optional

        :param metric_type: The metric's type.
        :type metric_type: MetricTagConfigurationMetricTypes

        :param tags: A list of tag keys that will be queryable for your metric.
        :type tags: [str]
        """
        if aggregations is not unset:
            kwargs["aggregations"] = aggregations
        if include_percentiles is not unset:
            kwargs["include_percentiles"] = include_percentiles
        super().__init__(kwargs)
        tags = kwargs.get("tags", [])

        self_.metric_type = metric_type
        self_.tags = tags
