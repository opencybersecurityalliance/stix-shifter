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
    from datadog_api_client.v1.model.monitor_group_search_response_counts import MonitorGroupSearchResponseCounts
    from datadog_api_client.v1.model.monitor_group_search_result import MonitorGroupSearchResult
    from datadog_api_client.v1.model.monitor_search_response_metadata import MonitorSearchResponseMetadata


class MonitorGroupSearchResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.monitor_group_search_response_counts import MonitorGroupSearchResponseCounts
        from datadog_api_client.v1.model.monitor_group_search_result import MonitorGroupSearchResult
        from datadog_api_client.v1.model.monitor_search_response_metadata import MonitorSearchResponseMetadata

        return {
            "counts": (MonitorGroupSearchResponseCounts,),
            "groups": ([MonitorGroupSearchResult],),
            "metadata": (MonitorSearchResponseMetadata,),
        }

    attribute_map = {
        "counts": "counts",
        "groups": "groups",
        "metadata": "metadata",
    }
    read_only_vars = {
        "counts",
        "groups",
    }

    def __init__(
        self_,
        counts: Union[MonitorGroupSearchResponseCounts, UnsetType] = unset,
        groups: Union[List[MonitorGroupSearchResult], UnsetType] = unset,
        metadata: Union[MonitorSearchResponseMetadata, UnsetType] = unset,
        **kwargs,
    ):
        """
        The response of a monitor group search.

        :param counts: The counts of monitor groups per different criteria.
        :type counts: MonitorGroupSearchResponseCounts, optional

        :param groups: The list of found monitor groups.
        :type groups: [MonitorGroupSearchResult], optional

        :param metadata: Metadata about the response.
        :type metadata: MonitorSearchResponseMetadata, optional
        """
        if counts is not unset:
            kwargs["counts"] = counts
        if groups is not unset:
            kwargs["groups"] = groups
        if metadata is not unset:
            kwargs["metadata"] = metadata
        super().__init__(kwargs)
