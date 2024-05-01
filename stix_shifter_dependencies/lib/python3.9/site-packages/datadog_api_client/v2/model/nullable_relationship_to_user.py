# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.nullable_relationship_to_user_data import NullableRelationshipToUserData


class NullableRelationshipToUser(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.nullable_relationship_to_user_data import NullableRelationshipToUserData

        return {
            "data": (NullableRelationshipToUserData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: Union[NullableRelationshipToUserData, none_type], **kwargs):
        """
        Relationship to user.

        :param data: Relationship to user object.
        :type data: NullableRelationshipToUserData, none_type
        """
        super().__init__(kwargs)

        self_.data = data
