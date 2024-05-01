# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class UserTeamPermissionType(ModelSimple):
    """
    User team permission type

    :param value: If omitted defaults to "user_team_permissions". Must be one of ["user_team_permissions"].
    :type value: str
    """

    allowed_values = {
        "user_team_permissions",
    }
    USER_TEAM_PERMISSIONS: ClassVar["UserTeamPermissionType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


UserTeamPermissionType.USER_TEAM_PERMISSIONS = UserTeamPermissionType("user_team_permissions")
