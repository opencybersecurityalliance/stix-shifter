# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SecurityMonitoringSignalRuleType(ModelSimple):
    """
    The rule type.

    :param value: If omitted defaults to "signal_correlation". Must be one of ["signal_correlation"].
    :type value: str
    """

    allowed_values = {
        "signal_correlation",
    }
    SIGNAL_CORRELATION: ClassVar["SecurityMonitoringSignalRuleType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SecurityMonitoringSignalRuleType.SIGNAL_CORRELATION = SecurityMonitoringSignalRuleType("signal_correlation")
