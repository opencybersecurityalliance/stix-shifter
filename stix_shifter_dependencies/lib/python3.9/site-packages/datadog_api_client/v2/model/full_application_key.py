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
    from datadog_api_client.v2.model.full_application_key_attributes import FullApplicationKeyAttributes
    from datadog_api_client.v2.model.application_key_relationships import ApplicationKeyRelationships
    from datadog_api_client.v2.model.application_keys_type import ApplicationKeysType


class FullApplicationKey(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.full_application_key_attributes import FullApplicationKeyAttributes
        from datadog_api_client.v2.model.application_key_relationships import ApplicationKeyRelationships
        from datadog_api_client.v2.model.application_keys_type import ApplicationKeysType

        return {
            "attributes": (FullApplicationKeyAttributes,),
            "id": (str,),
            "relationships": (ApplicationKeyRelationships,),
            "type": (ApplicationKeysType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[FullApplicationKeyAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        relationships: Union[ApplicationKeyRelationships, UnsetType] = unset,
        type: Union[ApplicationKeysType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Datadog application key.

        :param attributes: Attributes of a full application key.
        :type attributes: FullApplicationKeyAttributes, optional

        :param id: ID of the application key.
        :type id: str, optional

        :param relationships: Resources related to the application key.
        :type relationships: ApplicationKeyRelationships, optional

        :param type: Application Keys resource type.
        :type type: ApplicationKeysType, optional
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
