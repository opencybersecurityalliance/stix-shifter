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


class MonitorOptionsAggregation(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "group_by": (str,),
            "metric": (str,),
            "type": (str,),
        }

    attribute_map = {
        "group_by": "group_by",
        "metric": "metric",
        "type": "type",
    }

    def __init__(
        self_,
        group_by: Union[str, UnsetType] = unset,
        metric: Union[str, UnsetType] = unset,
        type: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Type of aggregation performed in the monitor query.

        :param group_by: Group to break down the monitor on.
        :type group_by: str, optional

        :param metric: Metric name used in the monitor.
        :type metric: str, optional

        :param type: Metric type used in the monitor.
        :type type: str, optional
        """
        if group_by is not unset:
            kwargs["group_by"] = group_by
        if metric is not unset:
            kwargs["metric"] = metric
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
