# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MonitorSummaryWidgetDefinitionType(ModelSimple):
    """
    Type of the monitor summary widget.

    :param value: If omitted defaults to "manage_status". Must be one of ["manage_status"].
    :type value: str
    """

    allowed_values = {
        "manage_status",
    }
    MANAGE_STATUS: ClassVar["MonitorSummaryWidgetDefinitionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MonitorSummaryWidgetDefinitionType.MANAGE_STATUS = MonitorSummaryWidgetDefinitionType("manage_status")
