# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class TimeseriesWidgetDefinitionType(ModelSimple):
    """
    Type of the timeseries widget.

    :param value: If omitted defaults to "timeseries". Must be one of ["timeseries"].
    :type value: str
    """

    allowed_values = {
        "timeseries",
    }
    TIMESERIES: ClassVar["TimeseriesWidgetDefinitionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


TimeseriesWidgetDefinitionType.TIMESERIES = TimeseriesWidgetDefinitionType("timeseries")
