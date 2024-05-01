# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SLOTimeframe(ModelSimple):
    """
    The SLO time window options.

    :param value: Must be one of ["7d", "30d", "90d", "custom"].
    :type value: str
    """

    allowed_values = {
        "7d",
        "30d",
        "90d",
        "custom",
    }
    SEVEN_DAYS: ClassVar["SLOTimeframe"]
    THIRTY_DAYS: ClassVar["SLOTimeframe"]
    NINETY_DAYS: ClassVar["SLOTimeframe"]
    CUSTOM: ClassVar["SLOTimeframe"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SLOTimeframe.SEVEN_DAYS = SLOTimeframe("7d")
SLOTimeframe.THIRTY_DAYS = SLOTimeframe("30d")
SLOTimeframe.NINETY_DAYS = SLOTimeframe("90d")
SLOTimeframe.CUSTOM = SLOTimeframe("custom")
