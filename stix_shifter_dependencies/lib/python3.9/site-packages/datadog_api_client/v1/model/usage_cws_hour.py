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


class UsageCWSHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "cws_container_count": (int, none_type),
            "cws_host_count": (int, none_type),
            "hour": (datetime,),
            "org_name": (str,),
            "public_id": (str,),
        }

    attribute_map = {
        "cws_container_count": "cws_container_count",
        "cws_host_count": "cws_host_count",
        "hour": "hour",
        "org_name": "org_name",
        "public_id": "public_id",
    }

    def __init__(
        self_,
        cws_container_count: Union[int, none_type, UnsetType] = unset,
        cws_host_count: Union[int, none_type, UnsetType] = unset,
        hour: Union[datetime, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Cloud Workload Security usage for a given organization for a given hour.

        :param cws_container_count: The total number of Cloud Workload Security container hours from the start of the given hour’s month until the given hour.
        :type cws_container_count: int, none_type, optional

        :param cws_host_count: The total number of Cloud Workload Security host hours from the start of the given hour’s month until the given hour.
        :type cws_host_count: int, none_type, optional

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional
        """
        if cws_container_count is not unset:
            kwargs["cws_container_count"] = cws_container_count
        if cws_host_count is not unset:
            kwargs["cws_host_count"] = cws_host_count
        if hour is not unset:
            kwargs["hour"] = hour
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        super().__init__(kwargs)
