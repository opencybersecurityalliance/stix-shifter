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


class LogsMetricUpdateCompute(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "include_percentiles": (bool,),
        }

    attribute_map = {
        "include_percentiles": "include_percentiles",
    }

    def __init__(self_, include_percentiles: Union[bool, UnsetType] = unset, **kwargs):
        """
        The compute rule to compute the log-based metric.

        :param include_percentiles: Toggle to include or exclude percentile aggregations for distribution metrics.
            Only present when the ``aggregation_type`` is ``distribution``.
        :type include_percentiles: bool, optional
        """
        if include_percentiles is not unset:
            kwargs["include_percentiles"] = include_percentiles
        super().__init__(kwargs)
