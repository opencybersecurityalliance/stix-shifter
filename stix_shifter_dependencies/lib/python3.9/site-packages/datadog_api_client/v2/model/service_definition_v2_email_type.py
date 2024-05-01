# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ServiceDefinitionV2EmailType(ModelSimple):
    """
    Contact type.

    :param value: If omitted defaults to "email". Must be one of ["email"].
    :type value: str
    """

    allowed_values = {
        "email",
    }
    EMAIL: ClassVar["ServiceDefinitionV2EmailType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ServiceDefinitionV2EmailType.EMAIL = ServiceDefinitionV2EmailType("email")
