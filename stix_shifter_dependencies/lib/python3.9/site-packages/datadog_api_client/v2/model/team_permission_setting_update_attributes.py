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
    from datadog_api_client.v2.model.team_permission_setting_value import TeamPermissionSettingValue


class TeamPermissionSettingUpdateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.team_permission_setting_value import TeamPermissionSettingValue

        return {
            "value": (TeamPermissionSettingValue,),
        }

    attribute_map = {
        "value": "value",
    }

    def __init__(self_, value: Union[TeamPermissionSettingValue, UnsetType] = unset, **kwargs):
        """
        Team permission setting update attributes

        :param value: What type of user is allowed to perform the specified action
        :type value: TeamPermissionSettingValue, optional
        """
        if value is not unset:
            kwargs["value"] = value
        super().__init__(kwargs)
