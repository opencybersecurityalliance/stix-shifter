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
    from datadog_api_client.v2.model.metric_suggested_tags_and_aggregations import MetricSuggestedTagsAndAggregations


class MetricSuggestedTagsAndAggregationsResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metric_suggested_tags_and_aggregations import (
            MetricSuggestedTagsAndAggregations,
        )

        return {
            "data": (MetricSuggestedTagsAndAggregations,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: Union[MetricSuggestedTagsAndAggregations, UnsetType] = unset, **kwargs):
        """
        Response object that includes a single metric's actively queried tags and aggregations.

        :param data: Object for a single metric's actively queried tags and aggregations.
        :type data: MetricSuggestedTagsAndAggregations, optional
        """
        if data is not unset:
            kwargs["data"] = data
        super().__init__(kwargs)
