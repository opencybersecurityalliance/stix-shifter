# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsTraceRemapperType(ModelSimple):
    """
    Type of logs trace remapper.

    :param value: If omitted defaults to "trace-id-remapper". Must be one of ["trace-id-remapper"].
    :type value: str
    """

    allowed_values = {
        "trace-id-remapper",
    }
    TRACE_ID_REMAPPER: ClassVar["LogsTraceRemapperType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsTraceRemapperType.TRACE_ID_REMAPPER = LogsTraceRemapperType("trace-id-remapper")
