# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class RUMAggregationFunction(ModelSimple):
    """
    An aggregation function.

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
    COUNT: ClassVar["RUMAggregationFunction"]
    CARDINALITY: ClassVar["RUMAggregationFunction"]
    PERCENTILE_75: ClassVar["RUMAggregationFunction"]
    PERCENTILE_90: ClassVar["RUMAggregationFunction"]
    PERCENTILE_95: ClassVar["RUMAggregationFunction"]
    PERCENTILE_98: ClassVar["RUMAggregationFunction"]
    PERCENTILE_99: ClassVar["RUMAggregationFunction"]
    SUM: ClassVar["RUMAggregationFunction"]
    MIN: ClassVar["RUMAggregationFunction"]
    MAX: ClassVar["RUMAggregationFunction"]
    AVG: ClassVar["RUMAggregationFunction"]
    MEDIAN: ClassVar["RUMAggregationFunction"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


RUMAggregationFunction.COUNT = RUMAggregationFunction("count")
RUMAggregationFunction.CARDINALITY = RUMAggregationFunction("cardinality")
RUMAggregationFunction.PERCENTILE_75 = RUMAggregationFunction("pc75")
RUMAggregationFunction.PERCENTILE_90 = RUMAggregationFunction("pc90")
RUMAggregationFunction.PERCENTILE_95 = RUMAggregationFunction("pc95")
RUMAggregationFunction.PERCENTILE_98 = RUMAggregationFunction("pc98")
RUMAggregationFunction.PERCENTILE_99 = RUMAggregationFunction("pc99")
RUMAggregationFunction.SUM = RUMAggregationFunction("sum")
RUMAggregationFunction.MIN = RUMAggregationFunction("min")
RUMAggregationFunction.MAX = RUMAggregationFunction("max")
RUMAggregationFunction.AVG = RUMAggregationFunction("avg")
RUMAggregationFunction.MEDIAN = RUMAggregationFunction("median")
