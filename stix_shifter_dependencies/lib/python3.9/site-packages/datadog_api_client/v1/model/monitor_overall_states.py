# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MonitorOverallStates(ModelSimple):
    """
    The different states your monitor can be in.

    :param value: Must be one of ["Alert", "Ignored", "No Data", "OK", "Skipped", "Unknown", "Warn"].
    :type value: str
    """

    allowed_values = {
        "Alert",
        "Ignored",
        "No Data",
        "OK",
        "Skipped",
        "Unknown",
        "Warn",
    }
    ALERT: ClassVar["MonitorOverallStates"]
    IGNORED: ClassVar["MonitorOverallStates"]
    NO_DATA: ClassVar["MonitorOverallStates"]
    OK: ClassVar["MonitorOverallStates"]
    SKIPPED: ClassVar["MonitorOverallStates"]
    UNKNOWN: ClassVar["MonitorOverallStates"]
    WARN: ClassVar["MonitorOverallStates"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MonitorOverallStates.ALERT = MonitorOverallStates("Alert")
MonitorOverallStates.IGNORED = MonitorOverallStates("Ignored")
MonitorOverallStates.NO_DATA = MonitorOverallStates("No Data")
MonitorOverallStates.OK = MonitorOverallStates("OK")
MonitorOverallStates.SKIPPED = MonitorOverallStates("Skipped")
MonitorOverallStates.UNKNOWN = MonitorOverallStates("Unknown")
MonitorOverallStates.WARN = MonitorOverallStates("Warn")
