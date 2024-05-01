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
    from datadog_api_client.v2.model.relationship_to_user import RelationshipToUser


class ApplicationKeyRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.relationship_to_user import RelationshipToUser

        return {
            "owned_by": (RelationshipToUser,),
        }

    attribute_map = {
        "owned_by": "owned_by",
    }

    def __init__(self_, owned_by: Union[RelationshipToUser, UnsetType] = unset, **kwargs):
        """
        Resources related to the application key.

        :param owned_by: Relationship to user.
        :type owned_by: RelationshipToUser, optional
        """
        if owned_by is not unset:
            kwargs["owned_by"] = owned_by
        super().__init__(kwargs)
