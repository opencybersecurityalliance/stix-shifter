# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MetricCustomTimeAggregation(ModelSimple):
    """
    A time aggregation for use in query.

    :param value: Must be one of ["avg", "count", "max", "min", "sum"].
    :type value: str
    """

    allowed_values = {
        "avg",
        "count",
        "max",
        "min",
        "sum",
    }
    AVG: ClassVar["MetricCustomTimeAggregation"]
    COUNT: ClassVar["MetricCustomTimeAggregation"]
    MAX: ClassVar["MetricCustomTimeAggregation"]
    MIN: ClassVar["MetricCustomTimeAggregation"]
    SUM: ClassVar["MetricCustomTimeAggregation"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MetricCustomTimeAggregation.AVG = MetricCustomTimeAggregation("avg")
MetricCustomTimeAggregation.COUNT = MetricCustomTimeAggregation("count")
MetricCustomTimeAggregation.MAX = MetricCustomTimeAggregation("max")
MetricCustomTimeAggregation.MIN = MetricCustomTimeAggregation("min")
MetricCustomTimeAggregation.SUM = MetricCustomTimeAggregation("sum")
