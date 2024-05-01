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
    from datadog_api_client.v1.model.logs_sort import LogsSort
    from datadog_api_client.v1.model.logs_list_request_time import LogsListRequestTime


class LogsListRequest(ModelNormal):
    validations = {
        "limit": {
            "inclusive_maximum": 1000,
        },
    }

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_sort import LogsSort
        from datadog_api_client.v1.model.logs_list_request_time import LogsListRequestTime

        return {
            "index": (str,),
            "limit": (int,),
            "query": (str,),
            "sort": (LogsSort,),
            "start_at": (str,),
            "time": (LogsListRequestTime,),
        }

    attribute_map = {
        "index": "index",
        "limit": "limit",
        "query": "query",
        "sort": "sort",
        "start_at": "startAt",
        "time": "time",
    }

    def __init__(
        self_,
        time: LogsListRequestTime,
        index: Union[str, UnsetType] = unset,
        limit: Union[int, UnsetType] = unset,
        query: Union[str, UnsetType] = unset,
        sort: Union[LogsSort, UnsetType] = unset,
        start_at: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object to send with the request to retrieve a list of logs from your Organization.

        :param index: The log index on which the request is performed. For multi-index organizations,
            the default is all live indexes. Historical indexes of rehydrated logs must be specified.
        :type index: str, optional

        :param limit: Number of logs return in the response.
        :type limit: int, optional

        :param query: The search query - following the log search syntax.
        :type query: str, optional

        :param sort: Time-ascending ``asc`` or time-descending ``desc`` results.
        :type sort: LogsSort, optional

        :param start_at: Hash identifier of the first log to return in the list, available in a log ``id`` attribute.
            This parameter is used for the pagination feature.

            **Note** : This parameter is ignored if the corresponding log
            is out of the scope of the specified time window.
        :type start_at: str, optional

        :param time: Timeframe to retrieve the log from.
        :type time: LogsListRequestTime
        """
        if index is not unset:
            kwargs["index"] = index
        if limit is not unset:
            kwargs["limit"] = limit
        if query is not unset:
            kwargs["query"] = query
        if sort is not unset:
            kwargs["sort"] = sort
        if start_at is not unset:
            kwargs["start_at"] = start_at
        super().__init__(kwargs)

        self_.time = time
