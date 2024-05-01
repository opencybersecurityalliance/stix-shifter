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


class UsageBillableSummaryBody(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "account_billable_usage": (int,),
            "elapsed_usage_hours": (int,),
            "first_billable_usage_hour": (datetime,),
            "last_billable_usage_hour": (datetime,),
            "org_billable_usage": (int,),
            "percentage_in_account": (float,),
            "usage_unit": (str,),
        }

    attribute_map = {
        "account_billable_usage": "account_billable_usage",
        "elapsed_usage_hours": "elapsed_usage_hours",
        "first_billable_usage_hour": "first_billable_usage_hour",
        "last_billable_usage_hour": "last_billable_usage_hour",
        "org_billable_usage": "org_billable_usage",
        "percentage_in_account": "percentage_in_account",
        "usage_unit": "usage_unit",
    }

    def __init__(
        self_,
        account_billable_usage: Union[int, UnsetType] = unset,
        elapsed_usage_hours: Union[int, UnsetType] = unset,
        first_billable_usage_hour: Union[datetime, UnsetType] = unset,
        last_billable_usage_hour: Union[datetime, UnsetType] = unset,
        org_billable_usage: Union[int, UnsetType] = unset,
        percentage_in_account: Union[float, UnsetType] = unset,
        usage_unit: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Response with properties for each aggregated usage type.

        :param account_billable_usage: The total account usage.
        :type account_billable_usage: int, optional

        :param elapsed_usage_hours: Elapsed usage hours for some billable product.
        :type elapsed_usage_hours: int, optional

        :param first_billable_usage_hour: The first billable hour for the org.
        :type first_billable_usage_hour: datetime, optional

        :param last_billable_usage_hour: The last billable hour for the org.
        :type last_billable_usage_hour: datetime, optional

        :param org_billable_usage: The number of units used within the billable timeframe.
        :type org_billable_usage: int, optional

        :param percentage_in_account: The percentage of account usage the org represents.
        :type percentage_in_account: float, optional

        :param usage_unit: Units pertaining to the usage.
        :type usage_unit: str, optional
        """
        if account_billable_usage is not unset:
            kwargs["account_billable_usage"] = account_billable_usage
        if elapsed_usage_hours is not unset:
            kwargs["elapsed_usage_hours"] = elapsed_usage_hours
        if first_billable_usage_hour is not unset:
            kwargs["first_billable_usage_hour"] = first_billable_usage_hour
        if last_billable_usage_hour is not unset:
            kwargs["last_billable_usage_hour"] = last_billable_usage_hour
        if org_billable_usage is not unset:
            kwargs["org_billable_usage"] = org_billable_usage
        if percentage_in_account is not unset:
            kwargs["percentage_in_account"] = percentage_in_account
        if usage_unit is not unset:
            kwargs["usage_unit"] = usage_unit
        super().__init__(kwargs)
