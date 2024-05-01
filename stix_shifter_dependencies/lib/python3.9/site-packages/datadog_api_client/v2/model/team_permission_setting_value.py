# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class TeamPermissionSettingValue(ModelSimple):
    """
    What type of user is allowed to perform the specified action

    :param value: Must be one of ["admins", "members", "organization", "user_access_manage", "teams_manage"].
    :type value: str
    """

    allowed_values = {
        "admins",
        "members",
        "organization",
        "user_access_manage",
        "teams_manage",
    }
    ADMINS: ClassVar["TeamPermissionSettingValue"]
    MEMBERS: ClassVar["TeamPermissionSettingValue"]
    ORGANIZATION: ClassVar["TeamPermissionSettingValue"]
    USER_ACCESS_MANAGE: ClassVar["TeamPermissionSettingValue"]
    TEAMS_MANAGE: ClassVar["TeamPermissionSettingValue"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


TeamPermissionSettingValue.ADMINS = TeamPermissionSettingValue("admins")
TeamPermissionSettingValue.MEMBERS = TeamPermissionSettingValue("members")
TeamPermissionSettingValue.ORGANIZATION = TeamPermissionSettingValue("organization")
TeamPermissionSettingValue.USER_ACCESS_MANAGE = TeamPermissionSettingValue("user_access_manage")
TeamPermissionSettingValue.TEAMS_MANAGE = TeamPermissionSettingValue("teams_manage")
