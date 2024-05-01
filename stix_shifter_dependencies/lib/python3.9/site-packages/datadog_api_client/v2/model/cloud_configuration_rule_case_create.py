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


class CloudConfigurationRuleCaseCreate(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_rule_severity import SecurityMonitoringRuleSeverity

        return {
            "notifications": ([str],),
            "status": (SecurityMonitoringRuleSeverity,),
        }

    attribute_map = {
        "notifications": "notifications",
        "status": "status",
    }

    def __init__(
        self_, status: SecurityMonitoringRuleSeverity, notifications: Union[List[str], UnsetType] = unset, **kwargs
    ):
        """
        Description of signals.

        :param notifications: Notification targets for each rule case.
        :type notifications: [str], optional

        :param status: Severity of the Security Signal.
        :type status: SecurityMonitoringRuleSeverity
        """
        if notifications is not unset:
            kwargs["notifications"] = notifications
        super().__init__(kwargs)

        self_.status = status
