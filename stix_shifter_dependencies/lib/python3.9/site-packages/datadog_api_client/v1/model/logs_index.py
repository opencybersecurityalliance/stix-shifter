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
    from datadog_api_client.v1.model.logs_exclusion import LogsExclusion
    from datadog_api_client.v1.model.logs_filter import LogsFilter


class LogsIndex(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_exclusion import LogsExclusion
        from datadog_api_client.v1.model.logs_filter import LogsFilter

        return {
            "daily_limit": (int,),
            "exclusion_filters": ([LogsExclusion],),
            "filter": (LogsFilter,),
            "is_rate_limited": (bool,),
            "name": (str,),
            "num_retention_days": (int,),
        }

    attribute_map = {
        "daily_limit": "daily_limit",
        "exclusion_filters": "exclusion_filters",
        "filter": "filter",
        "is_rate_limited": "is_rate_limited",
        "name": "name",
        "num_retention_days": "num_retention_days",
    }
    read_only_vars = {
        "is_rate_limited",
    }

    def __init__(
        self_,
        filter: LogsFilter,
        name: str,
        daily_limit: Union[int, UnsetType] = unset,
        exclusion_filters: Union[List[LogsExclusion], UnsetType] = unset,
        is_rate_limited: Union[bool, UnsetType] = unset,
        num_retention_days: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object describing a Datadog Log index.

        :param daily_limit: The number of log events you can send in this index per day before you are rate-limited.
        :type daily_limit: int, optional

        :param exclusion_filters: An array of exclusion objects. The logs are tested against the query of each filter,
            following the order of the array. Only the first matching active exclusion matters,
            others (if any) are ignored.
        :type exclusion_filters: [LogsExclusion], optional

        :param filter: Filter for logs.
        :type filter: LogsFilter

        :param is_rate_limited: A boolean stating if the index is rate limited, meaning more logs than the daily limit have been sent.
            Rate limit is reset every-day at 2pm UTC.
        :type is_rate_limited: bool, optional

        :param name: The name of the index.
        :type name: str

        :param num_retention_days: The number of days before logs are deleted from this index. Available values depend on
            retention plans specified in your organization's contract/subscriptions.
        :type num_retention_days: int, optional
        """
        if daily_limit is not unset:
            kwargs["daily_limit"] = daily_limit
        if exclusion_filters is not unset:
            kwargs["exclusion_filters"] = exclusion_filters
        if is_rate_limited is not unset:
            kwargs["is_rate_limited"] = is_rate_limited
        if num_retention_days is not unset:
            kwargs["num_retention_days"] = num_retention_days
        super().__init__(kwargs)

        self_.filter = filter
        self_.name = name
