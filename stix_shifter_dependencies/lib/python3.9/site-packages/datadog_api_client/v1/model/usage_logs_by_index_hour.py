# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


class UsageLogsByIndexHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "event_count": (int,),
            "hour": (datetime,),
            "index_id": (str,),
            "index_name": (str,),
            "org_name": (str,),
            "public_id": (str,),
            "retention": (int,),
        }

    attribute_map = {
        "event_count": "event_count",
        "hour": "hour",
        "index_id": "index_id",
        "index_name": "index_name",
        "org_name": "org_name",
        "public_id": "public_id",
        "retention": "retention",
    }

    def __init__(
        self_,
        event_count: Union[int, UnsetType] = unset,
        hour: Union[datetime, UnsetType] = unset,
        index_id: Union[str, UnsetType] = unset,
        index_name: Union[str, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        retention: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Number of indexed logs for each hour and index for a given organization.

        :param event_count: The total number of indexed logs for the queried hour.
        :type event_count: int, optional

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param index_id: The index ID for this usage.
        :type index_id: str, optional

        :param index_name: The user specified name for this index ID.
        :type index_name: str, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional

        :param retention: The retention period (in days) for this index ID.
        :type retention: int, optional
        """
        if event_count is not unset:
            kwargs["event_count"] = event_count
        if hour is not unset:
            kwargs["hour"] = hour
        if index_id is not unset:
            kwargs["index_id"] = index_id
        if index_name is not unset:
            kwargs["index_name"] = index_name
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if retention is not unset:
            kwargs["retention"] = retention
        super().__init__(kwargs)
