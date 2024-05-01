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
    from datadog_api_client.v2.model.user_attributes import UserAttributes
    from datadog_api_client.v2.model.user_response_relationships import UserResponseRelationships
    from datadog_api_client.v2.model.users_type import UsersType


class User(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.user_attributes import UserAttributes
        from datadog_api_client.v2.model.user_response_relationships import UserResponseRelationships
        from datadog_api_client.v2.model.users_type import UsersType

        return {
            "attributes": (UserAttributes,),
            "id": (str,),
            "relationships": (UserResponseRelationships,),
            "type": (UsersType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[UserAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        relationships: Union[UserResponseRelationships, UnsetType] = unset,
        type: Union[UsersType, UnsetType] = unset,
        **kwargs,
    ):
        """
        User object returned by the API.

        :param attributes: Attributes of user object returned by the API.
        :type attributes: UserAttributes, optional

        :param id: ID of the user.
        :type id: str, optional

        :param relationships: Relationships of the user object returned by the API.
        :type relationships: UserResponseRelationships, optional

        :param type: Users resource type.
        :type type: UsersType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if relationships is not unset:
            kwargs["relationships"] = relationships
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
