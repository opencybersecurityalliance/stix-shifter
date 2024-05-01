# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.usage_top_avg_metrics_pagination import UsageTopAvgMetricsPagination


class UsageTopAvgMetricsMetadata(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.usage_top_avg_metrics_pagination import UsageTopAvgMetricsPagination

        return {
            "day": (datetime,),
            "month": (datetime,),
            "pagination": (UsageTopAvgMetricsPagination,),
        }

    attribute_map = {
        "day": "day",
        "month": "month",
        "pagination": "pagination",
    }

    def __init__(
        self_,
        day: Union[datetime, UnsetType] = unset,
        month: Union[datetime, UnsetType] = unset,
        pagination: Union[UsageTopAvgMetricsPagination, UnsetType] = unset,
        **kwargs,
    ):
        """
        The object containing document metadata.

        :param day: The day value from the user request that contains the returned usage data. (If day was used the request)
        :type day: datetime, optional

        :param month: The month value from the user request that contains the returned usage data. (If month was used the request)
        :type month: datetime, optional

        :param pagination: The metadata for the current pagination.
        :type pagination: UsageTopAvgMetricsPagination, optional
        """
        if day is not unset:
            kwargs["day"] = day
        if month is not unset:
            kwargs["month"] = month
        if pagination is not unset:
            kwargs["pagination"] = pagination
        super().__init__(kwargs)
