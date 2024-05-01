# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.security_monitoring_rule_severity import SecurityMonitoringRuleSeverity


class SecurityMonitoringRuleCaseCreate(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_rule_severity import SecurityMonitoringRuleSeverity

        return {
            "condition": (str,),
            "name": (str,),
            "notifications": ([str],),
            "status": (SecurityMonitoringRuleSeverity,),
        }

    attribute_map = {
        "condition": "condition",
        "name": "name",
        "notifications": "notifications",
        "status": "status",
    }

    def __init__(
        self_,
        status: SecurityMonitoringRuleSeverity,
        condition: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        notifications: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        Case when signal is generated.

        :param condition: A rule case contains logical operations ( ``>`` , ``>=`` , ``&&`` , ``||`` ) to determine if a signal should be generated
            based on the event counts in the previously defined queries.
        :type condition: str, optional

        :param name: Name of the case.
        :type name: str, optional

        :param notifications: Notification targets for each rule case.
        :type notifications: [str], optional

        :param status: Severity of the Security Signal.
        :type status: SecurityMonitoringRuleSeverity
        """
        if condition is not unset:
            kwargs["condition"] = condition
        if name is not unset:
            kwargs["name"] = name
        if notifications is not unset:
            kwargs["notifications"] = notifications
        super().__init__(kwargs)

        self_.status = status
