# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.monitor_overall_states import MonitorOverallStates


class MonitorGroupSearchResult(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.monitor_overall_states import MonitorOverallStates

        return {
            "group": (str,),
            "group_tags": ([str],),
            "last_nodata_ts": (int,),
            "last_triggered_ts": (int, none_type),
            "monitor_id": (int,),
            "monitor_name": (str,),
            "status": (MonitorOverallStates,),
        }

    attribute_map = {
        "group": "group",
        "group_tags": "group_tags",
        "last_nodata_ts": "last_nodata_ts",
        "last_triggered_ts": "last_triggered_ts",
        "monitor_id": "monitor_id",
        "monitor_name": "monitor_name",
        "status": "status",
    }
    read_only_vars = {
        "group",
        "group_tags",
        "last_nodata_ts",
        "last_triggered_ts",
        "monitor_id",
        "monitor_name",
        "status",
    }

    def __init__(
        self_,
        group: Union[str, UnsetType] = unset,
        group_tags: Union[List[str], UnsetType] = unset,
        last_nodata_ts: Union[int, UnsetType] = unset,
        last_triggered_ts: Union[int, none_type, UnsetType] = unset,
        monitor_id: Union[int, UnsetType] = unset,
        monitor_name: Union[str, UnsetType] = unset,
        status: Union[MonitorOverallStates, UnsetType] = unset,
        **kwargs,
    ):
        """
        A single monitor group search result.

        :param group: The name of the group.
        :type group: str, optional

        :param group_tags: The list of tags of the monitor group.
        :type group_tags: [str], optional

        :param last_nodata_ts: Latest timestamp the monitor group was in NO_DATA state.
        :type last_nodata_ts: int, optional

        :param last_triggered_ts: Latest timestamp the monitor group triggered.
        :type last_triggered_ts: int, none_type, optional

        :param monitor_id: The ID of the monitor.
        :type monitor_id: int, optional

        :param monitor_name: The name of the monitor.
        :type monitor_name: str, optional

        :param status: The different states your monitor can be in.
        :type status: MonitorOverallStates, optional
        """
        if group is not unset:
            kwargs["group"] = group
        if group_tags is not unset:
            kwargs["group_tags"] = group_tags
        if last_nodata_ts is not unset:
            kwargs["last_nodata_ts"] = last_nodata_ts
        if last_triggered_ts is not unset:
            kwargs["last_triggered_ts"] = last_triggered_ts
        if monitor_id is not unset:
            kwargs["monitor_id"] = monitor_id
        if monitor_name is not unset:
            kwargs["monitor_name"] = monitor_name
        if status is not unset:
            kwargs["status"] = status
        super().__init__(kwargs)
