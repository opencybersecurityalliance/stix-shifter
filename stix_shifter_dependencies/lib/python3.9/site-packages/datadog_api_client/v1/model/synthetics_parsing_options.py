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
    from datadog_api_client.v1.model.synthetics_variable_parser import SyntheticsVariableParser
    from datadog_api_client.v1.model.synthetics_global_variable_parse_test_options_type import (
        SyntheticsGlobalVariableParseTestOptionsType,
    )


class SyntheticsParsingOptions(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_variable_parser import SyntheticsVariableParser
        from datadog_api_client.v1.model.synthetics_global_variable_parse_test_options_type import (
            SyntheticsGlobalVariableParseTestOptionsType,
        )

        return {
            "field": (str,),
            "name": (str,),
            "parser": (SyntheticsVariableParser,),
            "type": (SyntheticsGlobalVariableParseTestOptionsType,),
        }

    attribute_map = {
        "field": "field",
        "name": "name",
        "parser": "parser",
        "type": "type",
    }

    def __init__(
        self_,
        field: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        parser: Union[SyntheticsVariableParser, UnsetType] = unset,
        type: Union[SyntheticsGlobalVariableParseTestOptionsType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Parsing options for variables to extract.

        :param field: When type is ``http_header`` , name of the header to use to extract the value.
        :type field: str, optional

        :param name: Name of the variable to extract.
        :type name: str, optional

        :param parser: Details of the parser to use for the global variable.
        :type parser: SyntheticsVariableParser, optional

        :param type: Property of the Synthetics Test Response to use for a Synthetics global variable.
        :type type: SyntheticsGlobalVariableParseTestOptionsType, optional
        """
        if field is not unset:
            kwargs["field"] = field
        if name is not unset:
            kwargs["name"] = name
        if parser is not unset:
            kwargs["parser"] = parser
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
