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
    from datadog_api_client.v2.model.team_attributes import TeamAttributes
    from datadog_api_client.v2.model.team_relationships import TeamRelationships
    from datadog_api_client.v2.model.team_type import TeamType


class Team(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.team_attributes import TeamAttributes
        from datadog_api_client.v2.model.team_relationships import TeamRelationships
        from datadog_api_client.v2.model.team_type import TeamType

        return {
            "attributes": (TeamAttributes,),
            "id": (str,),
            "relationships": (TeamRelationships,),
            "type": (TeamType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: TeamAttributes,
        id: str,
        type: TeamType,
        relationships: Union[TeamRelationships, UnsetType] = unset,
        **kwargs,
    ):
        """
        A team

        :param attributes: Team attributes
        :type attributes: TeamAttributes

        :param id: The team's identifier
        :type id: str

        :param relationships: Resources related to a team
        :type relationships: TeamRelationships, optional

        :param type: Team type
        :type type: TeamType
        """
        if relationships is not unset:
            kwargs["relationships"] = relationships
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.type = type
