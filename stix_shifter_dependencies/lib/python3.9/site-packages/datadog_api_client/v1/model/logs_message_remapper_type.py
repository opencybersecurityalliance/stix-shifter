# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsMessageRemapperType(ModelSimple):
    """
    Type of logs message remapper.

    :param value: If omitted defaults to "message-remapper". Must be one of ["message-remapper"].
    :type value: str
    """

    allowed_values = {
        "message-remapper",
    }
    MESSAGE_REMAPPER: ClassVar["LogsMessageRemapperType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsMessageRemapperType.MESSAGE_REMAPPER = LogsMessageRemapperType("message-remapper")
