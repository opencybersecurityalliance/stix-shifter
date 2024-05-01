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
    from datadog_api_client.v1.model.synthetics_global_variable_totp_parameters import (
        SyntheticsGlobalVariableTOTPParameters,
    )


class SyntheticsGlobalVariableOptions(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.synthetics_global_variable_totp_parameters import (
            SyntheticsGlobalVariableTOTPParameters,
        )

        return {
            "totp_parameters": (SyntheticsGlobalVariableTOTPParameters,),
        }

    attribute_map = {
        "totp_parameters": "totp_parameters",
    }

    def __init__(self_, totp_parameters: Union[SyntheticsGlobalVariableTOTPParameters, UnsetType] = unset, **kwargs):
        """
        Options for the Global Variable for MFA.

        :param totp_parameters: Parameters for the TOTP/MFA variable
        :type totp_parameters: SyntheticsGlobalVariableTOTPParameters, optional
        """
        if totp_parameters is not unset:
            kwargs["totp_parameters"] = totp_parameters
        super().__init__(kwargs)
