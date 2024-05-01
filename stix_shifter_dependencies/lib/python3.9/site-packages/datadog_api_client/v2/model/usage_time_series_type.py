# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class UsageTimeSeriesType(ModelSimple):
    """
    Type of usage data.

    :param value: If omitted defaults to "usage_timeseries". Must be one of ["usage_timeseries"].
    :type value: str
    """

    allowed_values = {
        "usage_timeseries",
    }
    USAGE_TIMESERIES: ClassVar["UsageTimeSeriesType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


UsageTimeSeriesType.USAGE_TIMESERIES = UsageTimeSeriesType("usage_timeseries")
