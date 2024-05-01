# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.synthetics_global_variable_attributes import SyntheticsGlobalVariableAttributes
    from datadog_api_client.v1.model.synthetics_global_variable_parse_test_options import (
        SyntheticsGlobalVariableParseTestOptions,
    )
    from datadog_api_client.v1.model.synthetics_global_variable_value import SyntheticsGlobalVariableValue


class SyntheticsGlobalVariable(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_global_variable_attributes import SyntheticsGlobalVariableAttributes
        from datadog_api_client.v1.model.synthetics_global_variable_parse_test_options import (
            SyntheticsGlobalVariableParseTestOptions,
        )
        from datadog_api_client.v1.model.synthetics_global_variable_value import SyntheticsGlobalVariableValue

        return {
            "attributes": (SyntheticsGlobalVariableAttributes,),
            "description": (str,),
            "id": (str,),
            "name": (str,),
            "parse_test_options": (SyntheticsGlobalVariableParseTestOptions,),
            "parse_test_public_id": (str,),
            "tags": ([str],),
            "value": (SyntheticsGlobalVariableValue,),
        }

    attribute_map = {
        "attributes": "attributes",
        "description": "description",
        "id": "id",
        "name": "name",
        "parse_test_options": "parse_test_options",
        "parse_test_public_id": "parse_test_public_id",
        "tags": "tags",
        "value": "value",
    }
    read_only_vars = {
        "id",
    }

    def __init__(
        self_,
        description: str,
        name: str,
        tags: List[str],
        value: SyntheticsGlobalVariableValue,
        attributes: Union[SyntheticsGlobalVariableAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        parse_test_options: Union[SyntheticsGlobalVariableParseTestOptions, UnsetType] = unset,
        parse_test_public_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Synthetics global variable.

        :param attributes: Attributes of the global variable.
        :type attributes: SyntheticsGlobalVariableAttributes, optional

        :param description: Description of the global variable.
        :type description: str

        :param id: Unique identifier of the global variable.
        :type id: str, optional

        :param name: Name of the global variable. Unique across Synthetics global variables.
        :type name: str

        :param parse_test_options: Parser options to use for retrieving a Synthetics global variable from a Synthetics Test. Used in conjunction with ``parse_test_public_id``.
        :type parse_test_options: SyntheticsGlobalVariableParseTestOptions, optional

        :param parse_test_public_id: A Synthetic test ID to use as a test to generate the variable value.
        :type parse_test_public_id: str, optional

        :param tags: Tags of the global variable.
        :type tags: [str]

        :param value: Value of the global variable.
        :type value: SyntheticsGlobalVariableValue
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if parse_test_options is not unset:
            kwargs["parse_test_options"] = parse_test_options
        if parse_test_public_id is not unset:
            kwargs["parse_test_public_id"] = parse_test_public_id
        super().__init__(kwargs)

        self_.description = description
        self_.name = name
        self_.tags = tags
        self_.value = value
