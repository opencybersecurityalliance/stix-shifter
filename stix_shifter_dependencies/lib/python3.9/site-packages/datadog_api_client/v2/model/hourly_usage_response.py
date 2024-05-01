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
    from datadog_api_client.v2.model.hourly_usage import HourlyUsage
    from datadog_api_client.v2.model.hourly_usage_metadata import HourlyUsageMetadata


class HourlyUsageResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.hourly_usage import HourlyUsage
        from datadog_api_client.v2.model.hourly_usage_metadata import HourlyUsageMetadata

        return {
            "data": ([HourlyUsage],),
            "meta": (HourlyUsageMetadata,),
        }

    attribute_map = {
        "data": "data",
        "meta": "meta",
    }

    def __init__(
        self_,
        data: Union[List[HourlyUsage], UnsetType] = unset,
        meta: Union[HourlyUsageMetadata, UnsetType] = unset,
        **kwargs,
    ):
        """
        Hourly usage response.

        :param data: Response containing hourly usage.
        :type data: [HourlyUsage], optional

        :param meta: The object containing document metadata.
        :type meta: HourlyUsageMetadata, optional
        """
        if data is not unset:
            kwargs["data"] = data
        if meta is not unset:
            kwargs["meta"] = meta
        super().__init__(kwargs)
