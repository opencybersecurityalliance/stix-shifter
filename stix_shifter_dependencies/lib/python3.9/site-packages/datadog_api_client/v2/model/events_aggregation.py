# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class EventsAggregation(ModelSimple):
    """
    The type of aggregation that can be performed on events-based queries.

    :param value: If omitted defaults to "count". Must be one of ["count", "cardinality", "pc75", "pc90", "pc95", "pc98", "pc99", "sum", "min", "max", "avg"].
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
    }
    COUNT: ClassVar["EventsAggregation"]
    CARDINALITY: ClassVar["EventsAggregation"]
    PC75: ClassVar["EventsAggregation"]
    PC90: ClassVar["EventsAggregation"]
    PC95: ClassVar["EventsAggregation"]
    PC98: ClassVar["EventsAggregation"]
    PC99: ClassVar["EventsAggregation"]
    SUM: ClassVar["EventsAggregation"]
    MIN: ClassVar["EventsAggregation"]
    MAX: ClassVar["EventsAggregation"]
    AVG: ClassVar["EventsAggregation"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


EventsAggregation.COUNT = EventsAggregation("count")
EventsAggregation.CARDINALITY = EventsAggregation("cardinality")
EventsAggregation.PC75 = EventsAggregation("pc75")
EventsAggregation.PC90 = EventsAggregation("pc90")
EventsAggregation.PC95 = EventsAggregation("pc95")
EventsAggregation.PC98 = EventsAggregation("pc98")
EventsAggregation.PC99 = EventsAggregation("pc99")
EventsAggregation.SUM = EventsAggregation("sum")
EventsAggregation.MIN = EventsAggregation("min")
EventsAggregation.MAX = EventsAggregation("max")
EventsAggregation.AVG = EventsAggregation("avg")
