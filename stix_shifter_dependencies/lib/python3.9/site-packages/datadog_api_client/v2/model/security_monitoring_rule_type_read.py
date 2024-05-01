# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SecurityMonitoringRuleTypeRead(ModelSimple):
    """
    The rule type.

    :param value: Must be one of ["log_detection", "infrastructure_configuration", "workload_security", "cloud_configuration", "application_security"].
    :type value: str
    """

    allowed_values = {
        "log_detection",
        "infrastructure_configuration",
        "workload_security",
        "cloud_configuration",
        "application_security",
    }
    LOG_DETECTION: ClassVar["SecurityMonitoringRuleTypeRead"]
    INFRASTRUCTURE_CONFIGURATION: ClassVar["SecurityMonitoringRuleTypeRead"]
    WORKLOAD_SECURITY: ClassVar["SecurityMonitoringRuleTypeRead"]
    CLOUD_CONFIGURATION: ClassVar["SecurityMonitoringRuleTypeRead"]
    APPLICATION_SECURITY: ClassVar["SecurityMonitoringRuleTypeRead"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SecurityMonitoringRuleTypeRead.LOG_DETECTION = SecurityMonitoringRuleTypeRead("log_detection")
SecurityMonitoringRuleTypeRead.INFRASTRUCTURE_CONFIGURATION = SecurityMonitoringRuleTypeRead(
    "infrastructure_configuration"
)
SecurityMonitoringRuleTypeRead.WORKLOAD_SECURITY = SecurityMonitoringRuleTypeRead("workload_security")
SecurityMonitoringRuleTypeRead.CLOUD_CONFIGURATION = SecurityMonitoringRuleTypeRead("cloud_configuration")
SecurityMonitoringRuleTypeRead.APPLICATION_SECURITY = SecurityMonitoringRuleTypeRead("application_security")
