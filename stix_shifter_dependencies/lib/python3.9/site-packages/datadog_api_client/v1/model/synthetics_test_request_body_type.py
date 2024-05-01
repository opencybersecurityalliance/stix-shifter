# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsTestRequestBodyType(ModelSimple):
    """
    Type of the request body.

    :param value: Must be one of ["text/plain", "application/json", "text/xml", "text/html", "application/x-www-form-urlencoded", "graphql"].
    :type value: str
    """

    allowed_values = {
        "text/plain",
        "application/json",
        "text/xml",
        "text/html",
        "application/x-www-form-urlencoded",
        "graphql",
    }
    TEXT_PLAIN: ClassVar["SyntheticsTestRequestBodyType"]
    APPLICATION_JSON: ClassVar["SyntheticsTestRequestBodyType"]
    TEXT_XML: ClassVar["SyntheticsTestRequestBodyType"]
    TEXT_HTML: ClassVar["SyntheticsTestRequestBodyType"]
    APPLICATION_X_WWW_FORM_URLENCODED: ClassVar["SyntheticsTestRequestBodyType"]
    GRAPHQL: ClassVar["SyntheticsTestRequestBodyType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsTestRequestBodyType.TEXT_PLAIN = SyntheticsTestRequestBodyType("text/plain")
SyntheticsTestRequestBodyType.APPLICATION_JSON = SyntheticsTestRequestBodyType("application/json")
SyntheticsTestRequestBodyType.TEXT_XML = SyntheticsTestRequestBodyType("text/xml")
SyntheticsTestRequestBodyType.TEXT_HTML = SyntheticsTestRequestBodyType("text/html")
SyntheticsTestRequestBodyType.APPLICATION_X_WWW_FORM_URLENCODED = SyntheticsTestRequestBodyType(
    "application/x-www-form-urlencoded"
)
SyntheticsTestRequestBodyType.GRAPHQL = SyntheticsTestRequestBodyType("graphql")
