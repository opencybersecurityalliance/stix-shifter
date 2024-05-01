# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.user_team_permission_type import UserTeamPermissionType


class RelationshipToUserTeamPermissionData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.user_team_permission_type import UserTeamPermissionType

        return {
            "id": (str,),
            "type": (UserTeamPermissionType,),
        }

    attribute_map = {
        "id": "id",
        "type": "type",
    }

    def __init__(self_, id: str, type: UserTeamPermissionType, **kwargs):
        """
        Related user team permission data

        :param id: The ID of the user team permission
        :type id: str

        :param type: User team permission type
        :type type: UserTeamPermissionType
        """
        super().__init__(kwargs)

        self_.id = id
        self_.type = type
