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
    from datadog_api_client.v2.model.user_team_user_type import UserTeamUserType


class RelationshipToUserTeamUserData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.user_team_user_type import UserTeamUserType

        return {
            "id": (str,),
            "type": (UserTeamUserType,),
        }

    attribute_map = {
        "id": "id",
        "type": "type",
    }

    def __init__(self_, id: str, type: UserTeamUserType, **kwargs):
        """
        A user's relationship with a team

        :param id: The ID of the user associated with the team
        :type id: str

        :param type: User team user type
        :type type: UserTeamUserType
        """
        super().__init__(kwargs)

        self_.id = id
        self_.type = type
