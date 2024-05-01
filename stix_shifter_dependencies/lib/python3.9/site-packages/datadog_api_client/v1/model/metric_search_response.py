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
    from datadog_api_client.v1.model.metric_search_response_results import MetricSearchResponseResults


class MetricSearchResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.metric_search_response_results import MetricSearchResponseResults

        return {
            "results": (MetricSearchResponseResults,),
        }

    attribute_map = {
        "results": "results",
    }

    def __init__(self_, results: Union[MetricSearchResponseResults, UnsetType] = unset, **kwargs):
        """
        Object containing the list of metrics matching the search query.

        :param results: Search result.
        :type results: MetricSearchResponseResults, optional
        """
        if results is not unset:
            kwargs["results"] = results
        super().__init__(kwargs)
