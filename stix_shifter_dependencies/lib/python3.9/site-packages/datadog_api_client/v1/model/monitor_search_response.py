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
    from datadog_api_client.v1.model.monitor_search_response_counts import MonitorSearchResponseCounts
    from datadog_api_client.v1.model.monitor_search_response_metadata import MonitorSearchResponseMetadata
    from datadog_api_client.v1.model.monitor_search_result import MonitorSearchResult


class MonitorSearchResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.monitor_search_response_counts import MonitorSearchResponseCounts
        from datadog_api_client.v1.model.monitor_search_response_metadata import MonitorSearchResponseMetadata
        from datadog_api_client.v1.model.monitor_search_result import MonitorSearchResult

        return {
            "counts": (MonitorSearchResponseCounts,),
            "metadata": (MonitorSearchResponseMetadata,),
            "monitors": ([MonitorSearchResult],),
        }

    attribute_map = {
        "counts": "counts",
        "metadata": "metadata",
        "monitors": "monitors",
    }
    read_only_vars = {
        "counts",
        "monitors",
    }

    def __init__(
        self_,
        counts: Union[MonitorSearchResponseCounts, UnsetType] = unset,
        metadata: Union[MonitorSearchResponseMetadata, UnsetType] = unset,
        monitors: Union[List[MonitorSearchResult], UnsetType] = unset,
        **kwargs,
    ):
        """
        The response form a monitor search.

        :param counts: The counts of monitors per different criteria.
        :type counts: MonitorSearchResponseCounts, optional

        :param metadata: Metadata about the response.
        :type metadata: MonitorSearchResponseMetadata, optional

        :param monitors: The list of found monitors.
        :type monitors: [MonitorSearchResult], optional
        """
        if counts is not unset:
            kwargs["counts"] = counts
        if metadata is not unset:
            kwargs["metadata"] = metadata
        if monitors is not unset:
            kwargs["monitors"] = monitors
        super().__init__(kwargs)
