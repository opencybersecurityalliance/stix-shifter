# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MonitorFormulaAndFunctionEventAggregation(ModelSimple):
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
    COUNT: ClassVar["MonitorFormulaAndFunctionEventAggregation"]
    CARDINALITY: ClassVar["MonitorFormulaAndFunctionEventAggregation"]
    MEDIAN: ClassVar["MonitorFormulaAndFunctionEventAggregation"]
    PC75: ClassVar["MonitorFormulaAndFunctionEventAggregation"]
    PC90: ClassVar["MonitorFormulaAndFunctionEventAggregation"]
    PC95: ClassVar["MonitorFormulaAndFunctionEventAggregation"]
    PC98: ClassVar["MonitorFormulaAndFunctionEventAggregation"]
    PC99: ClassVar["MonitorFormulaAndFunctionEventAggregation"]
    SUM: ClassVar["MonitorFormulaAndFunctionEventAggregation"]
    MIN: ClassVar["MonitorFormulaAndFunctionEventAggregation"]
    MAX: ClassVar["MonitorFormulaAndFunctionEventAggregation"]
    AVG: ClassVar["MonitorFormulaAndFunctionEventAggregation"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MonitorFormulaAndFunctionEventAggregation.COUNT = MonitorFormulaAndFunctionEventAggregation("count")
MonitorFormulaAndFunctionEventAggregation.CARDINALITY = MonitorFormulaAndFunctionEventAggregation("cardinality")
MonitorFormulaAndFunctionEventAggregation.MEDIAN = MonitorFormulaAndFunctionEventAggregation("median")
MonitorFormulaAndFunctionEventAggregation.PC75 = MonitorFormulaAndFunctionEventAggregation("pc75")
MonitorFormulaAndFunctionEventAggregation.PC90 = MonitorFormulaAndFunctionEventAggregation("pc90")
MonitorFormulaAndFunctionEventAggregation.PC95 = MonitorFormulaAndFunctionEventAggregation("pc95")
MonitorFormulaAndFunctionEventAggregation.PC98 = MonitorFormulaAndFunctionEventAggregation("pc98")
MonitorFormulaAndFunctionEventAggregation.PC99 = MonitorFormulaAndFunctionEventAggregation("pc99")
MonitorFormulaAndFunctionEventAggregation.SUM = MonitorFormulaAndFunctionEventAggregation("sum")
MonitorFormulaAndFunctionEventAggregation.MIN = MonitorFormulaAndFunctionEventAggregation("min")
MonitorFormulaAndFunctionEventAggregation.MAX = MonitorFormulaAndFunctionEventAggregation("max")
MonitorFormulaAndFunctionEventAggregation.AVG = MonitorFormulaAndFunctionEventAggregation("avg")
