# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.security_monitoring_triage_user import SecurityMonitoringTriageUser


class SecurityMonitoringSignalAssigneeUpdateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_triage_user import SecurityMonitoringTriageUser

        return {
            "assignee": (SecurityMonitoringTriageUser,),
            "version": (int,),
        }

    attribute_map = {
        "assignee": "assignee",
        "version": "version",
    }

    def __init__(self_, assignee: SecurityMonitoringTriageUser, version: Union[int, UnsetType] = unset, **kwargs):
        """
        Attributes describing the new assignee of a security signal.

        :param assignee: Object representing a given user entity.
        :type assignee: SecurityMonitoringTriageUser

        :param version: Version of the updated signal. If server side version is higher, update will be rejected.
        :type version: int, optional
        """
        if version is not unset:
            kwargs["version"] = version
        super().__init__(kwargs)

        self_.assignee = assignee
