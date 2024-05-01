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


class RoleResponseRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.relationship_to_permissions import RelationshipToPermissions

        return {
            "permissions": (RelationshipToPermissions,),
        }

    attribute_map = {
        "permissions": "permissions",
    }

    def __init__(self_, permissions: Union[RelationshipToPermissions, UnsetType] = unset, **kwargs):
        """
        Relationships of the role object returned by the API.

        :param permissions: Relationship to multiple permissions objects.
        :type permissions: RelationshipToPermissions, optional
        """
        if permissions is not unset:
            kwargs["permissions"] = permissions
        super().__init__(kwargs)
