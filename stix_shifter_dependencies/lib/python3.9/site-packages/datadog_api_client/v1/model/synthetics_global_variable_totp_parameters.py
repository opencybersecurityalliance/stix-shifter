# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class SyntheticsGlobalVariableTOTPParameters(ModelNormal):
    validations = {
        "digits": {
            "inclusive_maximum": 10,
            "inclusive_minimum": 4,
        },
        "refresh_interval": {
            "inclusive_maximum": 999,
            "inclusive_minimum": 0,
        },
    }

    @cached_property
    def openapi_types(_):
        return {
            "digits": (int,),
            "refresh_interval": (int,),
        }

    attribute_map = {
        "digits": "digits",
        "refresh_interval": "refresh_interval",
    }

    def __init__(
        self_, digits: Union[int, UnsetType] = unset, refresh_interval: Union[int, UnsetType] = unset, **kwargs
    ):
        """
        Parameters for the TOTP/MFA variable

        :param digits: Number of digits for the OTP code.
        :type digits: int, optional

        :param refresh_interval: Interval for which to refresh the token (in seconds).
        :type refresh_interval: int, optional
        """
        if digits is not unset:
            kwargs["digits"] = digits
        if refresh_interval is not unset:
            kwargs["refresh_interval"] = refresh_interval
        super().__init__(kwargs)
