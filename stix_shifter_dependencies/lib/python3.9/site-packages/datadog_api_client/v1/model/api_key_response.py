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
    from datadog_api_client.v1.model.api_key import ApiKey


class ApiKeyResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.api_key import ApiKey

        return {
            "api_key": (ApiKey,),
        }

    attribute_map = {
        "api_key": "api_key",
    }

    def __init__(self_, api_key: Union[ApiKey, UnsetType] = unset, **kwargs):
        """
        An API key with its associated metadata.

        :param api_key: Datadog API key.
        :type api_key: ApiKey, optional
        """
        if api_key is not unset:
            kwargs["api_key"] = api_key
        super().__init__(kwargs)
