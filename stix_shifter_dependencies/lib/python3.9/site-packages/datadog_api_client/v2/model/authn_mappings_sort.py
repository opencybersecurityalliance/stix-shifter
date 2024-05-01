# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class AuthNMappingsSort(ModelSimple):
    """
    Sorting options for AuthN Mappings.

    :param value: Must be one of ["created_at", "-created_at", "role_id", "-role_id", "saml_assertion_attribute_id", "-saml_assertion_attribute_id", "role.name", "-role.name", "saml_assertion_attribute.attribute_key", "-saml_assertion_attribute.attribute_key", "saml_assertion_attribute.attribute_value", "-saml_assertion_attribute.attribute_value"].
    :type value: str
    """

    allowed_values = {
        "created_at",
        "-created_at",
        "role_id",
        "-role_id",
        "saml_assertion_attribute_id",
        "-saml_assertion_attribute_id",
        "role.name",
        "-role.name",
        "saml_assertion_attribute.attribute_key",
        "-saml_assertion_attribute.attribute_key",
        "saml_assertion_attribute.attribute_value",
        "-saml_assertion_attribute.attribute_value",
    }
    CREATED_AT_ASCENDING: ClassVar["AuthNMappingsSort"]
    CREATED_AT_DESCENDING: ClassVar["AuthNMappingsSort"]
    ROLE_ID_ASCENDING: ClassVar["AuthNMappingsSort"]
    ROLE_ID_DESCENDING: ClassVar["AuthNMappingsSort"]
    SAML_ASSERTION_ATTRIBUTE_ID_ASCENDING: ClassVar["AuthNMappingsSort"]
    SAML_ASSERTION_ATTRIBUTE_ID_DESCENDING: ClassVar["AuthNMappingsSort"]
    ROLE_NAME_ASCENDING: ClassVar["AuthNMappingsSort"]
    ROLE_NAME_DESCENDING: ClassVar["AuthNMappingsSort"]
    SAML_ASSERTION_ATTRIBUTE_KEY_ASCENDING: ClassVar["AuthNMappingsSort"]
    SAML_ASSERTION_ATTRIBUTE_KEY_DESCENDING: ClassVar["AuthNMappingsSort"]
    SAML_ASSERTION_ATTRIBUTE_VALUE_ASCENDING: ClassVar["AuthNMappingsSort"]
    SAML_ASSERTION_ATTRIBUTE_VALUE_DESCENDING: ClassVar["AuthNMappingsSort"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


AuthNMappingsSort.CREATED_AT_ASCENDING = AuthNMappingsSort("created_at")
AuthNMappingsSort.CREATED_AT_DESCENDING = AuthNMappingsSort("-created_at")
AuthNMappingsSort.ROLE_ID_ASCENDING = AuthNMappingsSort("role_id")
AuthNMappingsSort.ROLE_ID_DESCENDING = AuthNMappingsSort("-role_id")
AuthNMappingsSort.SAML_ASSERTION_ATTRIBUTE_ID_ASCENDING = AuthNMappingsSort("saml_assertion_attribute_id")
AuthNMappingsSort.SAML_ASSERTION_ATTRIBUTE_ID_DESCENDING = AuthNMappingsSort("-saml_assertion_attribute_id")
AuthNMappingsSort.ROLE_NAME_ASCENDING = AuthNMappingsSort("role.name")
AuthNMappingsSort.ROLE_NAME_DESCENDING = AuthNMappingsSort("-role.name")
AuthNMappingsSort.SAML_ASSERTION_ATTRIBUTE_KEY_ASCENDING = AuthNMappingsSort("saml_assertion_attribute.attribute_key")
AuthNMappingsSort.SAML_ASSERTION_ATTRIBUTE_KEY_DESCENDING = AuthNMappingsSort("-saml_assertion_attribute.attribute_key")
AuthNMappingsSort.SAML_ASSERTION_ATTRIBUTE_VALUE_ASCENDING = AuthNMappingsSort(
    "saml_assertion_attribute.attribute_value"
)
AuthNMappingsSort.SAML_ASSERTION_ATTRIBUTE_VALUE_DESCENDING = AuthNMappingsSort(
    "-saml_assertion_attribute.attribute_value"
)
