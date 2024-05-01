# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsStatusRemapperType(ModelSimple):
    """
    Type of logs status remapper.

    :param value: If omitted defaults to "status-remapper". Must be one of ["status-remapper"].
    :type value: str
    """

    allowed_values = {
        "status-remapper",
    }
    STATUS_REMAPPER: ClassVar["LogsStatusRemapperType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsStatusRemapperType.STATUS_REMAPPER = LogsStatusRemapperType("status-remapper")
