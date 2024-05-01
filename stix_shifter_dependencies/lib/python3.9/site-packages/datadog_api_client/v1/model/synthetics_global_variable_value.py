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
    from datadog_api_client.v1.model.synthetics_global_variable_options import SyntheticsGlobalVariableOptions


class SyntheticsGlobalVariableValue(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_global_variable_options import SyntheticsGlobalVariableOptions

        return {
            "options": (SyntheticsGlobalVariableOptions,),
            "secure": (bool,),
            "value": (str,),
        }

    attribute_map = {
        "options": "options",
        "secure": "secure",
        "value": "value",
    }

    def __init__(
        self_,
        options: Union[SyntheticsGlobalVariableOptions, UnsetType] = unset,
        secure: Union[bool, UnsetType] = unset,
        value: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Value of the global variable.

        :param options: Options for the Global Variable for MFA.
        :type options: SyntheticsGlobalVariableOptions, optional

        :param secure: Determines if the value of the variable is hidden.
        :type secure: bool, optional

        :param value: Value of the global variable. When reading a global variable,
            the value will not be present if the variable is hidden with the ``secure`` property.
        :type value: str, optional
        """
        if options is not unset:
            kwargs["options"] = options
        if secure is not unset:
            kwargs["secure"] = secure
        if value is not unset:
            kwargs["value"] = value
        super().__init__(kwargs)
