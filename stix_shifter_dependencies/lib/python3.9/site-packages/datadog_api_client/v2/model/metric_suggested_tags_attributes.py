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
    from datadog_api_client.v2.model.metric_suggested_aggregations import MetricSuggestedAggregations


class MetricSuggestedTagsAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metric_suggested_aggregations import MetricSuggestedAggregations

        return {
            "active_aggregations": (MetricSuggestedAggregations,),
            "active_tags": ([str],),
        }

    attribute_map = {
        "active_aggregations": "active_aggregations",
        "active_tags": "active_tags",
    }

    def __init__(
        self_,
        active_aggregations: Union[MetricSuggestedAggregations, UnsetType] = unset,
        active_tags: Union[List[str], UnsetType] = unset,
        **kwargs,
    ):
        """
        Object containing the definition of a metric's actively queried tags and aggregations.

        :param active_aggregations: List of aggregation combinations that have been actively queried.
        :type active_aggregations: MetricSuggestedAggregations, optional

        :param active_tags: List of tag keys that have been actively queried.
        :type active_tags: [str], optional
        """
        if active_aggregations is not unset:
            kwargs["active_aggregations"] = active_aggregations
        if active_tags is not unset:
            kwargs["active_tags"] = active_tags
        super().__init__(kwargs)
