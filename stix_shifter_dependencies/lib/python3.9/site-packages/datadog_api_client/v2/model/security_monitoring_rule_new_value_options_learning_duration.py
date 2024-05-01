# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SecurityMonitoringRuleNewValueOptionsLearningDuration(ModelSimple):
    """
    The duration in days during which values are learned, and after which signals will be generated for values that
        weren't learned. If set to 0, a signal will be generated for all new values after the first value is learned.

    :param value: If omitted defaults to 0. Must be one of [0, 1, 7].
    :type value: int
    """

    allowed_values = {
        0,
        1,
        7,
    }
    ZERO_DAYS: ClassVar["SecurityMonitoringRuleNewValueOptionsLearningDuration"]
    ONE_DAY: ClassVar["SecurityMonitoringRuleNewValueOptionsLearningDuration"]
    SEVEN_DAYS: ClassVar["SecurityMonitoringRuleNewValueOptionsLearningDuration"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (int,),
        }


SecurityMonitoringRuleNewValueOptionsLearningDuration.ZERO_DAYS = SecurityMonitoringRuleNewValueOptionsLearningDuration(
    0
)
SecurityMonitoringRuleNewValueOptionsLearningDuration.ONE_DAY = SecurityMonitoringRuleNewValueOptionsLearningDuration(1)
SecurityMonitoringRuleNewValueOptionsLearningDuration.SEVEN_DAYS = (
    SecurityMonitoringRuleNewValueOptionsLearningDuration(7)
)
