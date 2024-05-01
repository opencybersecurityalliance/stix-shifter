# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class RUMSort(ModelSimple):
    """
    Sort parameters when querying events.

    :param value: Must be one of ["timestamp", "-timestamp"].
    :type value: str
    """

    allowed_values = {
        "timestamp",
        "-timestamp",
    }
    TIMESTAMP_ASCENDING: ClassVar["RUMSort"]
    TIMESTAMP_DESCENDING: ClassVar["RUMSort"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


RUMSort.TIMESTAMP_ASCENDING = RUMSort("timestamp")
RUMSort.TIMESTAMP_DESCENDING = RUMSort("-timestamp")
