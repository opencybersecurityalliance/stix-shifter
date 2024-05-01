# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SecurityMonitoringRuleKeepAlive(ModelSimple):
    """
    Once a signal is generated, the signal will remain “open” if a case is matched at least once within
        this keep alive window.

    :param value: Must be one of [0, 60, 300, 600, 900, 1800, 3600, 7200, 10800, 21600].
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
    }
    ZERO_MINUTES: ClassVar["SecurityMonitoringRuleKeepAlive"]
    ONE_MINUTE: ClassVar["SecurityMonitoringRuleKeepAlive"]
    FIVE_MINUTES: ClassVar["SecurityMonitoringRuleKeepAlive"]
    TEN_MINUTES: ClassVar["SecurityMonitoringRuleKeepAlive"]
    FIFTEEN_MINUTES: ClassVar["SecurityMonitoringRuleKeepAlive"]
    THIRTY_MINUTES: ClassVar["SecurityMonitoringRuleKeepAlive"]
    ONE_HOUR: ClassVar["SecurityMonitoringRuleKeepAlive"]
    TWO_HOURS: ClassVar["SecurityMonitoringRuleKeepAlive"]
    THREE_HOURS: ClassVar["SecurityMonitoringRuleKeepAlive"]
    SIX_HOURS: ClassVar["SecurityMonitoringRuleKeepAlive"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (int,),
        }


SecurityMonitoringRuleKeepAlive.ZERO_MINUTES = SecurityMonitoringRuleKeepAlive(0)
SecurityMonitoringRuleKeepAlive.ONE_MINUTE = SecurityMonitoringRuleKeepAlive(60)
SecurityMonitoringRuleKeepAlive.FIVE_MINUTES = SecurityMonitoringRuleKeepAlive(300)
SecurityMonitoringRuleKeepAlive.TEN_MINUTES = SecurityMonitoringRuleKeepAlive(600)
SecurityMonitoringRuleKeepAlive.FIFTEEN_MINUTES = SecurityMonitoringRuleKeepAlive(900)
SecurityMonitoringRuleKeepAlive.THIRTY_MINUTES = SecurityMonitoringRuleKeepAlive(1800)
SecurityMonitoringRuleKeepAlive.ONE_HOUR = SecurityMonitoringRuleKeepAlive(3600)
SecurityMonitoringRuleKeepAlive.TWO_HOURS = SecurityMonitoringRuleKeepAlive(7200)
SecurityMonitoringRuleKeepAlive.THREE_HOURS = SecurityMonitoringRuleKeepAlive(10800)
SecurityMonitoringRuleKeepAlive.SIX_HOURS = SecurityMonitoringRuleKeepAlive(21600)
