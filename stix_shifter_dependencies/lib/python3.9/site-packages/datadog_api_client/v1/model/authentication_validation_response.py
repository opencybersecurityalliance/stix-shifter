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


class AuthenticationValidationResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "valid": (bool,),
        }

    attribute_map = {
        "valid": "valid",
    }
    read_only_vars = {
        "valid",
    }

    def __init__(self_, valid: Union[bool, UnsetType] = unset, **kwargs):
        """
        Represent validation endpoint responses.

        :param valid: Return ``true`` if the authentication response is valid.
        :type valid: bool, optional
        """
        if valid is not unset:
            kwargs["valid"] = valid
        super().__init__(kwargs)
