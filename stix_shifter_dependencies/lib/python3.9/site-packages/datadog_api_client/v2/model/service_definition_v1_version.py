# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class ServiceDefinitionV1Version(ModelSimple):
    """
    Schema version being used.

    :param value: If omitted defaults to "v1". Must be one of ["v1"].
    :type value: str
    """

    allowed_values = {
        "v1",
    }
    V1: ClassVar["ServiceDefinitionV1Version"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


ServiceDefinitionV1Version.V1 = ServiceDefinitionV1Version("v1")
