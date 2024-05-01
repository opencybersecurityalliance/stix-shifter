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


class UsageIngestedSpansHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "hour": (datetime,),
            "ingested_events_bytes": (int,),
            "org_name": (str,),
            "public_id": (str,),
        }

    attribute_map = {
        "hour": "hour",
        "ingested_events_bytes": "ingested_events_bytes",
        "org_name": "org_name",
        "public_id": "public_id",
    }

    def __init__(
        self_,
        hour: Union[datetime, UnsetType] = unset,
        ingested_events_bytes: Union[int, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Ingested spans usage for a given organization for a given hour.

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param ingested_events_bytes: Contains the total number of bytes ingested for APM spans during a given hour.
        :type ingested_events_bytes: int, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional
        """
        if hour is not unset:
            kwargs["hour"] = hour
        if ingested_events_bytes is not unset:
            kwargs["ingested_events_bytes"] = ingested_events_bytes
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        super().__init__(kwargs)
