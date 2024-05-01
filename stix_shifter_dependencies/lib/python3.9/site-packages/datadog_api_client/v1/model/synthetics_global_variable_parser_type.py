# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class SyntheticsGlobalVariableParserType(ModelSimple):
    """
    Type of parser for a Synthetics global variable from a synthetics test.

    :param value: Must be one of ["raw", "json_path", "regex", "x_path"].
    :type value: str
    """

    allowed_values = {
        "raw",
        "json_path",
        "regex",
        "x_path",
    }
    RAW: ClassVar["SyntheticsGlobalVariableParserType"]
    JSON_PATH: ClassVar["SyntheticsGlobalVariableParserType"]
    REGEX: ClassVar["SyntheticsGlobalVariableParserType"]
    X_PATH: ClassVar["SyntheticsGlobalVariableParserType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


SyntheticsGlobalVariableParserType.RAW = SyntheticsGlobalVariableParserType("raw")
SyntheticsGlobalVariableParserType.JSON_PATH = SyntheticsGlobalVariableParserType("json_path")
SyntheticsGlobalVariableParserType.REGEX = SyntheticsGlobalVariableParserType("regex")
SyntheticsGlobalVariableParserType.X_PATH = SyntheticsGlobalVariableParserType("x_path")
