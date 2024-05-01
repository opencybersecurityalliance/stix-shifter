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
    from datadog_api_client.v2.model.team_update_attributes import TeamUpdateAttributes
    from datadog_api_client.v2.model.team_update_relationships import TeamUpdateRelationships
    from datadog_api_client.v2.model.team_type import TeamType


class TeamUpdate(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.team_update_attributes import TeamUpdateAttributes
        from datadog_api_client.v2.model.team_update_relationships import TeamUpdateRelationships
        from datadog_api_client.v2.model.team_type import TeamType

        return {
            "attributes": (TeamUpdateAttributes,),
            "relationships": (TeamUpdateRelationships,),
            "type": (TeamType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: TeamUpdateAttributes,
        type: TeamType,
        relationships: Union[TeamUpdateRelationships, UnsetType] = unset,
        **kwargs,
    ):
        """
        Team update request

        :param attributes: Team update attributes
        :type attributes: TeamUpdateAttributes

        :param relationships: Team update relationships
        :type relationships: TeamUpdateRelationships, optional

        :param type: Team type
        :type type: TeamType
        """
        if relationships is not unset:
            kwargs["relationships"] = relationships
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
