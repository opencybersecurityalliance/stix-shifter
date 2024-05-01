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
    from datadog_api_client.v1.model.api_key import ApiKey


class ApiKeyListResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.api_key import ApiKey

        return {
            "api_keys": ([ApiKey],),
        }

    attribute_map = {
        "api_keys": "api_keys",
    }

    def __init__(self_, api_keys: Union[List[ApiKey], UnsetType] = unset, **kwargs):
        """
        List of API and application keys available for a given organization.

        :param api_keys: Array of API keys.
        :type api_keys: [ApiKey], optional
        """
        if api_keys is not unset:
            kwargs["api_keys"] = api_keys
        super().__init__(kwargs)
