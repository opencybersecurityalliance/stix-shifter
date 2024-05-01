# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.synthetics_global_variable_parser_type import SyntheticsGlobalVariableParserType


class SyntheticsVariableParser(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_global_variable_parser_type import (
            SyntheticsGlobalVariableParserType,
        )

        return {
            "type": (SyntheticsGlobalVariableParserType,),
            "value": (str,),
        }

    attribute_map = {
        "type": "type",
        "value": "value",
    }

    def __init__(self_, type: SyntheticsGlobalVariableParserType, value: Union[str, UnsetType] = unset, **kwargs):
        """
        Details of the parser to use for the global variable.

        :param type: Type of parser for a Synthetics global variable from a synthetics test.
        :type type: SyntheticsGlobalVariableParserType

        :param value: Regex or JSON path used for the parser. Not used with type ``raw``.
        :type value: str, optional
        """
        if value is not unset:
            kwargs["value"] = value
        super().__init__(kwargs)

        self_.type = type
