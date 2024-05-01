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
    from datadog_api_client.v2.model.service_account_create_attributes import ServiceAccountCreateAttributes
    from datadog_api_client.v2.model.user_relationships import UserRelationships
    from datadog_api_client.v2.model.users_type import UsersType


class ServiceAccountCreateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.service_account_create_attributes import ServiceAccountCreateAttributes
        from datadog_api_client.v2.model.user_relationships import UserRelationships
        from datadog_api_client.v2.model.users_type import UsersType

        return {
            "attributes": (ServiceAccountCreateAttributes,),
            "relationships": (UserRelationships,),
            "type": (UsersType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: ServiceAccountCreateAttributes,
        type: UsersType,
        relationships: Union[UserRelationships, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object to create a service account User.

        :param attributes: Attributes of the created user.
        :type attributes: ServiceAccountCreateAttributes

        :param relationships: Relationships of the user object.
        :type relationships: UserRelationships, optional

        :param type: Users resource type.
        :type type: UsersType
        """
        if relationships is not unset:
            kwargs["relationships"] = relationships
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
