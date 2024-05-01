# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class FormulaAndFunctionEventAggregation(ModelSimple):
    """
    Aggregation methods for event platform queries.

    :param value: Must be one of ["count", "cardinality", "median", "pc75", "pc90", "pc95", "pc98", "pc99", "sum", "min", "max", "avg"].
    :type value: str
    """

    allowed_values = {
        "count",
        "cardinality",
        "median",
        "pc75",
        "pc90",
        "pc95",
        "pc98",
        "pc99",
        "sum",
        "min",
        "max",
        "avg",
    }
    COUNT: ClassVar["FormulaAndFunctionEventAggregation"]
    CARDINALITY: ClassVar["FormulaAndFunctionEventAggregation"]
    MEDIAN: ClassVar["FormulaAndFunctionEventAggregation"]
    PC75: ClassVar["FormulaAndFunctionEventAggregation"]
    PC90: ClassVar["FormulaAndFunctionEventAggregation"]
    PC95: ClassVar["FormulaAndFunctionEventAggregation"]
    PC98: ClassVar["FormulaAndFunctionEventAggregation"]
    PC99: ClassVar["FormulaAndFunctionEventAggregation"]
    SUM: ClassVar["FormulaAndFunctionEventAggregation"]
    MIN: ClassVar["FormulaAndFunctionEventAggregation"]
    MAX: ClassVar["FormulaAndFunctionEventAggregation"]
    AVG: ClassVar["FormulaAndFunctionEventAggregation"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


FormulaAndFunctionEventAggregation.COUNT = FormulaAndFunctionEventAggregation("count")
FormulaAndFunctionEventAggregation.CARDINALITY = FormulaAndFunctionEventAggregation("cardinality")
FormulaAndFunctionEventAggregation.MEDIAN = FormulaAndFunctionEventAggregation("median")
FormulaAndFunctionEventAggregation.PC75 = FormulaAndFunctionEventAggregation("pc75")
FormulaAndFunctionEventAggregation.PC90 = FormulaAndFunctionEventAggregation("pc90")
FormulaAndFunctionEventAggregation.PC95 = FormulaAndFunctionEventAggregation("pc95")
FormulaAndFunctionEventAggregation.PC98 = FormulaAndFunctionEventAggregation("pc98")
FormulaAndFunctionEventAggregation.PC99 = FormulaAndFunctionEventAggregation("pc99")
FormulaAndFunctionEventAggregation.SUM = FormulaAndFunctionEventAggregation("sum")
FormulaAndFunctionEventAggregation.MIN = FormulaAndFunctionEventAggregation("min")
FormulaAndFunctionEventAggregation.MAX = FormulaAndFunctionEventAggregation("max")
FormulaAndFunctionEventAggregation.AVG = FormulaAndFunctionEventAggregation("avg")
