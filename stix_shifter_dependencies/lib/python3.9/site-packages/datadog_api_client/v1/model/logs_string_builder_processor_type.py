# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsStringBuilderProcessorType(ModelSimple):
    """
    Type of logs string builder processor.

    :param value: If omitted defaults to "string-builder-processor". Must be one of ["string-builder-processor"].
    :type value: str
    """

    allowed_values = {
        "string-builder-processor",
    }
    STRING_BUILDER_PROCESSOR: ClassVar["LogsStringBuilderProcessorType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsStringBuilderProcessorType.STRING_BUILDER_PROCESSOR = LogsStringBuilderProcessorType("string-builder-processor")
