# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogStreamWidgetDefinitionType(ModelSimple):
    """
    Type of the log stream widget.

    :param value: If omitted defaults to "log_stream". Must be one of ["log_stream"].
    :type value: str
    """

    allowed_values = {
        "log_stream",
    }
    LOG_STREAM: ClassVar["LogStreamWidgetDefinitionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogStreamWidgetDefinitionType.LOG_STREAM = LogStreamWidgetDefinitionType("log_stream")
