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
    from datadog_api_client.v2.model.partial_api_key_attributes import PartialAPIKeyAttributes
    from datadog_api_client.v2.model.api_key_relationships import APIKeyRelationships
    from datadog_api_client.v2.model.api_keys_type import APIKeysType


class PartialAPIKey(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.partial_api_key_attributes import PartialAPIKeyAttributes
        from datadog_api_client.v2.model.api_key_relationships import APIKeyRelationships
        from datadog_api_client.v2.model.api_keys_type import APIKeysType

        return {
            "attributes": (PartialAPIKeyAttributes,),
            "id": (str,),
            "relationships": (APIKeyRelationships,),
            "type": (APIKeysType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[PartialAPIKeyAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        relationships: Union[APIKeyRelationships, UnsetType] = unset,
        type: Union[APIKeysType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Partial Datadog API key.

        :param attributes: Attributes of a partial API key.
        :type attributes: PartialAPIKeyAttributes, optional

        :param id: ID of the API key.
        :type id: str, optional

        :param relationships: Resources related to the API key.
        :type relationships: APIKeyRelationships, optional

        :param type: API Keys resource type.
        :type type: APIKeysType, optional
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
