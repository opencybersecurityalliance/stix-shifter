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


class UsageHostHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "agent_host_count": (int, none_type),
            "alibaba_host_count": (int, none_type),
            "apm_azure_app_service_host_count": (int, none_type),
            "apm_host_count": (int, none_type),
            "aws_host_count": (int, none_type),
            "azure_host_count": (int, none_type),
            "container_count": (int, none_type),
            "gcp_host_count": (int, none_type),
            "heroku_host_count": (int, none_type),
            "host_count": (int, none_type),
            "hour": (datetime, none_type),
            "infra_azure_app_service": (int, none_type),
            "opentelemetry_apm_host_count": (int, none_type),
            "opentelemetry_host_count": (int, none_type),
            "org_name": (str,),
            "public_id": (str,),
            "vsphere_host_count": (int, none_type),
        }

    attribute_map = {
        "agent_host_count": "agent_host_count",
        "alibaba_host_count": "alibaba_host_count",
        "apm_azure_app_service_host_count": "apm_azure_app_service_host_count",
        "apm_host_count": "apm_host_count",
        "aws_host_count": "aws_host_count",
        "azure_host_count": "azure_host_count",
        "container_count": "container_count",
        "gcp_host_count": "gcp_host_count",
        "heroku_host_count": "heroku_host_count",
        "host_count": "host_count",
        "hour": "hour",
        "infra_azure_app_service": "infra_azure_app_service",
        "opentelemetry_apm_host_count": "opentelemetry_apm_host_count",
        "opentelemetry_host_count": "opentelemetry_host_count",
        "org_name": "org_name",
        "public_id": "public_id",
        "vsphere_host_count": "vsphere_host_count",
    }

    def __init__(
        self_,
        agent_host_count: Union[int, none_type, UnsetType] = unset,
        alibaba_host_count: Union[int, none_type, UnsetType] = unset,
        apm_azure_app_service_host_count: Union[int, none_type, UnsetType] = unset,
        apm_host_count: Union[int, none_type, UnsetType] = unset,
        aws_host_count: Union[int, none_type, UnsetType] = unset,
        azure_host_count: Union[int, none_type, UnsetType] = unset,
        container_count: Union[int, none_type, UnsetType] = unset,
        gcp_host_count: Union[int, none_type, UnsetType] = unset,
        heroku_host_count: Union[int, none_type, UnsetType] = unset,
        host_count: Union[int, none_type, UnsetType] = unset,
        hour: Union[datetime, none_type, UnsetType] = unset,
        infra_azure_app_service: Union[int, none_type, UnsetType] = unset,
        opentelemetry_apm_host_count: Union[int, none_type, UnsetType] = unset,
        opentelemetry_host_count: Union[int, none_type, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        vsphere_host_count: Union[int, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        Number of hosts/containers recorded for each hour for a given organization.

        :param agent_host_count: Contains the total number of infrastructure hosts reporting
            during a given hour that were running the Datadog Agent.
        :type agent_host_count: int, none_type, optional

        :param alibaba_host_count: Contains the total number of hosts that reported through Alibaba integration
            (and were NOT running the Datadog Agent).
        :type alibaba_host_count: int, none_type, optional

        :param apm_azure_app_service_host_count: Contains the total number of Azure App Services hosts using APM.
        :type apm_azure_app_service_host_count: int, none_type, optional

        :param apm_host_count: Shows the total number of hosts using APM during the hour,
            these are counted as billable (except during trial periods).
        :type apm_host_count: int, none_type, optional

        :param aws_host_count: Contains the total number of hosts that reported through the AWS integration
            (and were NOT running the Datadog Agent).
        :type aws_host_count: int, none_type, optional

        :param azure_host_count: Contains the total number of hosts that reported through Azure integration
            (and were NOT running the Datadog Agent).
        :type azure_host_count: int, none_type, optional

        :param container_count: Shows the total number of containers reported by the Docker integration during the hour.
        :type container_count: int, none_type, optional

        :param gcp_host_count: Contains the total number of hosts that reported through the Google Cloud integration
            (and were NOT running the Datadog Agent).
        :type gcp_host_count: int, none_type, optional

        :param heroku_host_count: Contains the total number of Heroku dynos reported by the Datadog Agent.
        :type heroku_host_count: int, none_type, optional

        :param host_count: Contains the total number of billable infrastructure hosts reporting during a given hour.
            This is the sum of ``agent_host_count`` , ``aws_host_count`` , and ``gcp_host_count``.
        :type host_count: int, none_type, optional

        :param hour: The hour for the usage.
        :type hour: datetime, none_type, optional

        :param infra_azure_app_service: Contains the total number of hosts that reported through the Azure App Services integration
            (and were NOT running the Datadog Agent).
        :type infra_azure_app_service: int, none_type, optional

        :param opentelemetry_apm_host_count: Contains the total number of hosts using APM reported by Datadog exporter for the OpenTelemetry Collector.
        :type opentelemetry_apm_host_count: int, none_type, optional

        :param opentelemetry_host_count: Contains the total number of hosts reported by Datadog exporter for the OpenTelemetry Collector.
        :type opentelemetry_host_count: int, none_type, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional

        :param vsphere_host_count: Contains the total number of hosts that reported through vSphere integration
            (and were NOT running the Datadog Agent).
        :type vsphere_host_count: int, none_type, optional
        """
        if agent_host_count is not unset:
            kwargs["agent_host_count"] = agent_host_count
        if alibaba_host_count is not unset:
            kwargs["alibaba_host_count"] = alibaba_host_count
        if apm_azure_app_service_host_count is not unset:
            kwargs["apm_azure_app_service_host_count"] = apm_azure_app_service_host_count
        if apm_host_count is not unset:
            kwargs["apm_host_count"] = apm_host_count
        if aws_host_count is not unset:
            kwargs["aws_host_count"] = aws_host_count
        if azure_host_count is not unset:
            kwargs["azure_host_count"] = azure_host_count
        if container_count is not unset:
            kwargs["container_count"] = container_count
        if gcp_host_count is not unset:
            kwargs["gcp_host_count"] = gcp_host_count
        if heroku_host_count is not unset:
            kwargs["heroku_host_count"] = heroku_host_count
        if host_count is not unset:
            kwargs["host_count"] = host_count
        if hour is not unset:
            kwargs["hour"] = hour
        if infra_azure_app_service is not unset:
            kwargs["infra_azure_app_service"] = infra_azure_app_service
        if opentelemetry_apm_host_count is not unset:
            kwargs["opentelemetry_apm_host_count"] = opentelemetry_apm_host_count
        if opentelemetry_host_count is not unset:
            kwargs["opentelemetry_host_count"] = opentelemetry_host_count
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if vsphere_host_count is not unset:
            kwargs["vsphere_host_count"] = vsphere_host_count
        super().__init__(kwargs)
