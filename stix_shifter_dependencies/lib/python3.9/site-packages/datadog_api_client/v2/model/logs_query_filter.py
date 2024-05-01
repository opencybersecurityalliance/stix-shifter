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
    from datadog_api_client.v2.model.logs_storage_tier import LogsStorageTier


class LogsQueryFilter(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.logs_storage_tier import LogsStorageTier

        return {
            "_from": (str,),
            "indexes": ([str],),
            "query": (str,),
            "storage_tier": (LogsStorageTier,),
            "to": (str,),
        }

    attribute_map = {
        "_from": "from",
        "indexes": "indexes",
        "query": "query",
        "storage_tier": "storage_tier",
        "to": "to",
    }

    def __init__(
        self_,
        _from: Union[str, UnsetType] = unset,
        indexes: Union[List[str], UnsetType] = unset,
        query: Union[str, UnsetType] = unset,
        storage_tier: Union[LogsStorageTier, UnsetType] = unset,
        to: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The search and filter query settings

        :param _from: The minimum time for the requested logs, supports date math and regular timestamps (milliseconds).
        :type _from: str, optional

        :param indexes: For customers with multiple indexes, the indexes to search. Defaults to ['*'] which means all indexes.
        :type indexes: [str], optional

        :param query: The search query - following the log search syntax.
        :type query: str, optional

        :param storage_tier: Specifies storage type as indexes or online-archives
        :type storage_tier: LogsStorageTier, optional

        :param to: The maximum time for the requested logs, supports date math and regular timestamps (milliseconds).
        :type to: str, optional
        """
        if _from is not unset:
            kwargs["_from"] = _from
        if indexes is not unset:
            kwargs["indexes"] = indexes
        if query is not unset:
            kwargs["query"] = query
        if storage_tier is not unset:
            kwargs["storage_tier"] = storage_tier
        if to is not unset:
            kwargs["to"] = to
        super().__init__(kwargs)
