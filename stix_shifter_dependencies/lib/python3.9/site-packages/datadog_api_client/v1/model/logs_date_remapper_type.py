# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsDateRemapperType(ModelSimple):
    """
    Type of logs date remapper.

    :param value: If omitted defaults to "date-remapper". Must be one of ["date-remapper"].
    :type value: str
    """

    allowed_values = {
        "date-remapper",
    }
    DATE_REMAPPER: ClassVar["LogsDateRemapperType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsDateRemapperType.DATE_REMAPPER = LogsDateRemapperType("date-remapper")
