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


class UsageCloudSecurityPostureManagementHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "aas_host_count": (float, none_type),
            "aws_host_count": (float, none_type),
            "azure_host_count": (float, none_type),
            "compliance_host_count": (float, none_type),
            "container_count": (float, none_type),
            "gcp_host_count": (float, none_type),
            "host_count": (float, none_type),
            "hour": (datetime,),
            "org_name": (str,),
            "public_id": (str,),
        }

    attribute_map = {
        "aas_host_count": "aas_host_count",
        "aws_host_count": "aws_host_count",
        "azure_host_count": "azure_host_count",
        "compliance_host_count": "compliance_host_count",
        "container_count": "container_count",
        "gcp_host_count": "gcp_host_count",
        "host_count": "host_count",
        "hour": "hour",
        "org_name": "org_name",
        "public_id": "public_id",
    }

    def __init__(
        self_,
        aas_host_count: Union[float, none_type, UnsetType] = unset,
        aws_host_count: Union[float, none_type, UnsetType] = unset,
        azure_host_count: Union[float, none_type, UnsetType] = unset,
        compliance_host_count: Union[float, none_type, UnsetType] = unset,
        container_count: Union[float, none_type, UnsetType] = unset,
        gcp_host_count: Union[float, none_type, UnsetType] = unset,
        host_count: Union[float, none_type, UnsetType] = unset,
        hour: Union[datetime, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Cloud Security Posture Management usage for a given organization for a given hour.

        :param aas_host_count: The number of Cloud Security Posture Management Azure app services hosts during a given hour.
        :type aas_host_count: float, none_type, optional

        :param aws_host_count: The number of Cloud Security Posture Management AWS hosts during a given hour.
        :type aws_host_count: float, none_type, optional

        :param azure_host_count: The number of Cloud Security Posture Management Azure hosts during a given hour.
        :type azure_host_count: float, none_type, optional

        :param compliance_host_count: The number of Cloud Security Posture Management hosts during a given hour.
        :type compliance_host_count: float, none_type, optional

        :param container_count: The total number of Cloud Security Posture Management containers during a given hour.
        :type container_count: float, none_type, optional

        :param gcp_host_count: The number of Cloud Security Posture Management GCP hosts during a given hour.
        :type gcp_host_count: float, none_type, optional

        :param host_count: The total number of Cloud Security Posture Management hosts during a given hour.
        :type host_count: float, none_type, optional

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional
        """
        if aas_host_count is not unset:
            kwargs["aas_host_count"] = aas_host_count
        if aws_host_count is not unset:
            kwargs["aws_host_count"] = aws_host_count
        if azure_host_count is not unset:
            kwargs["azure_host_count"] = azure_host_count
        if compliance_host_count is not unset:
            kwargs["compliance_host_count"] = compliance_host_count
        if container_count is not unset:
            kwargs["container_count"] = container_count
        if gcp_host_count is not unset:
            kwargs["gcp_host_count"] = gcp_host_count
        if host_count is not unset:
            kwargs["host_count"] = host_count
        if hour is not unset:
            kwargs["hour"] = hour
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        super().__init__(kwargs)
