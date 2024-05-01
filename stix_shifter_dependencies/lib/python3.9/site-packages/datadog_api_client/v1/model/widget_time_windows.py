# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetTimeWindows(ModelSimple):
    """
    Define a time window.

    :param value: Must be one of ["7d", "30d", "90d", "week_to_date", "previous_week", "month_to_date", "previous_month", "global_time"].
    :type value: str
    """

    allowed_values = {
        "7d",
        "30d",
        "90d",
        "week_to_date",
        "previous_week",
        "month_to_date",
        "previous_month",
        "global_time",
    }
    SEVEN_DAYS: ClassVar["WidgetTimeWindows"]
    THIRTY_DAYS: ClassVar["WidgetTimeWindows"]
    NINETY_DAYS: ClassVar["WidgetTimeWindows"]
    WEEK_TO_DATE: ClassVar["WidgetTimeWindows"]
    PREVIOUS_WEEK: ClassVar["WidgetTimeWindows"]
    MONTH_TO_DATE: ClassVar["WidgetTimeWindows"]
    PREVIOUS_MONTH: ClassVar["WidgetTimeWindows"]
    GLOBAL_TIME: ClassVar["WidgetTimeWindows"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetTimeWindows.SEVEN_DAYS = WidgetTimeWindows("7d")
WidgetTimeWindows.THIRTY_DAYS = WidgetTimeWindows("30d")
WidgetTimeWindows.NINETY_DAYS = WidgetTimeWindows("90d")
WidgetTimeWindows.WEEK_TO_DATE = WidgetTimeWindows("week_to_date")
WidgetTimeWindows.PREVIOUS_WEEK = WidgetTimeWindows("previous_week")
WidgetTimeWindows.MONTH_TO_DATE = WidgetTimeWindows("month_to_date")
WidgetTimeWindows.PREVIOUS_MONTH = WidgetTimeWindows("previous_month")
WidgetTimeWindows.GLOBAL_TIME = WidgetTimeWindows("global_time")
