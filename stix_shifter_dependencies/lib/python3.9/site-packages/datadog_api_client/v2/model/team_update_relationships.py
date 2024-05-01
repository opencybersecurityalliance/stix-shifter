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
    from datadog_api_client.v2.model.relationship_to_team_links import RelationshipToTeamLinks


class TeamUpdateRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.relationship_to_team_links import RelationshipToTeamLinks

        return {
            "team_links": (RelationshipToTeamLinks,),
        }

    attribute_map = {
        "team_links": "team_links",
    }

    def __init__(self_, team_links: Union[RelationshipToTeamLinks, UnsetType] = unset, **kwargs):
        """
        Team update relationships

        :param team_links: Relationship between a team and a team link
        :type team_links: RelationshipToTeamLinks, optional
        """
        if team_links is not unset:
            kwargs["team_links"] = team_links
        super().__init__(kwargs)
