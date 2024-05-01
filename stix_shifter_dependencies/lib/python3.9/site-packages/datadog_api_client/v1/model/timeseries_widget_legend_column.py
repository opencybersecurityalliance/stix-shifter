# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class TimeseriesWidgetLegendColumn(ModelSimple):
    """
    Legend column.

    :param value: Must be one of ["value", "avg", "sum", "min", "max"].
    :type value: str
    """

    allowed_values = {
        "value",
        "avg",
        "sum",
        "min",
        "max",
    }
    VALUE: ClassVar["TimeseriesWidgetLegendColumn"]
    AVG: ClassVar["TimeseriesWidgetLegendColumn"]
    SUM: ClassVar["TimeseriesWidgetLegendColumn"]
    MIN: ClassVar["TimeseriesWidgetLegendColumn"]
    MAX: ClassVar["TimeseriesWidgetLegendColumn"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


TimeseriesWidgetLegendColumn.VALUE = TimeseriesWidgetLegendColumn("value")
TimeseriesWidgetLegendColumn.AVG = TimeseriesWidgetLegendColumn("avg")
TimeseriesWidgetLegendColumn.SUM = TimeseriesWidgetLegendColumn("sum")
TimeseriesWidgetLegendColumn.MIN = TimeseriesWidgetLegendColumn("min")
TimeseriesWidgetLegendColumn.MAX = TimeseriesWidgetLegendColumn("max")
