# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class CIAppAggregationFunction(ModelSimple):
    """
    An aggregation function.

    :param value: Must be one of ["count", "cardinality", "pc75", "pc90", "pc95", "pc98", "pc99", "sum", "min", "max", "avg", "median", "latest", "earliest", "most_frequent", "delta"].
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
        "latest",
        "earliest",
        "most_frequent",
        "delta",
    }
    COUNT: ClassVar["CIAppAggregationFunction"]
    CARDINALITY: ClassVar["CIAppAggregationFunction"]
    PERCENTILE_75: ClassVar["CIAppAggregationFunction"]
    PERCENTILE_90: ClassVar["CIAppAggregationFunction"]
    PERCENTILE_95: ClassVar["CIAppAggregationFunction"]
    PERCENTILE_98: ClassVar["CIAppAggregationFunction"]
    PERCENTILE_99: ClassVar["CIAppAggregationFunction"]
    SUM: ClassVar["CIAppAggregationFunction"]
    MIN: ClassVar["CIAppAggregationFunction"]
    MAX: ClassVar["CIAppAggregationFunction"]
    AVG: ClassVar["CIAppAggregationFunction"]
    MEDIAN: ClassVar["CIAppAggregationFunction"]
    LATEST: ClassVar["CIAppAggregationFunction"]
    EARLIEST: ClassVar["CIAppAggregationFunction"]
    MOST_FREQUENT: ClassVar["CIAppAggregationFunction"]
    DELTA: ClassVar["CIAppAggregationFunction"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


CIAppAggregationFunction.COUNT = CIAppAggregationFunction("count")
CIAppAggregationFunction.CARDINALITY = CIAppAggregationFunction("cardinality")
CIAppAggregationFunction.PERCENTILE_75 = CIAppAggregationFunction("pc75")
CIAppAggregationFunction.PERCENTILE_90 = CIAppAggregationFunction("pc90")
CIAppAggregationFunction.PERCENTILE_95 = CIAppAggregationFunction("pc95")
CIAppAggregationFunction.PERCENTILE_98 = CIAppAggregationFunction("pc98")
CIAppAggregationFunction.PERCENTILE_99 = CIAppAggregationFunction("pc99")
CIAppAggregationFunction.SUM = CIAppAggregationFunction("sum")
CIAppAggregationFunction.MIN = CIAppAggregationFunction("min")
CIAppAggregationFunction.MAX = CIAppAggregationFunction("max")
CIAppAggregationFunction.AVG = CIAppAggregationFunction("avg")
CIAppAggregationFunction.MEDIAN = CIAppAggregationFunction("median")
CIAppAggregationFunction.LATEST = CIAppAggregationFunction("latest")
CIAppAggregationFunction.EARLIEST = CIAppAggregationFunction("earliest")
CIAppAggregationFunction.MOST_FREQUENT = CIAppAggregationFunction("most_frequent")
CIAppAggregationFunction.DELTA = CIAppAggregationFunction("delta")
