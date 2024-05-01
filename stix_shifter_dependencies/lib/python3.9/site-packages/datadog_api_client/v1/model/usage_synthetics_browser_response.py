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
    from datadog_api_client.v1.model.usage_synthetics_browser_hour import UsageSyntheticsBrowserHour


class UsageSyntheticsBrowserResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.usage_synthetics_browser_hour import UsageSyntheticsBrowserHour

        return {
            "usage": ([UsageSyntheticsBrowserHour],),
        }

    attribute_map = {
        "usage": "usage",
    }

    def __init__(self_, usage: Union[List[UsageSyntheticsBrowserHour], UnsetType] = unset, **kwargs):
        """
        Response containing the number of Synthetics Browser tests run for each hour for a given organization.

        :param usage: Get hourly usage for Synthetics Browser tests.
        :type usage: [UsageSyntheticsBrowserHour], optional
        """
        if usage is not unset:
            kwargs["usage"] = usage
        super().__init__(kwargs)
