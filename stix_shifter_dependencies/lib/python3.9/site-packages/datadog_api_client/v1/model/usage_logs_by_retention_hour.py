# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class UsageLogsByRetentionHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "indexed_events_count": (int,),
            "live_indexed_events_count": (int,),
            "org_name": (str,),
            "public_id": (str,),
            "rehydrated_indexed_events_count": (int,),
            "retention": (str,),
        }

    attribute_map = {
        "indexed_events_count": "indexed_events_count",
        "live_indexed_events_count": "live_indexed_events_count",
        "org_name": "org_name",
        "public_id": "public_id",
        "rehydrated_indexed_events_count": "rehydrated_indexed_events_count",
        "retention": "retention",
    }

    def __init__(
        self_,
        indexed_events_count: Union[int, UnsetType] = unset,
        live_indexed_events_count: Union[int, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        rehydrated_indexed_events_count: Union[int, UnsetType] = unset,
        retention: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        The number of indexed logs for each hour for a given organization broken down by retention period.

        :param indexed_events_count: Total logs indexed with this retention period during a given hour.
        :type indexed_events_count: int, optional

        :param live_indexed_events_count: Live logs indexed with this retention period during a given hour.
        :type live_indexed_events_count: int, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional

        :param rehydrated_indexed_events_count: Rehydrated logs indexed with this retention period during a given hour.
        :type rehydrated_indexed_events_count: int, optional

        :param retention: The retention period in days or "custom" for all custom retention usage.
        :type retention: str, optional
        """
        if indexed_events_count is not unset:
            kwargs["indexed_events_count"] = indexed_events_count
        if live_indexed_events_count is not unset:
            kwargs["live_indexed_events_count"] = live_indexed_events_count
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if rehydrated_indexed_events_count is not unset:
            kwargs["rehydrated_indexed_events_count"] = rehydrated_indexed_events_count
        if retention is not unset:
            kwargs["retention"] = retention
        super().__init__(kwargs)
