# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.metric_custom_space_aggregation import MetricCustomSpaceAggregation
    from datadog_api_client.v2.model.metric_custom_time_aggregation import MetricCustomTimeAggregation


class MetricCustomAggregation(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metric_custom_space_aggregation import MetricCustomSpaceAggregation
        from datadog_api_client.v2.model.metric_custom_time_aggregation import MetricCustomTimeAggregation

        return {
            "space": (MetricCustomSpaceAggregation,),
            "time": (MetricCustomTimeAggregation,),
        }

    attribute_map = {
        "space": "space",
        "time": "time",
    }

    def __init__(self_, space: MetricCustomSpaceAggregation, time: MetricCustomTimeAggregation, **kwargs):
        """
        A time and space aggregation combination for use in query.

        :param space: A space aggregation for use in query.
        :type space: MetricCustomSpaceAggregation

        :param time: A time aggregation for use in query.
        :type time: MetricCustomTimeAggregation
        """
        super().__init__(kwargs)

        self_.space = space
        self_.time = time
