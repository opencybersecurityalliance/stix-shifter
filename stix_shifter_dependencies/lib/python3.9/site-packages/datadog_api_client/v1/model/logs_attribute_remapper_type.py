# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsAttributeRemapperType(ModelSimple):
    """
    Type of logs attribute remapper.

    :param value: If omitted defaults to "attribute-remapper". Must be one of ["attribute-remapper"].
    :type value: str
    """

    allowed_values = {
        "attribute-remapper",
    }
    ATTRIBUTE_REMAPPER: ClassVar["LogsAttributeRemapperType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsAttributeRemapperType.ATTRIBUTE_REMAPPER = LogsAttributeRemapperType("attribute-remapper")
