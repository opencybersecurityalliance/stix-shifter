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


class UsageDBMHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "dbm_host_count": (int, none_type),
            "dbm_queries_count": (int, none_type),
            "hour": (datetime,),
            "org_name": (str,),
            "public_id": (str,),
        }

    attribute_map = {
        "dbm_host_count": "dbm_host_count",
        "dbm_queries_count": "dbm_queries_count",
        "hour": "hour",
        "org_name": "org_name",
        "public_id": "public_id",
    }

    def __init__(
        self_,
        dbm_host_count: Union[int, none_type, UnsetType] = unset,
        dbm_queries_count: Union[int, none_type, UnsetType] = unset,
        hour: Union[datetime, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Database Monitoring usage for a given organization for a given hour.

        :param dbm_host_count: The total number of Database Monitoring host hours from the start of the given hour’s month until the given hour.
        :type dbm_host_count: int, none_type, optional

        :param dbm_queries_count: The total number of normalized Database Monitoring queries from the start of the given hour’s month until the given hour.
        :type dbm_queries_count: int, none_type, optional

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional
        """
        if dbm_host_count is not unset:
            kwargs["dbm_host_count"] = dbm_host_count
        if dbm_queries_count is not unset:
            kwargs["dbm_queries_count"] = dbm_queries_count
        if hour is not unset:
            kwargs["hour"] = hour
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        super().__init__(kwargs)
