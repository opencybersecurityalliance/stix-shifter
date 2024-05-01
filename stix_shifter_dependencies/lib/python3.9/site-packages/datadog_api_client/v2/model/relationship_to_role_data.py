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
    from datadog_api_client.v2.model.roles_type import RolesType


class RelationshipToRoleData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.roles_type import RolesType

        return {
            "id": (str,),
            "type": (RolesType,),
        }

    attribute_map = {
        "id": "id",
        "type": "type",
    }

    def __init__(self_, id: Union[str, UnsetType] = unset, type: Union[RolesType, UnsetType] = unset, **kwargs):
        """
        Relationship to role object.

        :param id: The unique identifier of the role.
        :type id: str, optional

        :param type: Roles type.
        :type type: RolesType, optional
        """
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
