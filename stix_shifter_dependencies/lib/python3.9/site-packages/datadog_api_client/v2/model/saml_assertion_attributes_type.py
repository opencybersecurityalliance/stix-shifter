# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SAMLAssertionAttributesType(ModelSimple):
    """
    SAML assertion attributes resource type.

    :param value: If omitted defaults to "saml_assertion_attributes". Must be one of ["saml_assertion_attributes"].
    :type value: str
    """

    allowed_values = {
        "saml_assertion_attributes",
    }
    SAML_ASSERTION_ATTRIBUTES: ClassVar["SAMLAssertionAttributesType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SAMLAssertionAttributesType.SAML_ASSERTION_ATTRIBUTES = SAMLAssertionAttributesType("saml_assertion_attributes")
