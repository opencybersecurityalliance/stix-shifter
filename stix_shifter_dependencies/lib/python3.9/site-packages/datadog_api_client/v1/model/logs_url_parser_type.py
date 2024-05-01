# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class LogsURLParserType(ModelSimple):
    """
    Type of logs URL parser.

    :param value: If omitted defaults to "url-parser". Must be one of ["url-parser"].
    :type value: str
    """

    allowed_values = {
        "url-parser",
    }
    URL_PARSER: ClassVar["LogsURLParserType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


LogsURLParserType.URL_PARSER = LogsURLParserType("url-parser")
