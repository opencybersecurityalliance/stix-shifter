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
    from datadog_api_client.v2.model.relationship_to_user_team_permission import RelationshipToUserTeamPermission


class TeamRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.relationship_to_team_links import RelationshipToTeamLinks
        from datadog_api_client.v2.model.relationship_to_user_team_permission import RelationshipToUserTeamPermission

        return {
            "team_links": (RelationshipToTeamLinks,),
            "user_team_permissions": (RelationshipToUserTeamPermission,),
        }

    attribute_map = {
        "team_links": "team_links",
        "user_team_permissions": "user_team_permissions",
    }

    def __init__(
        self_,
        team_links: Union[RelationshipToTeamLinks, UnsetType] = unset,
        user_team_permissions: Union[RelationshipToUserTeamPermission, UnsetType] = unset,
        **kwargs,
    ):
        """
        Resources related to a team

        :param team_links: Relationship between a team and a team link
        :type team_links: RelationshipToTeamLinks, optional

        :param user_team_permissions: Relationship between a user team permission and a team
        :type user_team_permissions: RelationshipToUserTeamPermission, optional
        """
        if team_links is not unset:
            kwargs["team_links"] = team_links
        if user_team_permissions is not unset:
            kwargs["user_team_permissions"] = user_team_permissions
        super().__init__(kwargs)
