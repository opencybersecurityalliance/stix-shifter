# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsArithmeticProcessorType(ModelSimple):
    """
    Type of logs arithmetic processor.

    :param value: If omitted defaults to "arithmetic-processor". Must be one of ["arithmetic-processor"].
    :type value: str
    """

    allowed_values = {
        "arithmetic-processor",
    }
    ARITHMETIC_PROCESSOR: ClassVar["LogsArithmeticProcessorType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsArithmeticProcessorType.ARITHMETIC_PROCESSOR = LogsArithmeticProcessorType("arithmetic-processor")
