# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SecurityMonitoringRuleDetectionMethod(ModelSimple):
    """
    The detection method.

    :param value: Must be one of ["threshold", "new_value", "anomaly_detection", "impossible_travel", "hardcoded", "third_party"].
    :type value: str
    """

    allowed_values = {
        "threshold",
        "new_value",
        "anomaly_detection",
        "impossible_travel",
        "hardcoded",
        "third_party",
    }
    THRESHOLD: ClassVar["SecurityMonitoringRuleDetectionMethod"]
    NEW_VALUE: ClassVar["SecurityMonitoringRuleDetectionMethod"]
    ANOMALY_DETECTION: ClassVar["SecurityMonitoringRuleDetectionMethod"]
    IMPOSSIBLE_TRAVEL: ClassVar["SecurityMonitoringRuleDetectionMethod"]
    HARDCODED: ClassVar["SecurityMonitoringRuleDetectionMethod"]
    THIRD_PARTY: ClassVar["SecurityMonitoringRuleDetectionMethod"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SecurityMonitoringRuleDetectionMethod.THRESHOLD = SecurityMonitoringRuleDetectionMethod("threshold")
SecurityMonitoringRuleDetectionMethod.NEW_VALUE = SecurityMonitoringRuleDetectionMethod("new_value")
SecurityMonitoringRuleDetectionMethod.ANOMALY_DETECTION = SecurityMonitoringRuleDetectionMethod("anomaly_detection")
SecurityMonitoringRuleDetectionMethod.IMPOSSIBLE_TRAVEL = SecurityMonitoringRuleDetectionMethod("impossible_travel")
SecurityMonitoringRuleDetectionMethod.HARDCODED = SecurityMonitoringRuleDetectionMethod("hardcoded")
SecurityMonitoringRuleDetectionMethod.THIRD_PARTY = SecurityMonitoringRuleDetectionMethod("third_party")
