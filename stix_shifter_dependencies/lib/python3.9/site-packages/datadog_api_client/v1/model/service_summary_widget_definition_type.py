# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ServiceSummaryWidgetDefinitionType(ModelSimple):
    """
    Type of the service summary widget.

    :param value: If omitted defaults to "trace_service". Must be one of ["trace_service"].
    :type value: str
    """

    allowed_values = {
        "trace_service",
    }
    TRACE_SERVICE: ClassVar["ServiceSummaryWidgetDefinitionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ServiceSummaryWidgetDefinitionType.TRACE_SERVICE = ServiceSummaryWidgetDefinitionType("trace_service")
