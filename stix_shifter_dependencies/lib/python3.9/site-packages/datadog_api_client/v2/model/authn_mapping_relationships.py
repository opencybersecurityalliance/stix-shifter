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
    from datadog_api_client.v2.model.relationship_to_role import RelationshipToRole
    from datadog_api_client.v2.model.relationship_to_saml_assertion_attribute import (
        RelationshipToSAMLAssertionAttribute,
    )


class AuthNMappingRelationships(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.relationship_to_role import RelationshipToRole
        from datadog_api_client.v2.model.relationship_to_saml_assertion_attribute import (
            RelationshipToSAMLAssertionAttribute,
        )

        return {
            "role": (RelationshipToRole,),
            "saml_assertion_attribute": (RelationshipToSAMLAssertionAttribute,),
        }

    attribute_map = {
        "role": "role",
        "saml_assertion_attribute": "saml_assertion_attribute",
    }

    def __init__(
        self_,
        role: Union[RelationshipToRole, UnsetType] = unset,
        saml_assertion_attribute: Union[RelationshipToSAMLAssertionAttribute, UnsetType] = unset,
        **kwargs,
    ):
        """
        All relationships associated with AuthN Mapping.

        :param role: Relationship to role.
        :type role: RelationshipToRole, optional

        :param saml_assertion_attribute: AuthN Mapping relationship to SAML Assertion Attribute.
        :type saml_assertion_attribute: RelationshipToSAMLAssertionAttribute, optional
        """
        if role is not unset:
            kwargs["role"] = role
        if saml_assertion_attribute is not unset:
            kwargs["saml_assertion_attribute"] = saml_assertion_attribute
        super().__init__(kwargs)
