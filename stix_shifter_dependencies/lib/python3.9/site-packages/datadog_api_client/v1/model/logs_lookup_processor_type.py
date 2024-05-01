# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsLookupProcessorType(ModelSimple):
    """
    Type of logs lookup processor.

    :param value: If omitted defaults to "lookup-processor". Must be one of ["lookup-processor"].
    :type value: str
    """

    allowed_values = {
        "lookup-processor",
    }
    LOOKUP_PROCESSOR: ClassVar["LogsLookupProcessorType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsLookupProcessorType.LOOKUP_PROCESSOR = LogsLookupProcessorType("lookup-processor")
