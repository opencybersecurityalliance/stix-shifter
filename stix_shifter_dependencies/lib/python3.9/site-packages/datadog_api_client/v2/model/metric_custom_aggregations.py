# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)


class MetricCustomAggregations(ModelSimple):
    """
    A list of queryable aggregation combinations for a count, rate, or gauge metric.
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


    :type value: [MetricCustomAggregation]
    """

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metric_custom_aggregation import MetricCustomAggregation

        return {
            "value": ([MetricCustomAggregation],),
        }
