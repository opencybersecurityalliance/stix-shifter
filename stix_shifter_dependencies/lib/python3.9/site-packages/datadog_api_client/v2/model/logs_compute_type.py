# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsComputeType(ModelSimple):
    """
    The type of compute

    :param value: If omitted defaults to "total". Must be one of ["timeseries", "total"].
    :type value: str
    """

    allowed_values = {
        "timeseries",
        "total",
    }
    TIMESERIES: ClassVar["LogsComputeType"]
    TOTAL: ClassVar["LogsComputeType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsComputeType.TIMESERIES = LogsComputeType("timeseries")
LogsComputeType.TOTAL = LogsComputeType("total")
