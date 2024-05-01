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
    from datadog_api_client.v1.model.usage_attribution_values import UsageAttributionValues


class UsageAttributionBody(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.usage_attribution_tag_names import UsageAttributionTagNames
        from datadog_api_client.v1.model.usage_attribution_values import UsageAttributionValues

        return {
            "month": (datetime,),
            "org_name": (str,),
            "public_id": (str,),
            "tag_config_source": (str,),
            "tags": (UsageAttributionTagNames,),
            "updated_at": (str,),
            "values": (UsageAttributionValues,),
        }

    attribute_map = {
        "month": "month",
        "org_name": "org_name",
        "public_id": "public_id",
        "tag_config_source": "tag_config_source",
        "tags": "tags",
        "updated_at": "updated_at",
        "values": "values",
    }

    def __init__(
        self_,
        month: Union[datetime, UnsetType] = unset,
        org_name: Union[str, UnsetType] = unset,
        public_id: Union[str, UnsetType] = unset,
        tag_config_source: Union[str, UnsetType] = unset,
        tags: Union[UsageAttributionTagNames, none_type, UnsetType] = unset,
        updated_at: Union[str, UnsetType] = unset,
        values: Union[UsageAttributionValues, UnsetType] = unset,
        **kwargs,
    ):
        """
        Usage Summary by tag for a given organization.

        :param month: Datetime in ISO-8601 format, UTC, precise to month: [YYYY-MM].
        :type month: datetime, optional

        :param org_name: The name of the organization.
        :type org_name: str, optional

        :param public_id: The organization public ID.
        :type public_id: str, optional

        :param tag_config_source: The source of the usage attribution tag configuration and the selected tags in the format ``<source_org_name>:::<selected tag 1>///<selected tag 2>///<selected tag 3>``.
        :type tag_config_source: str, optional

        :param tags: Tag keys and values.

            A ``null`` value here means that the requested tag breakdown cannot be applied because it does not match the `tags
            configured for usage attribution <https://docs.datadoghq.com/account_management/billing/usage_attribution/#getting-started>`_.
            In this scenario the API returns the total usage, not broken down by tags.
        :type tags: UsageAttributionTagNames, none_type, optional

        :param updated_at: Shows the the most recent hour in the current months for all organizations for which all usages were calculated.
        :type updated_at: str, optional

        :param values: Fields in Usage Summary by tag(s).
        :type values: UsageAttributionValues, optional
        """
        if month is not unset:
            kwargs["month"] = month
        if org_name is not unset:
            kwargs["org_name"] = org_name
        if public_id is not unset:
            kwargs["public_id"] = public_id
        if tag_config_source is not unset:
            kwargs["tag_config_source"] = tag_config_source
        if tags is not unset:
            kwargs["tags"] = tags
        if updated_at is not unset:
            kwargs["updated_at"] = updated_at
        if values is not unset:
            kwargs["values"] = values
        super().__init__(kwargs)
