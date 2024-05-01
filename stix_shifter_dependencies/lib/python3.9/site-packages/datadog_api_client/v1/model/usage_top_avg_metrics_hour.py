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
    from datadog_api_client.v1.model.usage_metric_category import UsageMetricCategory


class UsageTopAvgMetricsHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.usage_metric_category import UsageMetricCategory

        return {
            "avg_metric_hour": (int,),
            "max_metric_hour": (int,),
            "metric_category": (UsageMetricCategory,),
            "metric_name": (str,),
        }

    attribute_map = {
        "avg_metric_hour": "avg_metric_hour",
        "max_metric_hour": "max_metric_hour",
        "metric_category": "metric_category",
        "metric_name": "metric_name",
    }

    def __init__(
        self_,
        avg_metric_hour: Union[int, UnsetType] = unset,
        max_metric_hour: Union[int, UnsetType] = unset,
        metric_category: Union[UsageMetricCategory, UnsetType] = unset,
        metric_name: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Number of hourly recorded custom metrics for a given organization.

        :param avg_metric_hour: Average number of timeseries per hour in which the metric occurs.
        :type avg_metric_hour: int, optional

        :param max_metric_hour: Maximum number of timeseries per hour in which the metric occurs.
        :type max_metric_hour: int, optional

        :param metric_category: Contains the metric category.
        :type metric_category: UsageMetricCategory, optional

        :param metric_name: Contains the custom metric name.
        :type metric_name: str, optional
        """
        if avg_metric_hour is not unset:
            kwargs["avg_metric_hour"] = avg_metric_hour
        if max_metric_hour is not unset:
            kwargs["max_metric_hour"] = max_metric_hour
        if metric_category is not unset:
            kwargs["metric_category"] = metric_category
        if metric_name is not unset:
            kwargs["metric_name"] = metric_name
        super().__init__(kwargs)
