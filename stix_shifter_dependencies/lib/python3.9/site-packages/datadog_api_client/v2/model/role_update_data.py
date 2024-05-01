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
    from datadog_api_client.v2.model.role_update_attributes import RoleUpdateAttributes
    from datadog_api_client.v2.model.role_relationships import RoleRelationships
    from datadog_api_client.v2.model.roles_type import RolesType


class RoleUpdateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.role_update_attributes import RoleUpdateAttributes
        from datadog_api_client.v2.model.role_relationships import RoleRelationships
        from datadog_api_client.v2.model.roles_type import RolesType

        return {
            "attributes": (RoleUpdateAttributes,),
            "id": (str,),
            "relationships": (RoleRelationships,),
            "type": (RolesType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: RoleUpdateAttributes,
        id: str,
        type: RolesType,
        relationships: Union[RoleRelationships, UnsetType] = unset,
        **kwargs,
    ):
        """
        Data related to the update of a role.

        :param attributes: Attributes of the role.
        :type attributes: RoleUpdateAttributes

        :param id: The unique identifier of the role.
        :type id: str

        :param relationships: Relationships of the role object.
        :type relationships: RoleRelationships, optional

        :param type: Roles type.
        :type type: RolesType
        """
        if relationships is not unset:
            kwargs["relationships"] = relationships
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.type = type
