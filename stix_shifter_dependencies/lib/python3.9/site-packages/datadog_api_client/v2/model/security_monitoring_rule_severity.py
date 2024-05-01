# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SecurityMonitoringRuleSeverity(ModelSimple):
    """
    Severity of the Security Signal.

    :param value: Must be one of ["info", "low", "medium", "high", "critical"].
    :type value: str
    """

    allowed_values = {
        "info",
        "low",
        "medium",
        "high",
        "critical",
    }
    INFO: ClassVar["SecurityMonitoringRuleSeverity"]
    LOW: ClassVar["SecurityMonitoringRuleSeverity"]
    MEDIUM: ClassVar["SecurityMonitoringRuleSeverity"]
    HIGH: ClassVar["SecurityMonitoringRuleSeverity"]
    CRITICAL: ClassVar["SecurityMonitoringRuleSeverity"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SecurityMonitoringRuleSeverity.INFO = SecurityMonitoringRuleSeverity("info")
SecurityMonitoringRuleSeverity.LOW = SecurityMonitoringRuleSeverity("low")
SecurityMonitoringRuleSeverity.MEDIUM = SecurityMonitoringRuleSeverity("medium")
SecurityMonitoringRuleSeverity.HIGH = SecurityMonitoringRuleSeverity("high")
SecurityMonitoringRuleSeverity.CRITICAL = SecurityMonitoringRuleSeverity("critical")
