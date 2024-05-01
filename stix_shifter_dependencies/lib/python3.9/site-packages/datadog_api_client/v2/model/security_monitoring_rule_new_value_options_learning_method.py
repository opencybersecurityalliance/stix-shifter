# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SecurityMonitoringRuleNewValueOptionsLearningMethod(ModelSimple):
    """
    The learning method used to determine when signals should be generated for values that weren't learned.

    :param value: If omitted defaults to "duration". Must be one of ["duration", "threshold"].
    :type value: str
    """

    allowed_values = {
        "duration",
        "threshold",
    }
    DURATION: ClassVar["SecurityMonitoringRuleNewValueOptionsLearningMethod"]
    THRESHOLD: ClassVar["SecurityMonitoringRuleNewValueOptionsLearningMethod"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SecurityMonitoringRuleNewValueOptionsLearningMethod.DURATION = SecurityMonitoringRuleNewValueOptionsLearningMethod(
    "duration"
)
SecurityMonitoringRuleNewValueOptionsLearningMethod.THRESHOLD = SecurityMonitoringRuleNewValueOptionsLearningMethod(
    "threshold"
)
