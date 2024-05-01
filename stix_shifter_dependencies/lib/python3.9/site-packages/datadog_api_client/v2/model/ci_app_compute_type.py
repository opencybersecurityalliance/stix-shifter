# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class CIAppComputeType(ModelSimple):
    """
    The type of compute.

    :param value: If omitted defaults to "total". Must be one of ["timeseries", "total"].
    :type value: str
    """

    allowed_values = {
        "timeseries",
        "total",
    }
    TIMESERIES: ClassVar["CIAppComputeType"]
    TOTAL: ClassVar["CIAppComputeType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


CIAppComputeType.TIMESERIES = CIAppComputeType("timeseries")
CIAppComputeType.TOTAL = CIAppComputeType("total")
