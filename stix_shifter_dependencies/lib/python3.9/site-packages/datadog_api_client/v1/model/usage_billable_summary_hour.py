# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.usage_billable_summary_keys import UsageBillableSummaryKeys


class UsageBillableSummaryHour(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.usage_billable_summary_keys import UsageBillableSummaryKeys

        return {
            "billing_plan": (str,),
            "end_date": (datetime,),
            "num_orgs": (int,),
            "org_name": (str,),
            "public_id": (str,),
            "ratio_in_month": (float,),
            "region": (str,),
            "start_date": (datetime,),
            "usage": (UsageBillableSummaryKeys,),
        }

    attribute_map = {
        "billing_plan": "billing_plan",
        "end_date": "end_date",
        "num_orgs": "num_orgs",
        "org_name": "org_name",
        "public_id": "public_id",
        "ratio_in_month": "ratio_in_month",
        "region": "region",
        "start_date": "start_date",
        "usage": "usage",
    }

    def __init__(
        self_,
        billing_plan: Union[str, UnsetType] = unset,
        end_date: Union[datetime, UnsetType] = unset,
        num_orgs: Union[int, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        ratio_in_month: Union[float, UnsetType] = unset,
        region: Union[str, UnsetType] = unset,
        start_date: Union[datetime, UnsetType] = unset,
        usage: Union[UsageBillableSummaryKeys, UnsetType] = unset,
        **kwargs,
    ):
        """
        Response with monthly summary of data billed by Datadog.

        :param billing_plan: The billing plan.
        :type billing_plan: str, optional

        :param end_date: Shows the last date of usage.
        :type end_date: datetime, optional

        :param num_orgs: The number of organizations.
        :type num_orgs: int, optional

        :param org_name: The organization name.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional

        :param ratio_in_month: Shows usage aggregation for a billing period.
        :type ratio_in_month: float, optional

        :param region: The region of the organization.
        :type region: str, optional

        :param start_date: Shows the first date of usage.
        :type start_date: datetime, optional

        :param usage: Response with aggregated usage types.
        :type usage: UsageBillableSummaryKeys, optional
        """
        if billing_plan is not unset:
            kwargs["billing_plan"] = billing_plan
        if end_date is not unset:
            kwargs["end_date"] = end_date
        if num_orgs is not unset:
            kwargs["num_orgs"] = num_orgs
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if ratio_in_month is not unset:
            kwargs["ratio_in_month"] = ratio_in_month
        if region is not unset:
            kwargs["region"] = region
        if start_date is not unset:
            kwargs["start_date"] = start_date
        if usage is not unset:
            kwargs["usage"] = usage
        super().__init__(kwargs)
