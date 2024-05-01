# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class WidgetVizType(ModelSimple):
    """
    Whether to display the Alert Graph as a timeseries or a top list.

    :param value: Must be one of ["timeseries", "toplist"].
    :type value: str
    """

    allowed_values = {
        "timeseries",
        "toplist",
    }
    TIMESERIES: ClassVar["WidgetVizType"]
    TOPLIST: ClassVar["WidgetVizType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


WidgetVizType.TIMESERIES = WidgetVizType("timeseries")
WidgetVizType.TOPLIST = WidgetVizType("toplist")
