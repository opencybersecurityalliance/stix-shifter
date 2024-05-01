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
    from datadog_api_client.v2.model.authn_mapping_create_attributes import AuthNMappingCreateAttributes
    from datadog_api_client.v2.model.authn_mapping_create_relationships import AuthNMappingCreateRelationships
    from datadog_api_client.v2.model.authn_mappings_type import AuthNMappingsType


class AuthNMappingCreateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.authn_mapping_create_attributes import AuthNMappingCreateAttributes
        from datadog_api_client.v2.model.authn_mapping_create_relationships import AuthNMappingCreateRelationships
        from datadog_api_client.v2.model.authn_mappings_type import AuthNMappingsType

        return {
            "attributes": (AuthNMappingCreateAttributes,),
            "relationships": (AuthNMappingCreateRelationships,),
            "type": (AuthNMappingsType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "relationships": "relationships",
        "type": "type",
    }

    def __init__(
        self_,
        type: AuthNMappingsType,
        attributes: Union[AuthNMappingCreateAttributes, UnsetType] = unset,
        relationships: Union[AuthNMappingCreateRelationships, UnsetType] = unset,
        **kwargs,
    ):
        """
        Data for creating an AuthN Mapping.

        :param attributes: Key/Value pair of attributes used for create request.
        :type attributes: AuthNMappingCreateAttributes, optional

        :param relationships: Relationship of AuthN Mapping create object to Role.
        :type relationships: AuthNMappingCreateRelationships, optional

        :param type: AuthN Mappings resource type.
        :type type: AuthNMappingsType
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if relationships is not unset:
            kwargs["relationships"] = relationships
        super().__init__(kwargs)

        self_.type = type
