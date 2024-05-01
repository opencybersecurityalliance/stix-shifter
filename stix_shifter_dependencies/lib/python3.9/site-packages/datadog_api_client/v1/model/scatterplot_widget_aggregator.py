# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ScatterplotWidgetAggregator(ModelSimple):
    """
    Aggregator used for the request.

    :param value: Must be one of ["avg", "last", "max", "min", "sum"].
    :type value: str
    """

    allowed_values = {
        "avg",
        "last",
        "max",
        "min",
        "sum",
    }
    AVERAGE: ClassVar["ScatterplotWidgetAggregator"]
    LAST: ClassVar["ScatterplotWidgetAggregator"]
    MAXIMUM: ClassVar["ScatterplotWidgetAggregator"]
    MINIMUM: ClassVar["ScatterplotWidgetAggregator"]
    SUM: ClassVar["ScatterplotWidgetAggregator"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ScatterplotWidgetAggregator.AVERAGE = ScatterplotWidgetAggregator("avg")
ScatterplotWidgetAggregator.LAST = ScatterplotWidgetAggregator("last")
ScatterplotWidgetAggregator.MAXIMUM = ScatterplotWidgetAggregator("max")
ScatterplotWidgetAggregator.MINIMUM = ScatterplotWidgetAggregator("min")
ScatterplotWidgetAggregator.SUM = ScatterplotWidgetAggregator("sum")
