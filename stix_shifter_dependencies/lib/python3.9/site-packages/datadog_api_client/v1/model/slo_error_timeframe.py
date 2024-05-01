# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SLOErrorTimeframe(ModelSimple):
    """
    The timeframe of the threshold associated with this error
        or "all" if all thresholds are affected.

    :param value: Must be one of ["7d", "30d", "90d", "all"].
    :type value: str
    """

    allowed_values = {
        "7d",
        "30d",
        "90d",
        "all",
    }
    SEVEN_DAYS: ClassVar["SLOErrorTimeframe"]
    THIRTY_DAYS: ClassVar["SLOErrorTimeframe"]
    NINETY_DAYS: ClassVar["SLOErrorTimeframe"]
    ALL: ClassVar["SLOErrorTimeframe"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SLOErrorTimeframe.SEVEN_DAYS = SLOErrorTimeframe("7d")
SLOErrorTimeframe.THIRTY_DAYS = SLOErrorTimeframe("30d")
SLOErrorTimeframe.NINETY_DAYS = SLOErrorTimeframe("90d")
SLOErrorTimeframe.ALL = SLOErrorTimeframe("all")
