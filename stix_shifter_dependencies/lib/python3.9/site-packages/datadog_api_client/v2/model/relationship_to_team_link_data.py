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
    from datadog_api_client.v2.model.team_link_type import TeamLinkType


class RelationshipToTeamLinkData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.team_link_type import TeamLinkType

        return {
            "id": (str,),
            "type": (TeamLinkType,),
        }

    attribute_map = {
        "id": "id",
        "type": "type",
    }

    def __init__(self_, id: str, type: TeamLinkType, **kwargs):
        """
        Relationship between a link and a team

        :param id: The team link's identifier
        :type id: str

        :param type: Team link type
        :type type: TeamLinkType
        """
        super().__init__(kwargs)

        self_.id = id
        self_.type = type
