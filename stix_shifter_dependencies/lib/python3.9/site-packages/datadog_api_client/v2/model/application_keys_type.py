# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ApplicationKeysType(ModelSimple):
    """
    Application Keys resource type.

    :param value: If omitted defaults to "application_keys". Must be one of ["application_keys"].
    :type value: str
    """

    allowed_values = {
        "application_keys",
    }
    APPLICATION_KEYS: ClassVar["ApplicationKeysType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ApplicationKeysType.APPLICATION_KEYS = ApplicationKeysType("application_keys")
