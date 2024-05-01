# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class TargetFormatType(ModelSimple):
    """
    If the `target_type` of the remapper is `attribute`, try to cast the value to a new specific type.
        If the cast is not possible, the original type is kept. `string`, `integer`, or `double` are the possible types.
        If the `target_type` is `tag`, this parameter may not be specified.

    :param value: Must be one of ["auto", "string", "integer", "double"].
    :type value: str
    """

    allowed_values = {
        "auto",
        "string",
        "integer",
        "double",
    }
    AUTO: ClassVar["TargetFormatType"]
    STRING: ClassVar["TargetFormatType"]
    INTEGER: ClassVar["TargetFormatType"]
    DOUBLE: ClassVar["TargetFormatType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


TargetFormatType.AUTO = TargetFormatType("auto")
TargetFormatType.STRING = TargetFormatType("string")
TargetFormatType.INTEGER = TargetFormatType("integer")
TargetFormatType.DOUBLE = TargetFormatType("double")
