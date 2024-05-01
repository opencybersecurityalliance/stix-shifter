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


class UsageSNMPHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "hour": (datetime,),
            "org_name": (str,),
            "public_id": (str,),
            "snmp_devices": (int, none_type),
        }

    attribute_map = {
        "hour": "hour",
        "org_name": "org_name",
        "public_id": "public_id",
        "snmp_devices": "snmp_devices",
    }

    def __init__(
        self_,
        hour: Union[datetime, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        snmp_devices: Union[int, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        The number of SNMP devices for each hour for a given organization.

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional

        :param snmp_devices: Contains the number of SNMP devices.
        :type snmp_devices: int, none_type, optional
        """
        if hour is not unset:
            kwargs["hour"] = hour
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if snmp_devices is not unset:
            kwargs["snmp_devices"] = snmp_devices
        super().__init__(kwargs)
