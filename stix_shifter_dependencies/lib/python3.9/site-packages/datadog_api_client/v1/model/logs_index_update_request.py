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


class LogsIndexUpdateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.logs_exclusion import LogsExclusion
        from datadog_api_client.v1.model.logs_filter import LogsFilter

        return {
            "daily_limit": (int,),
            "disable_daily_limit": (bool,),
            "exclusion_filters": ([LogsExclusion],),
            "filter": (LogsFilter,),
            "num_retention_days": (int,),
        }

    attribute_map = {
        "daily_limit": "daily_limit",
        "disable_daily_limit": "disable_daily_limit",
        "exclusion_filters": "exclusion_filters",
        "filter": "filter",
        "num_retention_days": "num_retention_days",
    }

    def __init__(
        self_,
        filter: LogsFilter,
        daily_limit: Union[int, UnsetType] = unset,
        disable_daily_limit: Union[bool, UnsetType] = unset,
        exclusion_filters: Union[List[LogsExclusion], UnsetType] = unset,
        num_retention_days: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Object for updating a Datadog Log index.

        :param daily_limit: The number of log events you can send in this index per day before you are rate-limited.
        :type daily_limit: int, optional

        :param disable_daily_limit: If true, sets the ``daily_limit`` value to null and the index is not limited on a daily basis (any
            specified ``daily_limit`` value in the request is ignored). If false or omitted, the index's current
            ``daily_limit`` is maintained.
        :type disable_daily_limit: bool, optional

        :param exclusion_filters: An array of exclusion objects. The logs are tested against the query of each filter,
            following the order of the array. Only the first matching active exclusion matters,
            others (if any) are ignored.
        :type exclusion_filters: [LogsExclusion], optional

        :param filter: Filter for logs.
        :type filter: LogsFilter

        :param num_retention_days: The number of days before logs are deleted from this index. Available values depend on
            retention plans specified in your organization's contract/subscriptions.

            **Note:** Changing the retention for an index adjusts the length of retention for all logs
            already in this index. It may also affect billing.
        :type num_retention_days: int, optional
        """
        if daily_limit is not unset:
            kwargs["daily_limit"] = daily_limit
        if disable_daily_limit is not unset:
            kwargs["disable_daily_limit"] = disable_daily_limit
        if exclusion_filters is not unset:
            kwargs["exclusion_filters"] = exclusion_filters
        if num_retention_days is not unset:
            kwargs["num_retention_days"] = num_retention_days
        super().__init__(kwargs)

        self_.filter = filter
