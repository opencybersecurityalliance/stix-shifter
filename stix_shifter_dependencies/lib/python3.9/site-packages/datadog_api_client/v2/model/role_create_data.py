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
    from datadog_api_client.v2.model.role_create_attributes import RoleCreateAttributes
    from datadog_api_client.v2.model.role_relationships import RoleRelationships
    from datadog_api_client.v2.model.roles_type import RolesType


class RoleCreateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.role_create_attributes import RoleCreateAttributes
        from datadog_api_client.v2.model.role_relationships import RoleRelationships
        from datadog_api_client.v2.model.roles_type import RolesType

        return {
            "attributes": (RoleCreateAttributes,),
            "relationships": (RoleRelationships,),
            "type": (RolesType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: RoleCreateAttributes,
        relationships: Union[RoleRelationships, UnsetType] = unset,
        type: Union[RolesType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Data related to the creation of a role.

        :param attributes: Attributes of the created role.
        :type attributes: RoleCreateAttributes

        :param relationships: Relationships of the role object.
        :type relationships: RoleRelationships, optional

        :param type: Roles type.
        :type type: RolesType, optional
        """
        if relationships is not unset:
            kwargs["relationships"] = relationships
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)

        self_.attributes = attributes
