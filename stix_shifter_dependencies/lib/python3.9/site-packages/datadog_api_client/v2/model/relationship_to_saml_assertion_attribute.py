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
    from datadog_api_client.v2.model.relationship_to_saml_assertion_attribute_data import (
        RelationshipToSAMLAssertionAttributeData,
    )


class RelationshipToSAMLAssertionAttribute(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.relationship_to_saml_assertion_attribute_data import (
            RelationshipToSAMLAssertionAttributeData,
        )

        return {
            "data": (RelationshipToSAMLAssertionAttributeData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: RelationshipToSAMLAssertionAttributeData, **kwargs):
        """
        AuthN Mapping relationship to SAML Assertion Attribute.

        :param data: Data of AuthN Mapping relationship to SAML Assertion Attribute.
        :type data: RelationshipToSAMLAssertionAttributeData
        """
        super().__init__(kwargs)

        self_.data = data
