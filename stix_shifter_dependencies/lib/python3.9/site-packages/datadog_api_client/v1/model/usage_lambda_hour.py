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


class UsageLambdaHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "func_count": (int, none_type),
            "hour": (datetime,),
            "invocations_sum": (int, none_type),
            "org_name": (str,),
            "public_id": (str,),
        }

    attribute_map = {
        "func_count": "func_count",
        "hour": "hour",
        "invocations_sum": "invocations_sum",
        "org_name": "org_name",
        "public_id": "public_id",
    }

    def __init__(
        self_,
        func_count: Union[int, none_type, UnsetType] = unset,
        hour: Union[datetime, UnsetType] = unset,
        invocations_sum: Union[int, none_type, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Number of lambda functions and sum of the invocations of all lambda functions
        for each hour for a given organization.

        :param func_count: Contains the number of different functions for each region and AWS account.
        :type func_count: int, none_type, optional

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param invocations_sum: Contains the sum of invocations of all functions.
        :type invocations_sum: int, none_type, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional
        """
        if func_count is not unset:
            kwargs["func_count"] = func_count
        if hour is not unset:
            kwargs["hour"] = hour
        if invocations_sum is not unset:
            kwargs["invocations_sum"] = invocations_sum
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        super().__init__(kwargs)
