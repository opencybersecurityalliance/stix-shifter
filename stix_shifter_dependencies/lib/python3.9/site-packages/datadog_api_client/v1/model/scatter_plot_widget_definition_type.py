# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ScatterPlotWidgetDefinitionType(ModelSimple):
    """
    Type of the scatter plot widget.

    :param value: If omitted defaults to "scatterplot". Must be one of ["scatterplot"].
    :type value: str
    """

    allowed_values = {
        "scatterplot",
    }
    SCATTERPLOT: ClassVar["ScatterPlotWidgetDefinitionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ScatterPlotWidgetDefinitionType.SCATTERPLOT = ScatterPlotWidgetDefinitionType("scatterplot")
