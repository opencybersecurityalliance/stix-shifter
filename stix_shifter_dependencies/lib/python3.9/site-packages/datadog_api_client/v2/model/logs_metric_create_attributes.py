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
    from datadog_api_client.v2.model.logs_metric_compute import LogsMetricCompute
    from datadog_api_client.v2.model.logs_metric_filter import LogsMetricFilter
    from datadog_api_client.v2.model.logs_metric_group_by import LogsMetricGroupBy


class LogsMetricCreateAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.logs_metric_compute import LogsMetricCompute
        from datadog_api_client.v2.model.logs_metric_filter import LogsMetricFilter
        from datadog_api_client.v2.model.logs_metric_group_by import LogsMetricGroupBy

        return {
            "compute": (LogsMetricCompute,),
            "filter": (LogsMetricFilter,),
            "group_by": ([LogsMetricGroupBy],),
        }

    attribute_map = {
        "compute": "compute",
        "filter": "filter",
        "group_by": "group_by",
    }

    def __init__(
        self_,
        compute: LogsMetricCompute,
        filter: Union[LogsMetricFilter, UnsetType] = unset,
        group_by: Union[List[LogsMetricGroupBy], UnsetType] = unset,
        **kwargs,
    ):
        """
        The object describing the Datadog log-based metric to create.

        :param compute: The compute rule to compute the log-based metric.
        :type compute: LogsMetricCompute

        :param filter: The log-based metric filter. Logs matching this filter will be aggregated in this metric.
        :type filter: LogsMetricFilter, optional

        :param group_by: The rules for the group by.
        :type group_by: [LogsMetricGroupBy], optional
        """
        if filter is not unset:
            kwargs["filter"] = filter
        if group_by is not unset:
            kwargs["group_by"] = group_by
        super().__init__(kwargs)

        self_.compute = compute
