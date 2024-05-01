# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.usage_attribution_tag_names import UsageAttributionTagNames
    from datadog_api_client.v1.model.hourly_usage_attribution_usage_type import HourlyUsageAttributionUsageType


class HourlyUsageAttributionBody(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.usage_attribution_tag_names import UsageAttributionTagNames
        from datadog_api_client.v1.model.hourly_usage_attribution_usage_type import HourlyUsageAttributionUsageType

        return {
            "hour": (datetime,),
            "org_name": (str,),
            "public_id": (str,),
            "region": (str,),
            "tag_config_source": (str,),
            "tags": (UsageAttributionTagNames,),
            "total_usage_sum": (float,),
            "updated_at": (str,),
            "usage_type": (HourlyUsageAttributionUsageType,),
        }

    attribute_map = {
        "hour": "hour",
        "org_name": "org_name",
        "public_id": "public_id",
        "region": "region",
        "tag_config_source": "tag_config_source",
        "tags": "tags",
        "total_usage_sum": "total_usage_sum",
        "updated_at": "updated_at",
        "usage_type": "usage_type",
    }

    def __init__(
        self_,
        hour: Union[datetime, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        region: Union[str, UnsetType] = unset,
        tag_config_source: Union[str, UnsetType] = unset,
        tags: Union[UsageAttributionTagNames, none_type, UnsetType] = unset,
        total_usage_sum: Union[float, UnsetType] = unset,
        updated_at: Union[str, UnsetType] = unset,
        usage_type: Union[HourlyUsageAttributionUsageType, UnsetType] = unset,
        **kwargs,
    ):
        """
        The usage for one set of tags for one hour.

        :param hour: The hour for the usage.
        :type hour: datetime, optional

        :param org_name: The name of the organization.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional

        :param region: The region of the Datadog instance that the organization belongs to.
        :type region: str, optional

        :param tag_config_source: The source of the usage attribution tag configuration and the selected tags in the format of ``<source_org_name>:::<selected tag 1>///<selected tag 2>///<selected tag 3>``.
        :type tag_config_source: str, optional

        :param tags: Tag keys and values.

            A ``null`` value here means that the requested tag breakdown cannot be applied because it does not match the `tags
            configured for usage attribution <https://docs.datadoghq.com/account_management/billing/usage_attribution/#getting-started>`_.
            In this scenario the API returns the total usage, not broken down by tags.
        :type tags: UsageAttributionTagNames, none_type, optional

        :param total_usage_sum: Total product usage for the given tags within the hour.
        :type total_usage_sum: float, optional

        :param updated_at: Shows the most recent hour in the current month for all organizations where usages are calculated.
        :type updated_at: str, optional

        :param usage_type: Supported products for hourly usage attribution requests.
        :type usage_type: HourlyUsageAttributionUsageType, optional
        """
        if hour is not unset:
            kwargs["hour"] = hour
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if region is not unset:
            kwargs["region"] = region
        if tag_config_source is not unset:
            kwargs["tag_config_source"] = tag_config_source
        if tags is not unset:
            kwargs["tags"] = tags
        if total_usage_sum is not unset:
            kwargs["total_usage_sum"] = total_usage_sum
        if updated_at is not unset:
            kwargs["updated_at"] = updated_at
        if usage_type is not unset:
            kwargs["usage_type"] = usage_type
        super().__init__(kwargs)
