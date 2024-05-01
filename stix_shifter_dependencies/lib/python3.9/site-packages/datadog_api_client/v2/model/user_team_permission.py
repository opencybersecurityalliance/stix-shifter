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
    from datadog_api_client.v2.model.user_team_permission_attributes import UserTeamPermissionAttributes
    from datadog_api_client.v2.model.user_team_permission_type import UserTeamPermissionType


class UserTeamPermission(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.user_team_permission_attributes import UserTeamPermissionAttributes
        from datadog_api_client.v2.model.user_team_permission_type import UserTeamPermissionType

        return {
            "attributes": (UserTeamPermissionAttributes,),
            "id": (str,),
            "type": (UserTeamPermissionType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        id: str,
        type: UserTeamPermissionType,
        attributes: Union[UserTeamPermissionAttributes, UnsetType] = unset,
        **kwargs,
    ):
        """
        A user's permissions for a given team

        :param attributes: User team permission attributes
        :type attributes: UserTeamPermissionAttributes, optional

        :param id: The user team permission's identifier
        :type id: str

        :param type: User team permission type
        :type type: UserTeamPermissionType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        super().__init__(kwargs)

        self_.id = id
        self_.type = type
