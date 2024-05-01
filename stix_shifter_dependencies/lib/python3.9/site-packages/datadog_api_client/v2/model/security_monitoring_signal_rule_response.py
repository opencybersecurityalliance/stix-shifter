# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.security_monitoring_rule_case import SecurityMonitoringRuleCase
    from datadog_api_client.v2.model.security_monitoring_filter import SecurityMonitoringFilter
    from datadog_api_client.v2.model.security_monitoring_rule_options import SecurityMonitoringRuleOptions
    from datadog_api_client.v2.model.security_monitoring_signal_rule_response_query import (
        SecurityMonitoringSignalRuleResponseQuery,
    )
    from datadog_api_client.v2.model.security_monitoring_signal_rule_type import SecurityMonitoringSignalRuleType


class SecurityMonitoringSignalRuleResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_rule_case import SecurityMonitoringRuleCase
        from datadog_api_client.v2.model.security_monitoring_filter import SecurityMonitoringFilter
        from datadog_api_client.v2.model.security_monitoring_rule_options import SecurityMonitoringRuleOptions
        from datadog_api_client.v2.model.security_monitoring_signal_rule_response_query import (
            SecurityMonitoringSignalRuleResponseQuery,
        )
        from datadog_api_client.v2.model.security_monitoring_signal_rule_type import SecurityMonitoringSignalRuleType

        return {
            "cases": ([SecurityMonitoringRuleCase],),
            "created_at": (int,),
            "creation_author_id": (int,),
            "deprecation_date": (int,),
            "filters": ([SecurityMonitoringFilter],),
            "has_extended_title": (bool,),
            "id": (str,),
            "is_default": (bool,),
            "is_deleted": (bool,),
            "is_enabled": (bool,),
            "message": (str,),
            "name": (str,),
            "options": (SecurityMonitoringRuleOptions,),
            "queries": ([SecurityMonitoringSignalRuleResponseQuery],),
            "tags": ([str],),
            "type": (SecurityMonitoringSignalRuleType,),
            "update_author_id": (int,),
            "version": (int,),
        }

    attribute_map = {
        "cases": "cases",
        "created_at": "createdAt",
        "creation_author_id": "creationAuthorId",
        "deprecation_date": "deprecationDate",
        "filters": "filters",
        "has_extended_title": "hasExtendedTitle",
        "id": "id",
        "is_default": "isDefault",
        "is_deleted": "isDeleted",
        "is_enabled": "isEnabled",
        "message": "message",
        "name": "name",
        "options": "options",
        "queries": "queries",
        "tags": "tags",
        "type": "type",
        "update_author_id": "updateAuthorId",
        "version": "version",
    }

    def __init__(
        self_,
        cases: Union[List[SecurityMonitoringRuleCase], UnsetType] = unset,
        created_at: Union[int, UnsetType] = unset,
        creation_author_id: Union[int, UnsetType] = unset,
        deprecation_date: Union[int, UnsetType] = unset,
        filters: Union[List[SecurityMonitoringFilter], UnsetType] = unset,
        has_extended_title: Union[bool, UnsetType] = unset,
        id: Union[str, UnsetType] = unset,
        is_default: Union[bool, UnsetType] = unset,
        is_deleted: Union[bool, UnsetType] = unset,
        is_enabled: Union[bool, UnsetType] = unset,
        message: Union[str, UnsetType] = unset,
        name: Union[str, UnsetType] = unset,
        options: Union[SecurityMonitoringRuleOptions, UnsetType] = unset,
        queries: Union[List[SecurityMonitoringSignalRuleResponseQuery], UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        type: Union[SecurityMonitoringSignalRuleType, UnsetType] = unset,
        update_author_id: Union[int, UnsetType] = unset,
        version: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Rule.

        :param cases: Cases for generating signals.
        :type cases: [SecurityMonitoringRuleCase], optional

        :param created_at: When the rule was created, timestamp in milliseconds.
        :type created_at: int, optional

        :param creation_author_id: User ID of the user who created the rule.
        :type creation_author_id: int, optional

        :param deprecation_date: When the rule will be deprecated, timestamp in milliseconds.
        :type deprecation_date: int, optional

        :param filters: Additional queries to filter matched events before they are processed.
        :type filters: [SecurityMonitoringFilter], optional

        :param has_extended_title: Whether the notifications include the triggering group-by values in their title.
        :type has_extended_title: bool, optional

        :param id: The ID of the rule.
        :type id: str, optional

        :param is_default: Whether the rule is included by default.
        :type is_default: bool, optional

        :param is_deleted: Whether the rule has been deleted.
        :type is_deleted: bool, optional

        :param is_enabled: Whether the rule is enabled.
        :type is_enabled: bool, optional

        :param message: Message for generated signals.
        :type message: str, optional

        :param name: The name of the rule.
        :type name: str, optional

        :param options: Options on rules.
        :type options: SecurityMonitoringRuleOptions, optional

        :param queries: Queries for selecting logs which are part of the rule.
        :type queries: [SecurityMonitoringSignalRuleResponseQuery], optional

        :param tags: Tags for generated signals.
        :type tags: [str], optional

        :param type: The rule type.
        :type type: SecurityMonitoringSignalRuleType, optional

        :param update_author_id: User ID of the user who updated the rule.
        :type update_author_id: int, optional

        :param version: The version of the rule.
        :type version: int, optional
        """
        if cases is not unset:
            kwargs["cases"] = cases
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if creation_author_id is not unset:
            kwargs["creation_author_id"] = creation_author_id
        if deprecation_date is not unset:
            kwargs["deprecation_date"] = deprecation_date
        if filters is not unset:
            kwargs["filters"] = filters
        if has_extended_title is not unset:
            kwargs["has_extended_title"] = has_extended_title
        if id is not unset:
            kwargs["id"] = id
        if is_default is not unset:
            kwargs["is_default"] = is_default
        if is_deleted is not unset:
            kwargs["is_deleted"] = is_deleted
        if is_enabled is not unset:
            kwargs["is_enabled"] = is_enabled
        if message is not unset:
            kwargs["message"] = message
        if name is not unset:
            kwargs["name"] = name
        if options is not unset:
            kwargs["options"] = options
        if queries is not unset:
            kwargs["queries"] = queries
        if tags is not unset:
            kwargs["tags"] = tags
        if type is not unset:
            kwargs["type"] = type
        if update_author_id is not unset:
            kwargs["update_author_id"] = update_author_id
        if version is not unset:
            kwargs["version"] = version
        super().__init__(kwargs)
