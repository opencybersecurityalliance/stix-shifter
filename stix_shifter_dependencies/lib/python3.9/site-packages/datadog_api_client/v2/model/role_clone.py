# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.role_clone_attributes import RoleCloneAttributes
    from datadog_api_client.v2.model.roles_type import RolesType


class RoleClone(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.role_clone_attributes import RoleCloneAttributes
        from datadog_api_client.v2.model.roles_type import RolesType

        return {
            "attributes": (RoleCloneAttributes,),
            "type": (RolesType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(self_, attributes: RoleCloneAttributes, type: RolesType, **kwargs):
        """
        Data for the clone role request.

        :param attributes: Attributes required to create a new role by cloning an existing one.
        :type attributes: RoleCloneAttributes

        :param type: Roles type.
        :type type: RolesType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
