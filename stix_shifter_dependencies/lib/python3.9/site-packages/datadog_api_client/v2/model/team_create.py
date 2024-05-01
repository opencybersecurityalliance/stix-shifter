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
    from datadog_api_client.v2.model.team_create_attributes import TeamCreateAttributes
    from datadog_api_client.v2.model.team_create_relationships import TeamCreateRelationships
    from datadog_api_client.v2.model.team_type import TeamType


class TeamCreate(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.team_create_attributes import TeamCreateAttributes
        from datadog_api_client.v2.model.team_create_relationships import TeamCreateRelationships
        from datadog_api_client.v2.model.team_type import TeamType

        return {
            "attributes": (TeamCreateAttributes,),
            "relationships": (TeamCreateRelationships,),
            "type": (TeamType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: TeamCreateAttributes,
        type: TeamType,
        relationships: Union[TeamCreateRelationships, UnsetType] = unset,
        **kwargs,
    ):
        """
        Team create

        :param attributes: Team creation attributes
        :type attributes: TeamCreateAttributes

        :param relationships: Relationships formed with the team on creation
        :type relationships: TeamCreateRelationships, optional

        :param type: Team type
        :type type: TeamType
        """
        if relationships is not unset:
            kwargs["relationships"] = relationships
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
