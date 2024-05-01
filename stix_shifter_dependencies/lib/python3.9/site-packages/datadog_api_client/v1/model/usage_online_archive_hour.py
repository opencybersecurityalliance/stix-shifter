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


class UsageOnlineArchiveHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "hour": (datetime,),
            "online_archive_events_count": (int, none_type),
            "org_name": (str,),
            "public_id": (str,),
        }

    attribute_map = {
        "hour": "hour",
        "online_archive_events_count": "online_archive_events_count",
        "org_name": "org_name",
        "public_id": "public_id",
    }

    def __init__(
        self_,
        hour: Union[datetime, UnsetType] = unset,
        online_archive_events_count: Union[int, none_type, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Online Archive usage in a given hour.

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param online_archive_events_count: Total count of online archived events within the hour.
        :type online_archive_events_count: int, none_type, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional
        """
        if hour is not unset:
            kwargs["hour"] = hour
        if online_archive_events_count is not unset:
            kwargs["online_archive_events_count"] = online_archive_events_count
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        super().__init__(kwargs)
