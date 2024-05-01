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
    from datadog_api_client.v2.model.logs_metric_response_compute_aggregation_type import (
        LogsMetricResponseComputeAggregationType,
    )


class LogsMetricResponseCompute(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.logs_metric_response_compute_aggregation_type import (
            LogsMetricResponseComputeAggregationType,
        )

        return {
            "aggregation_type": (LogsMetricResponseComputeAggregationType,),
            "include_percentiles": (bool,),
            "path": (str,),
        }

    attribute_map = {
        "aggregation_type": "aggregation_type",
        "include_percentiles": "include_percentiles",
        "path": "path",
    }

    def __init__(
        self_,
        aggregation_type: Union[LogsMetricResponseComputeAggregationType, UnsetType] = unset,
        include_percentiles: Union[bool, UnsetType] = unset,
        path: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The compute rule to compute the log-based metric.

        :param aggregation_type: The type of aggregation to use.
        :type aggregation_type: LogsMetricResponseComputeAggregationType, optional

        :param include_percentiles: Toggle to include or exclude percentile aggregations for distribution metrics.
            Only present when the ``aggregation_type`` is ``distribution``.
        :type include_percentiles: bool, optional

        :param path: The path to the value the log-based metric will aggregate on (only used if the aggregation type is a "distribution").
        :type path: str, optional
        """
        if aggregation_type is not unset:
            kwargs["aggregation_type"] = aggregation_type
        if include_percentiles is not unset:
            kwargs["include_percentiles"] = include_percentiles
        if path is not unset:
            kwargs["path"] = path
        super().__init__(kwargs)
