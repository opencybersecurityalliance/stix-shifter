# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class DashboardGlobalTimeLiveSpan(ModelSimple):
    """
    Dashboard global time live_span selection

    :param value: Must be one of ["15m", "1h", "4h", "1d", "2d", "1w", "1mo", "3mo"].
    :type value: str
    """

    allowed_values = {
        "15m",
        "1h",
        "4h",
        "1d",
        "2d",
        "1w",
        "1mo",
        "3mo",
    }
    PAST_FIFTEEN_MINUTES: ClassVar["DashboardGlobalTimeLiveSpan"]
    PAST_ONE_HOUR: ClassVar["DashboardGlobalTimeLiveSpan"]
    PAST_FOUR_HOURS: ClassVar["DashboardGlobalTimeLiveSpan"]
    PAST_ONE_DAY: ClassVar["DashboardGlobalTimeLiveSpan"]
    PAST_TWO_DAYS: ClassVar["DashboardGlobalTimeLiveSpan"]
    PAST_ONE_WEEK: ClassVar["DashboardGlobalTimeLiveSpan"]
    PAST_ONE_MONTH: ClassVar["DashboardGlobalTimeLiveSpan"]
    PAST_THREE_MONTHS: ClassVar["DashboardGlobalTimeLiveSpan"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


DashboardGlobalTimeLiveSpan.PAST_FIFTEEN_MINUTES = DashboardGlobalTimeLiveSpan("15m")
DashboardGlobalTimeLiveSpan.PAST_ONE_HOUR = DashboardGlobalTimeLiveSpan("1h")
DashboardGlobalTimeLiveSpan.PAST_FOUR_HOURS = DashboardGlobalTimeLiveSpan("4h")
DashboardGlobalTimeLiveSpan.PAST_ONE_DAY = DashboardGlobalTimeLiveSpan("1d")
DashboardGlobalTimeLiveSpan.PAST_TWO_DAYS = DashboardGlobalTimeLiveSpan("2d")
DashboardGlobalTimeLiveSpan.PAST_ONE_WEEK = DashboardGlobalTimeLiveSpan("1w")
DashboardGlobalTimeLiveSpan.PAST_ONE_MONTH = DashboardGlobalTimeLiveSpan("1mo")
DashboardGlobalTimeLiveSpan.PAST_THREE_MONTHS = DashboardGlobalTimeLiveSpan("3mo")
