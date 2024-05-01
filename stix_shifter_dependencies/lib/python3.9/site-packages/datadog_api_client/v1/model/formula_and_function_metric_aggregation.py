# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class FormulaAndFunctionMetricAggregation(ModelSimple):
    """
    The aggregation methods available for metrics queries.

    :param value: Must be one of ["avg", "min", "max", "sum", "last", "area", "l2norm", "percentile"].
    :type value: str
    """

    allowed_values = {
        "avg",
        "min",
        "max",
        "sum",
        "last",
        "area",
        "l2norm",
        "percentile",
    }
    AVG: ClassVar["FormulaAndFunctionMetricAggregation"]
    MIN: ClassVar["FormulaAndFunctionMetricAggregation"]
    MAX: ClassVar["FormulaAndFunctionMetricAggregation"]
    SUM: ClassVar["FormulaAndFunctionMetricAggregation"]
    LAST: ClassVar["FormulaAndFunctionMetricAggregation"]
    AREA: ClassVar["FormulaAndFunctionMetricAggregation"]
    L2NORM: ClassVar["FormulaAndFunctionMetricAggregation"]
    PERCENTILE: ClassVar["FormulaAndFunctionMetricAggregation"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


FormulaAndFunctionMetricAggregation.AVG = FormulaAndFunctionMetricAggregation("avg")
FormulaAndFunctionMetricAggregation.MIN = FormulaAndFunctionMetricAggregation("min")
FormulaAndFunctionMetricAggregation.MAX = FormulaAndFunctionMetricAggregation("max")
FormulaAndFunctionMetricAggregation.SUM = FormulaAndFunctionMetricAggregation("sum")
FormulaAndFunctionMetricAggregation.LAST = FormulaAndFunctionMetricAggregation("last")
FormulaAndFunctionMetricAggregation.AREA = FormulaAndFunctionMetricAggregation("area")
FormulaAndFunctionMetricAggregation.L2NORM = FormulaAndFunctionMetricAggregation("l2norm")
FormulaAndFunctionMetricAggregation.PERCENTILE = FormulaAndFunctionMetricAggregation("percentile")
