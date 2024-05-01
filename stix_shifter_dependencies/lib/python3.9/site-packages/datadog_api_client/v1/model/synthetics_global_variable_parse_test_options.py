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


class SyntheticsGlobalVariableParseTestOptions(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_variable_parser import SyntheticsVariableParser
        from datadog_api_client.v1.model.synthetics_global_variable_parse_test_options_type import (
            SyntheticsGlobalVariableParseTestOptionsType,
        )

        return {
            "field": (str,),
            "local_variable_name": (str,),
            "parser": (SyntheticsVariableParser,),
            "type": (SyntheticsGlobalVariableParseTestOptionsType,),
        }

    attribute_map = {
        "field": "field",
        "local_variable_name": "localVariableName",
        "parser": "parser",
        "type": "type",
    }

    def __init__(
        self_,
        type: SyntheticsGlobalVariableParseTestOptionsType,
        field: Union[str, UnsetType] = unset,
        local_variable_name: Union[str, UnsetType] = unset,
        parser: Union[SyntheticsVariableParser, UnsetType] = unset,
        **kwargs,
    ):
        """
        Parser options to use for retrieving a Synthetics global variable from a Synthetics Test. Used in conjunction with ``parse_test_public_id``.

        :param field: When type is ``http_header`` , name of the header to use to extract the value.
        :type field: str, optional

        :param local_variable_name: When type is ``local_variable`` , name of the local variable to use to extract the value.
        :type local_variable_name: str, optional

        :param parser: Details of the parser to use for the global variable.
        :type parser: SyntheticsVariableParser, optional

        :param type: Property of the Synthetics Test Response to use for a Synthetics global variable.
        :type type: SyntheticsGlobalVariableParseTestOptionsType
        """
        if field is not unset:
            kwargs["field"] = field
        if local_variable_name is not unset:
            kwargs["local_variable_name"] = local_variable_name
        if parser is not unset:
            kwargs["parser"] = parser
        super().__init__(kwargs)

        self_.type = type
