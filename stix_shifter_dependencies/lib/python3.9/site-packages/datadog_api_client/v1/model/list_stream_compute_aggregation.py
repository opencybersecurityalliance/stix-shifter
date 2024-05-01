# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ListStreamComputeAggregation(ModelSimple):
    """
    Aggregation value.

    :param value: Must be one of ["count", "cardinality", "median", "pc75", "pc90", "pc95", "pc98", "pc99", "sum", "min", "max", "avg", "earliest", "latest", "most_frequent"].
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
        "earliest",
        "latest",
        "most_frequent",
    }
    COUNT: ClassVar["ListStreamComputeAggregation"]
    CARDINALITY: ClassVar["ListStreamComputeAggregation"]
    MEDIAN: ClassVar["ListStreamComputeAggregation"]
    PC75: ClassVar["ListStreamComputeAggregation"]
    PC90: ClassVar["ListStreamComputeAggregation"]
    PC95: ClassVar["ListStreamComputeAggregation"]
    PC98: ClassVar["ListStreamComputeAggregation"]
    PC99: ClassVar["ListStreamComputeAggregation"]
    SUM: ClassVar["ListStreamComputeAggregation"]
    MIN: ClassVar["ListStreamComputeAggregation"]
    MAX: ClassVar["ListStreamComputeAggregation"]
    AVG: ClassVar["ListStreamComputeAggregation"]
    EARLIEST: ClassVar["ListStreamComputeAggregation"]
    LATEST: ClassVar["ListStreamComputeAggregation"]
    MOST_FREQUENT: ClassVar["ListStreamComputeAggregation"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ListStreamComputeAggregation.COUNT = ListStreamComputeAggregation("count")
ListStreamComputeAggregation.CARDINALITY = ListStreamComputeAggregation("cardinality")
ListStreamComputeAggregation.MEDIAN = ListStreamComputeAggregation("median")
ListStreamComputeAggregation.PC75 = ListStreamComputeAggregation("pc75")
ListStreamComputeAggregation.PC90 = ListStreamComputeAggregation("pc90")
ListStreamComputeAggregation.PC95 = ListStreamComputeAggregation("pc95")
ListStreamComputeAggregation.PC98 = ListStreamComputeAggregation("pc98")
ListStreamComputeAggregation.PC99 = ListStreamComputeAggregation("pc99")
ListStreamComputeAggregation.SUM = ListStreamComputeAggregation("sum")
ListStreamComputeAggregation.MIN = ListStreamComputeAggregation("min")
ListStreamComputeAggregation.MAX = ListStreamComputeAggregation("max")
ListStreamComputeAggregation.AVG = ListStreamComputeAggregation("avg")
ListStreamComputeAggregation.EARLIEST = ListStreamComputeAggregation("earliest")
ListStreamComputeAggregation.LATEST = ListStreamComputeAggregation("latest")
ListStreamComputeAggregation.MOST_FREQUENT = ListStreamComputeAggregation("most_frequent")
