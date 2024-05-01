# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsSort(ModelSimple):
    """
    Time-ascending `asc` or time-descending `desc` results.

    :param value: Must be one of ["asc", "desc"].
    :type value: str
    """

    allowed_values = {
        "asc",
        "desc",
    }
    TIME_ASCENDING: ClassVar["LogsSort"]
    TIME_DESCENDING: ClassVar["LogsSort"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsSort.TIME_ASCENDING = LogsSort("asc")
LogsSort.TIME_DESCENDING = LogsSort("desc")
