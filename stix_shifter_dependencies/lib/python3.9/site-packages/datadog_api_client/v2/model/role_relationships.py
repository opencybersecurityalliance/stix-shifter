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
    from datadog_api_client.v2.model.relationship_to_permissions import RelationshipToPermissions
    from datadog_api_client.v2.model.relationship_to_users import RelationshipToUsers


class RoleRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.relationship_to_permissions import RelationshipToPermissions
        from datadog_api_client.v2.model.relationship_to_users import RelationshipToUsers

        return {
            "permissions": (RelationshipToPermissions,),
            "users": (RelationshipToUsers,),
        }

    attribute_map = {
        "permissions": "permissions",
        "users": "users",
    }

    def __init__(
        self_,
        permissions: Union[RelationshipToPermissions, UnsetType] = unset,
        users: Union[RelationshipToUsers, UnsetType] = unset,
        **kwargs,
    ):
        """
        Relationships of the role object.

        :param permissions: Relationship to multiple permissions objects.
        :type permissions: RelationshipToPermissions, optional

        :param users: Relationship to users.
        :type users: RelationshipToUsers, optional
        """
        if permissions is not unset:
            kwargs["permissions"] = permissions
        if users is not unset:
            kwargs["users"] = users
        super().__init__(kwargs)
