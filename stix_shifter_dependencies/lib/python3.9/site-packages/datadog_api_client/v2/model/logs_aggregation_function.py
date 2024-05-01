# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsAggregationFunction(ModelSimple):
    """
    An aggregation function

    :param value: Must be one of ["count", "cardinality", "pc75", "pc90", "pc95", "pc98", "pc99", "sum", "min", "max", "avg", "median"].
    :type value: str
    """

    allowed_values = {
        "count",
        "cardinality",
        "pc75",
        "pc90",
        "pc95",
        "pc98",
        "pc99",
        "sum",
        "min",
        "max",
        "avg",
        "median",
    }
    COUNT: ClassVar["LogsAggregationFunction"]
    CARDINALITY: ClassVar["LogsAggregationFunction"]
    PERCENTILE_75: ClassVar["LogsAggregationFunction"]
    PERCENTILE_90: ClassVar["LogsAggregationFunction"]
    PERCENTILE_95: ClassVar["LogsAggregationFunction"]
    PERCENTILE_98: ClassVar["LogsAggregationFunction"]
    PERCENTILE_99: ClassVar["LogsAggregationFunction"]
    SUM: ClassVar["LogsAggregationFunction"]
    MIN: ClassVar["LogsAggregationFunction"]
    MAX: ClassVar["LogsAggregationFunction"]
    AVG: ClassVar["LogsAggregationFunction"]
    MEDIAN: ClassVar["LogsAggregationFunction"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsAggregationFunction.COUNT = LogsAggregationFunction("count")
LogsAggregationFunction.CARDINALITY = LogsAggregationFunction("cardinality")
LogsAggregationFunction.PERCENTILE_75 = LogsAggregationFunction("pc75")
LogsAggregationFunction.PERCENTILE_90 = LogsAggregationFunction("pc90")
LogsAggregationFunction.PERCENTILE_95 = LogsAggregationFunction("pc95")
LogsAggregationFunction.PERCENTILE_98 = LogsAggregationFunction("pc98")
LogsAggregationFunction.PERCENTILE_99 = LogsAggregationFunction("pc99")
LogsAggregationFunction.SUM = LogsAggregationFunction("sum")
LogsAggregationFunction.MIN = LogsAggregationFunction("min")
LogsAggregationFunction.MAX = LogsAggregationFunction("max")
LogsAggregationFunction.AVG = LogsAggregationFunction("avg")
LogsAggregationFunction.MEDIAN = LogsAggregationFunction("median")
