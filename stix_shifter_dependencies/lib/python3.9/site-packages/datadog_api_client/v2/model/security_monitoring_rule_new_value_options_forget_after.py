# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SecurityMonitoringRuleNewValueOptionsForgetAfter(ModelSimple):
    """
    The duration in days after which a learned value is forgotten.

    :param value: Must be one of [1, 2, 7, 14, 21, 28].
    :type value: int
    """

    allowed_values = {
        1,
        2,
        7,
        14,
        21,
        28,
    }
    ONE_DAY: ClassVar["SecurityMonitoringRuleNewValueOptionsForgetAfter"]
    TWO_DAYS: ClassVar["SecurityMonitoringRuleNewValueOptionsForgetAfter"]
    ONE_WEEK: ClassVar["SecurityMonitoringRuleNewValueOptionsForgetAfter"]
    TWO_WEEKS: ClassVar["SecurityMonitoringRuleNewValueOptionsForgetAfter"]
    THREE_WEEKS: ClassVar["SecurityMonitoringRuleNewValueOptionsForgetAfter"]
    FOUR_WEEKS: ClassVar["SecurityMonitoringRuleNewValueOptionsForgetAfter"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (int,),
        }


SecurityMonitoringRuleNewValueOptionsForgetAfter.ONE_DAY = SecurityMonitoringRuleNewValueOptionsForgetAfter(1)
SecurityMonitoringRuleNewValueOptionsForgetAfter.TWO_DAYS = SecurityMonitoringRuleNewValueOptionsForgetAfter(2)
SecurityMonitoringRuleNewValueOptionsForgetAfter.ONE_WEEK = SecurityMonitoringRuleNewValueOptionsForgetAfter(7)
SecurityMonitoringRuleNewValueOptionsForgetAfter.TWO_WEEKS = SecurityMonitoringRuleNewValueOptionsForgetAfter(14)
SecurityMonitoringRuleNewValueOptionsForgetAfter.THREE_WEEKS = SecurityMonitoringRuleNewValueOptionsForgetAfter(21)
SecurityMonitoringRuleNewValueOptionsForgetAfter.FOUR_WEEKS = SecurityMonitoringRuleNewValueOptionsForgetAfter(28)
