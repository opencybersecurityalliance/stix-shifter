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


class UsageFargateHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "apm_fargate_count": (int, none_type),
            "appsec_fargate_count": (int, none_type),
            "avg_profiled_fargate_tasks": (int, none_type),
            "hour": (datetime,),
            "org_name": (str,),
            "public_id": (str,),
            "tasks_count": (int, none_type),
        }

    attribute_map = {
        "apm_fargate_count": "apm_fargate_count",
        "appsec_fargate_count": "appsec_fargate_count",
        "avg_profiled_fargate_tasks": "avg_profiled_fargate_tasks",
        "hour": "hour",
        "org_name": "org_name",
        "public_id": "public_id",
        "tasks_count": "tasks_count",
    }

    def __init__(
        self_,
        apm_fargate_count: Union[int, none_type, UnsetType] = unset,
        appsec_fargate_count: Union[int, none_type, UnsetType] = unset,
        avg_profiled_fargate_tasks: Union[int, none_type, UnsetType] = unset,
        hour: Union[datetime, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        tasks_count: Union[int, none_type, UnsetType] = unset,
        **kwargs,
    ):
        """
        Number of Fargate tasks run and hourly usage.

        :param apm_fargate_count: The high-water mark of APM ECS Fargate tasks during the given hour.
        :type apm_fargate_count: int, none_type, optional

        :param appsec_fargate_count: The Application Security Monitoring ECS Fargate tasks during the given hour.
        :type appsec_fargate_count: int, none_type, optional

        :param avg_profiled_fargate_tasks: The average profiled task count for Fargate Profiling.
        :type avg_profiled_fargate_tasks: int, none_type, optional

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional

        :param tasks_count: The number of Fargate tasks run.
        :type tasks_count: int, none_type, optional
        """
        if apm_fargate_count is not unset:
            kwargs["apm_fargate_count"] = apm_fargate_count
        if appsec_fargate_count is not unset:
            kwargs["appsec_fargate_count"] = appsec_fargate_count
        if avg_profiled_fargate_tasks is not unset:
            kwargs["avg_profiled_fargate_tasks"] = avg_profiled_fargate_tasks
        if hour is not unset:
            kwargs["hour"] = hour
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if tasks_count is not unset:
            kwargs["tasks_count"] = tasks_count
        super().__init__(kwargs)
