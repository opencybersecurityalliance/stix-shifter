# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SecurityMonitoringRuleMaxSignalDuration(ModelSimple):
    """
    A signal will “close” regardless of the query being matched once the time exceeds the maximum duration.
        This time is calculated from the first seen timestamp.

    :param value: Must be one of [0, 60, 300, 600, 900, 1800, 3600, 7200, 10800, 21600, 43200, 86400].
    :type value: int
    """

    allowed_values = {
        0,
        60,
        300,
        600,
        900,
        1800,
        3600,
        7200,
        10800,
        21600,
        43200,
        86400,
    }
    ZERO_MINUTES: ClassVar["SecurityMonitoringRuleMaxSignalDuration"]
    ONE_MINUTE: ClassVar["SecurityMonitoringRuleMaxSignalDuration"]
    FIVE_MINUTES: ClassVar["SecurityMonitoringRuleMaxSignalDuration"]
    TEN_MINUTES: ClassVar["SecurityMonitoringRuleMaxSignalDuration"]
    FIFTEEN_MINUTES: ClassVar["SecurityMonitoringRuleMaxSignalDuration"]
    THIRTY_MINUTES: ClassVar["SecurityMonitoringRuleMaxSignalDuration"]
    ONE_HOUR: ClassVar["SecurityMonitoringRuleMaxSignalDuration"]
    TWO_HOURS: ClassVar["SecurityMonitoringRuleMaxSignalDuration"]
    THREE_HOURS: ClassVar["SecurityMonitoringRuleMaxSignalDuration"]
    SIX_HOURS: ClassVar["SecurityMonitoringRuleMaxSignalDuration"]
    TWELVE_HOURS: ClassVar["SecurityMonitoringRuleMaxSignalDuration"]
    ONE_DAY: ClassVar["SecurityMonitoringRuleMaxSignalDuration"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (int,),
        }


SecurityMonitoringRuleMaxSignalDuration.ZERO_MINUTES = SecurityMonitoringRuleMaxSignalDuration(0)
SecurityMonitoringRuleMaxSignalDuration.ONE_MINUTE = SecurityMonitoringRuleMaxSignalDuration(60)
SecurityMonitoringRuleMaxSignalDuration.FIVE_MINUTES = SecurityMonitoringRuleMaxSignalDuration(300)
SecurityMonitoringRuleMaxSignalDuration.TEN_MINUTES = SecurityMonitoringRuleMaxSignalDuration(600)
SecurityMonitoringRuleMaxSignalDuration.FIFTEEN_MINUTES = SecurityMonitoringRuleMaxSignalDuration(900)
SecurityMonitoringRuleMaxSignalDuration.THIRTY_MINUTES = SecurityMonitoringRuleMaxSignalDuration(1800)
SecurityMonitoringRuleMaxSignalDuration.ONE_HOUR = SecurityMonitoringRuleMaxSignalDuration(3600)
SecurityMonitoringRuleMaxSignalDuration.TWO_HOURS = SecurityMonitoringRuleMaxSignalDuration(7200)
SecurityMonitoringRuleMaxSignalDuration.THREE_HOURS = SecurityMonitoringRuleMaxSignalDuration(10800)
SecurityMonitoringRuleMaxSignalDuration.SIX_HOURS = SecurityMonitoringRuleMaxSignalDuration(21600)
SecurityMonitoringRuleMaxSignalDuration.TWELVE_HOURS = SecurityMonitoringRuleMaxSignalDuration(43200)
SecurityMonitoringRuleMaxSignalDuration.ONE_DAY = SecurityMonitoringRuleMaxSignalDuration(86400)
