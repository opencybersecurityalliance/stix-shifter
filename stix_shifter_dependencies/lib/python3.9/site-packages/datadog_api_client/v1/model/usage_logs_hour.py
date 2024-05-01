# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    none_type,
    unset,
    UnsetType,
)


class UsageLogsHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "billable_ingested_bytes": (int, none_type),
            "hour": (datetime,),
            "indexed_events_count": (int, none_type),
            "ingested_events_bytes": (int, none_type),
            "logs_forwarding_events_bytes": (int, none_type),
            "logs_live_indexed_count": (int, none_type),
            "logs_live_ingested_bytes": (int, none_type),
            "logs_rehydrated_indexed_count": (int, none_type),
            "logs_rehydrated_ingested_bytes": (int, none_type),
            "org_name": (str,),
            "public_id": (str,),
        }

    attribute_map = {
        "billable_ingested_bytes": "billable_ingested_bytes",
        "hour": "hour",
        "indexed_events_count": "indexed_events_count",
        "ingested_events_bytes": "ingested_events_bytes",
        "logs_forwarding_events_bytes": "logs_forwarding_events_bytes",
        "logs_live_indexed_count": "logs_live_indexed_count",
        "logs_live_ingested_bytes": "logs_live_ingested_bytes",
        "logs_rehydrated_indexed_count": "logs_rehydrated_indexed_count",
        "logs_rehydrated_ingested_bytes": "logs_rehydrated_ingested_bytes",
        "org_name": "org_name",
        "public_id": "public_id",
    }

    def __init__(
        self_,
        billable_ingested_bytes: Union[int, none_type, UnsetType] = unset,
        hour: Union[datetime, UnsetType] = unset,
        indexed_events_count: Union[int, none_type, UnsetType] = unset,
        ingested_events_bytes: Union[int, none_type, UnsetType] = unset,
        logs_forwarding_events_bytes: Union[int, none_type, UnsetType] = unset,
        logs_live_indexed_count: Union[int, none_type, UnsetType] = unset,
        logs_live_ingested_bytes: Union[int, none_type, UnsetType] = unset,
        logs_rehydrated_indexed_count: Union[int, none_type, UnsetType] = unset,
        logs_rehydrated_ingested_bytes: Union[int, none_type, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Hour usage for logs.

        :param billable_ingested_bytes: Contains the number of billable log bytes ingested.
        :type billable_ingested_bytes: int, none_type, optional

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param indexed_events_count: Contains the number of log events indexed.
        :type indexed_events_count: int, none_type, optional

        :param ingested_events_bytes: Contains the number of log bytes ingested.
        :type ingested_events_bytes: int, none_type, optional

        :param logs_forwarding_events_bytes: Contains the number of logs forwarded bytes (data available as of April 1st 2023)
        :type logs_forwarding_events_bytes: int, none_type, optional

        :param logs_live_indexed_count: Contains the number of live log events indexed (data available as of December 1, 2020).
        :type logs_live_indexed_count: int, none_type, optional

        :param logs_live_ingested_bytes: Contains the number of live log bytes ingested (data available as of December 1, 2020).
        :type logs_live_ingested_bytes: int, none_type, optional

        :param logs_rehydrated_indexed_count: Contains the number of rehydrated log events indexed (data available as of December 1, 2020).
        :type logs_rehydrated_indexed_count: int, none_type, optional

        :param logs_rehydrated_ingested_bytes: Contains the number of rehydrated log bytes ingested (data available as of December 1, 2020).
        :type logs_rehydrated_ingested_bytes: int, none_type, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional
        """
        if billable_ingested_bytes is not unset:
            kwargs["billable_ingested_bytes"] = billable_ingested_bytes
        if hour is not unset:
            kwargs["hour"] = hour
        if indexed_events_count is not unset:
            kwargs["indexed_events_count"] = indexed_events_count
        if ingested_events_bytes is not unset:
            kwargs["ingested_events_bytes"] = ingested_events_bytes
        if logs_forwarding_events_bytes is not unset:
            kwargs["logs_forwarding_events_bytes"] = logs_forwarding_events_bytes
        if logs_live_indexed_count is not unset:
            kwargs["logs_live_indexed_count"] = logs_live_indexed_count
        if logs_live_ingested_bytes is not unset:
            kwargs["logs_live_ingested_bytes"] = logs_live_ingested_bytes
        if logs_rehydrated_indexed_count is not unset:
            kwargs["logs_rehydrated_indexed_count"] = logs_rehydrated_indexed_count
        if logs_rehydrated_ingested_bytes is not unset:
            kwargs["logs_rehydrated_ingested_bytes"] = logs_rehydrated_ingested_bytes
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        super().__init__(kwargs)
