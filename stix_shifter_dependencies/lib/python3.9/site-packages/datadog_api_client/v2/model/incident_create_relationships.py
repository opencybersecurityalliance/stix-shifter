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
    from datadog_api_client.v2.model.nullable_relationship_to_user import NullableRelationshipToUser


class IncidentCreateRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.nullable_relationship_to_user import NullableRelationshipToUser

        return {
            "commander_user": (NullableRelationshipToUser,),
        }

    attribute_map = {
        "commander_user": "commander_user",
    }

    def __init__(self_, commander_user: NullableRelationshipToUser, **kwargs):
        """
        The relationships the incident will have with other resources once created.

        :param commander_user: Relationship to user.
        :type commander_user: NullableRelationshipToUser
        """
        super().__init__(kwargs)

        self_.commander_user = commander_user
