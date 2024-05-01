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


class FastlyAccountUpdateRequestAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "api_key": (str,),
        }

    attribute_map = {
        "api_key": "api_key",
    }

    def __init__(self_, api_key: Union[str, UnsetType] = unset, **kwargs):
        """
        Attributes object for updating a Fastly account.

        :param api_key: The API key of the Fastly account.
        :type api_key: str, optional
        """
        if api_key is not unset:
            kwargs["api_key"] = api_key
        super().__init__(kwargs)
