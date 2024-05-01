# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsArchiveState(ModelSimple):
    """
    The state of the archive.

    :param value: Must be one of ["UNKNOWN", "WORKING", "FAILING", "WORKING_AUTH_LEGACY"].
    :type value: str
    """

    allowed_values = {
        "UNKNOWN",
        "WORKING",
        "FAILING",
        "WORKING_AUTH_LEGACY",
    }
    UNKNOWN: ClassVar["LogsArchiveState"]
    WORKING: ClassVar["LogsArchiveState"]
    FAILING: ClassVar["LogsArchiveState"]
    WORKING_AUTH_LEGACY: ClassVar["LogsArchiveState"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsArchiveState.UNKNOWN = LogsArchiveState("UNKNOWN")
LogsArchiveState.WORKING = LogsArchiveState("WORKING")
LogsArchiveState.FAILING = LogsArchiveState("FAILING")
LogsArchiveState.WORKING_AUTH_LEGACY = LogsArchiveState("WORKING_AUTH_LEGACY")
