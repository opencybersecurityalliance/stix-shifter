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
    from datadog_api_client.v2.model.user_team_attributes import UserTeamAttributes
    from datadog_api_client.v2.model.user_team_type import UserTeamType


class UserTeamUpdate(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.user_team_attributes import UserTeamAttributes
        from datadog_api_client.v2.model.user_team_type import UserTeamType

        return {
            "attributes": (UserTeamAttributes,),
            "type": (UserTeamType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(self_, type: UserTeamType, attributes: Union[UserTeamAttributes, UnsetType] = unset, **kwargs):
        """
        A user's relationship with a team

        :param attributes: Team membership attributes
        :type attributes: UserTeamAttributes, optional

        :param type: Team membership type
        :type type: UserTeamType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        super().__init__(kwargs)

        self_.type = type
