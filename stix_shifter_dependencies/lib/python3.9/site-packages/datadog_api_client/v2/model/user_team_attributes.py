# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.user_team_role import UserTeamRole


class UserTeamAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.user_team_role import UserTeamRole

        return {
            "role": (UserTeamRole,),
        }

    attribute_map = {
        "role": "role",
    }

    def __init__(self_, role: Union[UserTeamRole, none_type, UnsetType] = unset, **kwargs):
        """
        Team membership attributes

        :param role: The user's role within the team
        :type role: UserTeamRole, none_type, optional
        """
        if role is not unset:
            kwargs["role"] = role
        super().__init__(kwargs)
