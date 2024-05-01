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
    from datadog_api_client.v2.model.team_permission_setting_update_attributes import (
        TeamPermissionSettingUpdateAttributes,
    )
    from datadog_api_client.v2.model.team_permission_setting_type import TeamPermissionSettingType


class TeamPermissionSettingUpdate(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.team_permission_setting_update_attributes import (
            TeamPermissionSettingUpdateAttributes,
        )
        from datadog_api_client.v2.model.team_permission_setting_type import TeamPermissionSettingType

        return {
            "attributes": (TeamPermissionSettingUpdateAttributes,),
            "type": (TeamPermissionSettingType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(
        self_,
        type: TeamPermissionSettingType,
        attributes: Union[TeamPermissionSettingUpdateAttributes, UnsetType] = unset,
        **kwargs,
    ):
        """
        Team permission setting update

        :param attributes: Team permission setting update attributes
        :type attributes: TeamPermissionSettingUpdateAttributes, optional

        :param type: Team permission setting type
        :type type: TeamPermissionSettingType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        super().__init__(kwargs)

        self_.type = type
