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
    from datadog_api_client.v2.model.permission_attributes import PermissionAttributes
    from datadog_api_client.v2.model.permissions_type import PermissionsType


class Permission(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.permission_attributes import PermissionAttributes
        from datadog_api_client.v2.model.permissions_type import PermissionsType

        return {
            "attributes": (PermissionAttributes,),
            "id": (str,),
            "type": (PermissionsType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        type: PermissionsType,
        attributes: Union[PermissionAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Permission object.

        :param attributes: Attributes of a permission.
        :type attributes: PermissionAttributes, optional

        :param id: ID of the permission.
        :type id: str, optional

        :param type: Permissions resource type.
        :type type: PermissionsType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        super().__init__(kwargs)

        self_.type = type
