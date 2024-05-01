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
    from datadog_api_client.v2.model.relationship_to_users import RelationshipToUsers


class TeamCreateRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.relationship_to_users import RelationshipToUsers

        return {
            "users": (RelationshipToUsers,),
        }

    attribute_map = {
        "users": "users",
    }

    def __init__(self_, users: Union[RelationshipToUsers, UnsetType] = unset, **kwargs):
        """
        Relationships formed with the team on creation

        :param users: Relationship to users.
        :type users: RelationshipToUsers, optional
        """
        if users is not unset:
            kwargs["users"] = users
        super().__init__(kwargs)
