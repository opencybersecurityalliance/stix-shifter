# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SLOState(ModelSimple):
    """
    State of the SLO.

    :param value: Must be one of ["breached", "warning", "ok", "no_data"].
    :type value: str
    """

    allowed_values = {
        "breached",
        "warning",
        "ok",
        "no_data",
    }
    BREACHED: ClassVar["SLOState"]
    WARNING: ClassVar["SLOState"]
    OK: ClassVar["SLOState"]
    NO_DATA: ClassVar["SLOState"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SLOState.BREACHED = SLOState("breached")
SLOState.WARNING = SLOState("warning")
SLOState.OK = SLOState("ok")
SLOState.NO_DATA = SLOState("no_data")
