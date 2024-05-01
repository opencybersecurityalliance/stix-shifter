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


class UsageIncidentManagementHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "hour": (datetime,),
            "monthly_active_users": (int, none_type),
            "org_name": (str,),
            "public_id": (str,),
        }

    attribute_map = {
        "hour": "hour",
        "monthly_active_users": "monthly_active_users",
        "org_name": "org_name",
        "public_id": "public_id",
    }

    def __init__(
        self_,
        hour: Union[datetime, UnsetType] = unset,
        monthly_active_users: Union[int, none_type, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Incident management usage for a given organization for a given hour.

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param monthly_active_users: Contains the total number monthly active users from the start of the given hour's month until the given hour.
        :type monthly_active_users: int, none_type, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional
        """
        if hour is not unset:
            kwargs["hour"] = hour
        if monthly_active_users is not unset:
            kwargs["monthly_active_users"] = monthly_active_users
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        super().__init__(kwargs)
