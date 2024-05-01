# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class TimeseriesWidgetLegendLayout(ModelSimple):
    """
    Layout of the legend.

    :param value: Must be one of ["auto", "horizontal", "vertical"].
    :type value: str
    """

    allowed_values = {
        "auto",
        "horizontal",
        "vertical",
    }
    AUTO: ClassVar["TimeseriesWidgetLegendLayout"]
    HORIZONTAL: ClassVar["TimeseriesWidgetLegendLayout"]
    VERTICAL: ClassVar["TimeseriesWidgetLegendLayout"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


TimeseriesWidgetLegendLayout.AUTO = TimeseriesWidgetLegendLayout("auto")
TimeseriesWidgetLegendLayout.HORIZONTAL = TimeseriesWidgetLegendLayout("horizontal")
TimeseriesWidgetLegendLayout.VERTICAL = TimeseriesWidgetLegendLayout("vertical")
