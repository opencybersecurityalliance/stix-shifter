# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetCompareTo(ModelSimple):
    """
    Timeframe used for the change comparison.

    :param value: Must be one of ["hour_before", "day_before", "week_before", "month_before"].
    :type value: str
    """

    allowed_values = {
        "hour_before",
        "day_before",
        "week_before",
        "month_before",
    }
    HOUR_BEFORE: ClassVar["WidgetCompareTo"]
    DAY_BEFORE: ClassVar["WidgetCompareTo"]
    WEEK_BEFORE: ClassVar["WidgetCompareTo"]
    MONTH_BEFORE: ClassVar["WidgetCompareTo"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetCompareTo.HOUR_BEFORE = WidgetCompareTo("hour_before")
WidgetCompareTo.DAY_BEFORE = WidgetCompareTo("day_before")
WidgetCompareTo.WEEK_BEFORE = WidgetCompareTo("week_before")
WidgetCompareTo.MONTH_BEFORE = WidgetCompareTo("month_before")
