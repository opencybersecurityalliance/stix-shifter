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
    from datadog_api_client.v2.model.hourly_usage_attributes import HourlyUsageAttributes
    from datadog_api_client.v2.model.usage_time_series_type import UsageTimeSeriesType


class HourlyUsage(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.hourly_usage_attributes import HourlyUsageAttributes
        from datadog_api_client.v2.model.usage_time_series_type import UsageTimeSeriesType

        return {
            "attributes": (HourlyUsageAttributes,),
            "id": (str,),
            "type": (UsageTimeSeriesType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[HourlyUsageAttributes, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        type: Union[UsageTimeSeriesType, UnsetType] = unset,
        **kwargs,
    ):
        """
        Hourly usage for a product family for an org.

        :param attributes: Attributes of hourly usage for a product family for an org for a time period.
        :type attributes: HourlyUsageAttributes, optional

        :param id: Unique ID of the response.
        :type id: str, optional

        :param type: Type of usage data.
        :type type: UsageTimeSeriesType, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
