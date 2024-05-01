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
    from datadog_api_client.v2.model.team_permission_setting_serializer_action import (
        TeamPermissionSettingSerializerAction,
    )
    from datadog_api_client.v2.model.team_permission_setting_values import TeamPermissionSettingValues
    from datadog_api_client.v2.model.team_permission_setting_value import TeamPermissionSettingValue


class TeamPermissionSettingAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.team_permission_setting_serializer_action import (
            TeamPermissionSettingSerializerAction,
        )
        from datadog_api_client.v2.model.team_permission_setting_values import TeamPermissionSettingValues
        from datadog_api_client.v2.model.team_permission_setting_value import TeamPermissionSettingValue

        return {
            "action": (TeamPermissionSettingSerializerAction,),
            "editable": (bool,),
            "options": (TeamPermissionSettingValues,),
            "title": (str,),
            "value": (TeamPermissionSettingValue,),
        }

    attribute_map = {
        "action": "action",
        "editable": "editable",
        "options": "options",
        "title": "title",
        "value": "value",
    }
    read_only_vars = {
        "action",
        "editable",
        "options",
        "title",
    }

    def __init__(
        self_,
        action: Union[TeamPermissionSettingSerializerAction, UnsetType] = unset,
        editable: Union[bool, UnsetType] = unset,
        options: Union[TeamPermissionSettingValues, UnsetType] = unset,
        title: Union[str, UnsetType] = unset,
        value: Union[TeamPermissionSettingValue, UnsetType] = unset,
        **kwargs,
    ):
        """
        Team permission setting attributes

        :param action: The identifier for the action
        :type action: TeamPermissionSettingSerializerAction, optional

        :param editable: Whether or not the permission setting is editable by the current user
        :type editable: bool, optional

        :param options: Possible values for action
        :type options: TeamPermissionSettingValues, optional

        :param title: The team permission name
        :type title: str, optional

        :param value: What type of user is allowed to perform the specified action
        :type value: TeamPermissionSettingValue, optional
        """
        if action is not unset:
            kwargs["action"] = action
        if editable is not unset:
            kwargs["editable"] = editable
        if options is not unset:
            kwargs["options"] = options
        if title is not unset:
            kwargs["title"] = title
        if value is not unset:
            kwargs["value"] = value
        super().__init__(kwargs)
